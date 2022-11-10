from decimal import Decimal

from test.util.connector_util import fetch_data_print


class TestSubQueries:

    # MySQL Subquery
    def test_select_employment_age_when_hired(self, cursor):
        data = fetch_data_print(cursor, 'SELECT * FROM '
                                        '   (SELECT employeeId, firstName, lastName, '
                                        '   FLOOR((DATEDIFF(hireDate, birthDate) / 365)) AS employmentAge '
                                        '   FROM Employee '
                                        'ORDER BY employmentAge DESC) AS EmpDate;')

        assert data[0] == (4, 'Yael', 'Peled', 55)
        assert data[8] == (9, 'Zoya', 'Dolgopyatova', 28)

    # MySQL Subquery
    def test_select_employment_max_min_avg_age_when_hired(self, cursor):
        data = fetch_data_print(cursor, 'SELECT MAX(employmentAge) AS maxAge, '
                                        'MIN(employmentAge) AS minAge,'
                                        'AVG(employmentAge) FROM '
                                        '   (SELECT employeeId, firstName, lastName, '
                                        '   FLOOR((DATEDIFF(hireDate, birthDate) / 365)) AS employmentAge '
                                        '   FROM Employee '
                                        'ORDER BY employmentAge DESC) AS EmpDate;')

        assert data[0] == (55, 28, Decimal('36.7778'))

    # MySQL Subquery
    def test_select_product_where_price_bigger_than_avg_order_price(self, cursor):
        data = fetch_data_print(cursor, 'SELECT productId, productName, unitPrice FROM Product '
                                        'WHERE unitPrice > '
                                        '   (SELECT AVG(unitPrice) FROM OrderDetail);')

        assert data[0] == (7, 'Product HMLNI', Decimal('30.00'))
        assert data[25] == (72, 'Product GEEOO', Decimal('34.80'))

    # MySQL Subquery
    def test_select_customer_who_order_more_than_15_orders(self, cursor):
        data = fetch_data_print(cursor, 'SELECT custId, contactName, companyName, country, phone '
                                        'FROM Customer '
                                        'WHERE EXISTS( SELECT custId FROM '
                                        '   (SELECT custId, COUNT(*) AS orders FROM SalesOrder '
                                        '   GROUP BY custId) AS CustomerOrders '
                                        'WHERE orders > 15 '
                                        'AND Customer.custId = CustomerOrders.custId);')

        assert data[0] == (5, 'Higginbotham, Tom', 'Customer HGVLZ', 'Sweden', '0921-67 89 01')
        assert data[8] == (71, 'Navarro, Tomás', 'Customer LCOUJ', 'USA', '(208) 555-0116')

    # MySQL Subquery
    def test_select_employees_who_sell_most_products(self, cursor):
        data = fetch_data_print(cursor, 'SELECT employeeId, firstName, lastName, ordersQuantity, totalPrice FROM '
                                        '   (SELECT employeeId, '
                                        '   SUM(quantity) AS ordersQuantity, '
                                        '   SUM(unitPrice * quantity) AS totalPrice '
                                        '   FROM OrderDetail '
                                        '   INNER JOIN SalesOrder USING (orderId) '
                                        '   INNER JOIN Employee USING (employeeId) '
                                        '   GROUP BY employeeId) AS empQuantity '
                                        'INNER JOIN Employee USING (employeeId) '
                                        'ORDER BY ordersQuantity DESC;')

        assert data[0] == (4, 'Yael', 'Peled', Decimal('9798'), Decimal('250187.45'))
        assert data[8] == (9, 'Zoya', 'Dolgopyatova', Decimal('2670'), Decimal('82964.00'))

    # MySQL Subquery
    def test_select_employees_who_sell_most_products_having_more_than_200000(self, cursor):
        data = fetch_data_print(cursor, 'SELECT employeeId, firstName, lastName, ordersQuantity, totalPrice FROM '
                                        '   (SELECT employeeId, '
                                        '   SUM(quantity) AS ordersQuantity, '
                                        '   SUM(unitPrice * quantity) AS totalPrice '
                                        '   FROM OrderDetail '
                                        '   INNER JOIN SalesOrder USING (orderId) '
                                        '   INNER JOIN Employee USING (employeeId) '
                                        '   GROUP BY employeeId'
                                        '   HAVING totalPrice > 200000) AS empQuantity '
                                        'INNER JOIN Employee USING (employeeId) '
                                        'ORDER BY ordersQuantity DESC;')

        assert data[0] == (4, 'Yael', 'Peled', Decimal('9798'), Decimal('250187.45'))
        assert data[2] == (1, 'Sara', 'Davis', Decimal('7812'), Decimal('202143.71'))

    # MySQL Subquery
    def test_should_count_total_orders_and_price_per_year_per_product_with_rollup(self, cursor):
        data = fetch_data_print(cursor, 'SELECT IF(GROUPING(productName), "All products", productName) AS product, '
                                        'IF(GROUPING(year), "All years", year) AS year, '
                                        'SUM(totalOrders) AS totalOrders, '
                                        'SUM(totalPrice) AS totalPrice '
                                        'FROM '
                                        '   (SELECT productName, YEAR(orderDate) AS year, '
                                        '   COUNT(*) AS totalOrders, '
                                        '   SUM(OrderDetail.unitPrice * quantity) AS totalPrice FROM OrderDetail '
                                        '   INNER JOIN Product USING (productId) '
                                        '   INNER JOIN SalesOrder USING (orderId) '
                                        '   GROUP BY productName, year) AS TotalSales '
                                        'GROUP BY productName, year WITH ROLLUP;')

        assert data[0] == ('Product ACRVI', '2006', Decimal('4'), Decimal('1643.00'))
        assert data[3] == ('Product ACRVI', 'All years', Decimal('18'), Decimal('6664.75'))
        assert data[303] == ('Product ZZZHR', 'All years', Decimal('28'), Decimal('25079.20'))
        assert data[304] == ('All products', 'All years', Decimal('2155'), Decimal('1354458.59'))
