drop table if exists Countries;
create table Countries (
    ip_adress text primary key not null ,
    country text
);

drop table if exists Actions;
CREATE TABLE Actions (
    actions_ID integer PRIMARY KEY AUTOINCREMENT,
    ip_adress text NOT NULL,
    datetime text not null,
    action text not null,
    category text,
    FOREIGN KEY (ip_adress) REFERENCES Countries(ip_adress),
    FOREIGN KEY (category) REFERENCES Categories(category)
);

drop table if exists Transactions;
CREATE TABLE Transactions (
    trans_id integer PRIMARY KEY AUTOINCREMENT,
    ip_adress text NOT NULL,
    datetime text not null,
    order_id integer NOT NULL,
    FOREIGN KEY (ip_adress) REFERENCES Countries(ip_adress),
    FOREIGN KEY (order_id) REFERENCES Orders(order_id)
);

drop table if exists Orders;
CREATE TABLE Orders (
    order_id integer PRIMARY KEY,
    ip_adress integer not null,
    category text not null,
    datetime text not null,
    FOREIGN KEY (category) REFERENCES Categories(category),
    FOREIGN KEY (ip_adress) REFERENCES Countries(ip_adress)
);

drop table if exists Categories;
CREATE TABLE Categories (
    category text PRIMARY KEY,
    ip_adress integer not null,
    FOREIGN KEY (ip_adress) REFERENCES Countries(ip_adress)
    
);
