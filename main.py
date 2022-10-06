import mysql.connector

from util.connector_util import ConnectorUtil

connector_util = ConnectorUtil

# Example queries

if __name__ == '__main__':
    connection = mysql.connector.connect(host='localhost',
                                         port=3306,
                                         database='Northwind',
                                         user='user',
                                         password='user')
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
