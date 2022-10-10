import mysql.connector

from util.connector_util import ConnectorUtil
from util.secrets import Secrets

connector_util = ConnectorUtil

# Example queries

if __name__ == '__main__':
    connection = mysql.connector.connect(host='127.0.0.1',
                                         port=3306,
                                         database='Northwind',
                                         user=Secrets.MYSQL_USER,
                                         password=Secrets.MYSQL_PASSWORD)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Category;')
    connector_util.print_query(cursor)

    cursor.execute('SELECT custId, contactName, phone FROM Customer;')
    connector_util.print_query(cursor)

    cursor.execute('CREATE TABLE IF NOT EXISTS Cats ('
                   'name VARCHAR(20),'
                   'breed VARCHAR(20),'
                   'age INT'
                   ')')
    cursor.execute('SELECT * FROM Cats;')
    connector_util.print_query(cursor)

    cursor.close()
    connection.close()
