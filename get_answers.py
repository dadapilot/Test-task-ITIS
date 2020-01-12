import sqlite3

class GetAnswers():

    def __init__(self):

        self.conn = sqlite3.connect("database.db")
        self.curs = self.conn.cursor()

    def ans1(self):

        '''
        Посетители из какой страны совершают больше всего действий на сайте?
        '''

        self.curs.execute('''
                            SELECT Countries.country, count(action) AS act
                            FROM Countries, Actions
                            WHERE Countries.ip_adress = Actions.ip_adress
                            GROUP BY Countries.country
                            ORDER BY count(action) DESC LIMIT 1;
                         ''')

        return self.curs.fetchall()

    def ans2(self, cat):

        '''
        Посетители из какой страны чаще всего интересуются товарами из определенных категорий?
        '''

        self.curs.execute('''
                             SELECT count(*), country
                             FROM Countries, Actions
                             WHERE Countries.ip_adress = Actions.ip_adress
                             AND Actions.category =:cat
                             GROUP BY Countries.country
                             ORDER BY count(country) DESC LIMIT 1;
                          ''', {"cat": cat})

        return self.curs.fetchall()

    def ans3(self, dates):
        dates[0] += ' 00:00:00'
        dates[1] += ' 23:59:59'

        """
        Сколько брошенных (не оплаченных) корзин имеется за определенный период?
        """

        self.curs.execute('''
                            SELECT ABS(t1.cnt - t2.cnt)
                            FROM (SELECT count(Orders.order_id) as cnt FROM Orders
                            WHERE (Orders.datetime BETWEEN (?) AND (?))
                            ) AS t1
                            INNER JOIN (SELECT count(trans_id) as cnt FROM Transactions
                            WHERE (Transactions.datetime BETWEEN (?) AND (?))
                            ) AS t2;
                        ''', (dates[0],dates[1],dates[0],dates[1]))
        return self.curs.fetchall()


