from decimal import Decimal

from test.util.connector_util import fetch_data_print


class TestSubQueries:

    # MySQL Subquery
    def test_select_employment_age_when_hired(self, cursor):
        data = fetch_data_print(cursor, 'SELECT * FROM '
                                        '(SELECT employeeId, firstName, lastName, '
                                        'FLOOR((DATEDIFF(hireDate, birthDate) / 365)) as employmentAge '
                                        'FROM Employee '
                                        'ORDER BY employmentAge DESC) AS EmpDate;')

        assert data[0] == (4, 'Yael', 'Peled', 55)
        assert data[8] == (9, 'Zoya', 'Dolgopyatova', 28)

    # MySQL Subquery
    def test_select_employment_max_min_avg_age_when_hired(self, cursor):
        data = fetch_data_print(cursor, 'SELECT MAX(employmentAge) as maxAge, '
                                        'MIN(employmentAge) as minAge,'
                                        'AVG(employmentAge) FROM '
                                        '(SELECT employeeId, firstName, lastName, '
                                        'FLOOR((DATEDIFF(hireDate, birthDate) / 365)) as employmentAge '
                                        'FROM Employee '
                                        'ORDER BY employmentAge DESC) AS EmpDate;')

        assert data[0] == (55, 28, Decimal('36.7778'))

    # MySQL Subquery
    def test_select_product_where_price_bigger_than_avg_order_price(self, cursor):
        data = fetch_data_print(cursor, 'SELECT productId, productName, unitPrice FROM Product '
                                        'WHERE unitPrice > '
                                        '(SELECT AVG(unitPrice) FROM OrderDetail);')

        assert data[0] == (7, 'Product HMLNI', Decimal('30.00'))
        assert data[25] == (72, 'Product GEEOO', Decimal('34.80'))

    # MySQL Subquery
    def test_select_customer_who_order_more_than_15_orders(self, cursor):
        data = fetch_data_print(cursor, 'SELECT custId, contactName, companyName, country, phone '
                                        'FROM Customer '
                                        'WHERE EXISTS( SELECT custId FROM '
                                        '(SELECT custId, COUNT(*) as orders FROM SalesOrder '
                                        'GROUP BY custId) AS CustomerOrders '
                                        'WHERE orders > 15 '
                                        'AND Customer.custId = CustomerOrders.custId);')

        assert data[0] == (5, 'Higginbotham, Tom', 'Customer HGVLZ', 'Sweden', '0921-67 89 01')
        assert data[8] == (71, 'Navarro, Tomás', 'Customer LCOUJ', 'USA', '(208) 555-0116')