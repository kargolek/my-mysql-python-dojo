from decimal import Decimal

from test.util.connector_util import fetch_data_print


class TestAggregateData:

    # MySQL GROUP BY clause
    def test_should_select_customer_countries_and_group_them(self, cursor):
        data = fetch_data_print(cursor, 'SELECT country FROM Customer '
                                        'GROUP BY country;')

        assert data[20][0] == 'Poland'
        assert len(data) == 21

    # MySQL GROUP BY clause
    def test_should_select_grouped_employee_titles(self, cursor):
        data = fetch_data_print(cursor, 'SELECT title FROM Employee '
                                        'GROUP BY title;')

        assert data[0][0] == 'CEO'
        assert data[1][0] == 'Vice President, Sales'
        assert data[2][0] == 'Sales Manager'
        assert data[3][0] == 'Sales Representative'

    # MySQL GROUP BY clause and COUNT() aggregate function
    def test_should_count_customer_countries_occurrence(self, cursor):
        data = fetch_data_print(cursor, 'SELECT country, COUNT(*) AS occurrence FROM Customer '
                                        'GROUP BY country '
                                        'ORDER BY occurrence DESC, country DESC;')

        assert data[0] == ('USA', 13)
        assert data[1] == ('Germany', 11)
        assert data[20] == ('Ireland', 1)

    # MySQL GROUP BY clause and COUNT() aggregate function
    def test_should_count_products_in_order_details(self, cursor):
        data = fetch_data_print(cursor, 'SELECT Product.productName, COUNT(*) AS occurrence FROM OrderDetail '
                                        'JOIN Product '
                                        'ON Product.productId = OrderDetail.productId '
                                        'GROUP BY Product.productName '
                                        'ORDER BY occurrence DESC, productName DESC;')

        assert data[0] == ('Product UKXRI', 54)
        assert data[76] == ('Product AOZBW', 5)

    # MySQL aggregate function – AVG() function
    def test_should_count_average_products_price_order_details(self, cursor):
        data = fetch_data_print(cursor, 'SELECT productName, AVG(OrderDetail.unitPrice) AS avgPrice FROM OrderDetail '
                                        'JOIN Product '
                                        'Product USING (productId) '
                                        'GROUP BY productName '
                                        'ORDER BY avgPrice DESC, productName DESC;')

        assert data[0] == ('Product QDOMO', Decimal('245.933333'))
        assert data[76] == ('Product ASTMN', Decimal('2.328125'))

    # MySQL aggregate function – AVG() function
    def test_should_count_average_discount_per_product_in_order_details(self, cursor):
        data = fetch_data_print(cursor,
                                'SELECT productName, AVG(OrderDetail.discount) AS avgDiscount FROM OrderDetail '
                                'JOIN Product '
                                'Product USING (productId) '
                                'GROUP BY productName '
                                'ORDER BY avgDiscount DESC, productName DESC;')

        assert data[0] == ('Product MYNXN', Decimal('0.108333'))
        assert data[76] == ('Product IMEHJ', Decimal('0.016667'))

    # MySQL aggregate function – SUM() function
    def test_should_select_total_orders_price_in_order_detail_by_each_product(self, cursor):
        data = fetch_data_print(cursor, 'SELECT productName, '
                                        'SUM(OrderDetail.unitPrice * OrderDetail.quantity) AS totalPrice '
                                        'FROM OrderDetail '
                                        'JOIN Product '
                                        'Product USING (productId) '
                                        'GROUP BY productName '
                                        'ORDER BY totalPrice DESC, productName DESC;')

        assert data[0] == ('Product QDOMO', Decimal('149984.20'))
        assert data[76] == ('Product MYNXN', Decimal('1542.75'))

    # MySQL aggregate function – SUM() function
    def test_should_select_sum_of_quantity_by_each_product(self, cursor):
        data = fetch_data_print(cursor, 'SELECT productName, '
                                        'SUM(OrderDetail.quantity) AS totalQuantity '
                                        'FROM OrderDetail '
                                        'JOIN Product '
                                        'Product USING (productId) '
                                        'GROUP BY productName '
                                        'ORDER BY totalQuantity DESC, productName DESC;')

        assert data[0] == ('Product WHBYK', Decimal('1577'))
        assert data[76] == ('Product AOZBW', Decimal('95'))

    # MySQL aggregate function – MIN() function
    def test_should_select_lowest_product_price(self, cursor):
        data = fetch_data_print(cursor, 'SELECT MIN(unitPrice) AS lowestPrice '
                                        'FROM Product;')

        assert data[0][0] == Decimal('2.5')

    # MySQL aggregate function – MAX() function
    def test_should_select_highest_product_price(self, cursor):
        data = fetch_data_print(cursor, 'SELECT MAX(unitPrice) AS highestPrice '
                                        'FROM Product;')

        assert data[0][0] == Decimal('263.50')

    # MySQL aggregate function – MAX() function
    def test_should_select_order_id_with_max_freight(self, cursor):
        data = fetch_data_print(cursor, 'SELECT orderId, MAX(freight) '
                                        'FROM SalesOrder '
                                        'GROUP BY orderId;')

        assert data[0] == (10248, Decimal('32.38'))
        assert data[829] == (11077, Decimal('8.53'))

    # MySQL aggregate function – MIN() function
    def test_should_select_order_id_with_min_freight(self, cursor):
        data = fetch_data_print(cursor, 'SELECT orderId, MIN(freight) '
                                        'FROM SalesOrder '
                                        'GROUP BY orderId;')

        assert data[0] == (10248, Decimal('32.38'))
        assert data[829] == (11077, Decimal('8.53'))


