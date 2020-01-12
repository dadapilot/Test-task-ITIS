
import re
import sqlite3
import urllib
from collections import namedtuple
from urllib.parse import urldefrag, parse_qsl
from pysyge.pysyge import GeoLocator, MODE_MEMORY


class Log_Parser:

    def __init__(self):

        # устанавливаем соединение с БД
        # и создаем курсор для отправки запросов

        self.conn = sqlite3.connect('database.db')
        self.curs = self.conn.cursor()

        # список с IP, URL, датой для каждой строки лога
        self.parse_list = []

        self.countries = []
        self.orders = []

        #словарь вида (ip_adress : category)
        self.categories = dict()

        self.schema()
        self.log_list()

    # закрытие соединения с БД
    def __del__(self):
        self.curs.close()
        self.conn.close()

    def schema(self):
        with open('schema.sql') as s:
            self.curs.executescript(s.read())

    def log_list(self):

        reg_exp = r"^.*?(?P<datetime>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*?(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*?(?P<url>http.*)$"
        # компилируем регулярное выражение для строк
        pattern = re.compile(reg_exp)

        # создаем именованный кортеж

        key_list = namedtuple('key_list', [
            'datetime',
            'IP',
            'URL'
        ])

        with open('logs.txt', 'r', encoding='utf-8') as f:

            # построчно разбираем лог файл
            for string in f:
                parse_str = pattern.match(string)
                # получаем список для каждой строки
                self.parse_list.append(key_list(
                    parse_str.group('datetime'),
                    parse_str.group('ip'),
                    parse_str.group('url')
                ))

    def parse_URL(self, URL):

        # разделяем url "scheme='https', netloc='all_to_the_bottom.com', path='/frozen_fish/shark/', params='', query='', fragment=''"
        url = urllib.parse.urlparse(URL)
        url_reg_exp=r"^\/(?P<fragment>[\w_]+)"
        pattern = re.compile(url_reg_exp)
        # находим в 'path' первый фрагмент, соответствующий паттерну (действие)
        act = pattern.match(url.path)

        if act is None:
            return None

        return act.group('fragment')

    def url_params(self, url):
        # получаем параметры url
        url_frag = urllib.parse.urlparse(url)
        # словарь для query='goods_id=2&amount=2&cart_id=8664' вида: {'goods_id': '2', 'amount': '2', 'cart_id': '8664'}
        return dict(parse_qsl(url_frag.query))

    def country_by_IP(self, IP):
        # pysyge
        geodata = GeoLocator('SxGeoCity.dat', MODE_MEMORY)
        location = geodata.get_location(IP, detailed=False)
        try:
            return location['country_iso']
        except TypeError:
            return 'Unknown'

    def parse(self):

        for cort in self.parse_list:
            if cort.IP not in self.countries:
                self.create_Countries(cort.IP)
                self.countries.append(cort.IP)
            self.fill_tables(cort)

    def create_Category(self, cat, IP):
        self.curs.execute("INSERT INTO {0}({1},{2}) VALUES (?, ?);".format('Categories', 'category', 'ip_adress'),
                          (cat, self.country_by_IP(IP)))

        self.conn.commit()


    def create_Countries(self, IP):
        self.curs.execute("INSERT INTO {0}({1},{2}) VALUES (?, ?);".format('Countries', 'ip_adress', 'country'),
                         (IP, self.country_by_IP(IP)))

        self.conn.commit()

    def create_Orders(self, items):
        self.curs.execute('''
                            INSERT INTO {0}({1},{2},{3},{4}) VALUES (?, ?, ?, ?);
                         '''.format('orders', 'ip_adress', 'order_id', 'category', 'datetime'), items)

    def create_Actions(self, act):
        self.curs.execute('''
                            INSERT INTO {0}({1},{2},{3}, {4}) VALUES (?, ?, ?, ?);
                         '''.format('Actions', 'action', 'ip_adress', 'datetime', 'category'), act)
        self.conn.commit()

    def create_Transactions(self,trans):
        self.curs.execute('''
                            INSERT INTO {0}({1},{2},{3}) VALUES (?, ?, ?);
                         '''.format('Transactions', 'ip_adress', 'order_id', 'datetime'), trans)
        self.conn.commit()

    def fill_tables(self, cort):
        act = self.parse_URL(cort.URL)
        category_list = []
        cat = None
        if act is None:
            action = 'main'
        elif act == 'cart':
            action = 'cart'
            params = self.url_params(cort.URL)
            order_id = int(params['cart_id'][:-1])   # без /
            if order_id not in self.orders:
                self.orders.append(order_id)

                #[IP : cort.ip, order_id : params['cart_id'], product_id : params['goods_id'], category : self.categories['IP']]

                items = (cort.IP, order_id, self.categories[cort.IP], cort.datetime)
                self.create_Orders(items)
        elif act == 'pay':
            action = 'pay'
        elif 'success_pay' in act:  # подстрока success_pay в строке вида success_pay_8670
            order_id = int(act[12:])
            items = (cort.IP, order_id, self.categories[cort.IP], cort.datetime)
            self.create_Orders(items)
            self.create_Transactions((cort.IP, order_id, cort.datetime))
            return None
        else:
            action = 'category'
            category_list.append(act)
            self.categories[cort.IP] = act
            cat = act
            if act not in category_list:
                self.create_Category(act, cort.IP)

        self.create_Actions((action, cort.IP, cort.datetime, cat))
