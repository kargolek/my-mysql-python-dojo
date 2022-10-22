import datetime
from decimal import Decimal

from util.assertion_util import AssertionUtil
from util.connector_util import ConnectorUtil


class TestFilteringData:

    # MySQL WHERE Clause
    def test_should_select_product_name_by_product_id(self, cursor):
        data = ConnectorUtil.fetch_data_print(cursor, 'SELECT productName FROM Product '
                                                      'WHERE productId = 5;')

        assert data[0][0] == 'Product EPEIM'

    # MySQL WHERE Clause & AND operator
    def test_should_select_sales_orders_where_freight_above_800_and_shipper_id_is_3(self, cursor):
        data = ConnectorUtil.fetch_data_print(cursor, 'SELECT * FROM SalesOrder '
                                                      'WHERE freight > 800 '
                                                      'AND shipperId = 3;')

        assert data[0] == (10540, 63, 3, datetime.datetime(2007, 5, 19, 0, 0), datetime.datetime(2007, 6, 16, 0, 0),
                           datetime.datetime(2007, 6, 13, 0, 0), 3, Decimal('1007.64'), 'Ship to 63-C',
                           'Taucherstraße 3456', 'Cunewalde', None, '10281', 'Germany')

    # MySQL WHERE Clause & AND operator
    def test_should_select_sales_orders_where_city_munich_and_country_germany(self, cursor):
        data = ConnectorUtil.fetch_data_print(cursor, 'SELECT orderId '
                                                      'FROM SalesOrder '
                                                      'WHERE shipCountry = "Germany" '
                                                      'AND shipCity = "München";')

        assert data[0][0] == 10267
        assert data[14][0] == 11012

    # MySQL WHERE Clause OR operator
    def test_should_select_sales_orders_where_france_or_mexico_or_usa(self, cursor):
        data = ConnectorUtil.fetch_data_print(cursor, 'SELECT orderId '
                                                      'FROM SalesOrder '
                                                      'WHERE shipCountry = "France" '
                                                      'OR shipCountry = "Mexico" '
                                                      'OR shipCountry = "USA";')

        assert data[0][0] == 10248
        assert data[226][0] == 11077

    # MySQL WHERE Clause & AND operator & OR operator
    def test_should_select_sales_orders_where_city_lyon_or_reims_and_country_france(self, cursor):
        data = ConnectorUtil.fetch_data_print(cursor, 'SELECT orderId '
                                                      'FROM SalesOrder '
                                                      'WHERE shipCountry = "France" '
                                                      'AND shipCity = "Lyon" '
                                                      'OR shipCity = "Reims";')

        assert data[0][0] == 10248
        assert data[14][0] == 10850

    # MySQL DISTINCT AND WHERE NOT Clause & AND NOT operator & ORDER BY Keyword
    def test_should_select_countries_where_not_france_brazil_germany_sales_orders(self, cursor):
        data = ConnectorUtil.fetch_data_print(cursor, 'SELECT DISTINCT shipCountry '
                                                      'FROM SalesOrder '
                                                      'WHERE NOT shipCountry = "France" '
                                                      'AND NOT shipCountry = "Germany" '
                                                      'AND NOT shipCountry = "Brazil" '
                                                      'ORDER BY shipCountry ASC;')

        assert data[0][0] == 'Argentina'
        assert data[17][0] == 'Venezuela'

    # MySQL DISTINCTROW clause
    def test_should_select_distinctrow_and_concat_employee_name_surname_sales_order(self, cursor):
        data = ConnectorUtil.fetch_data_print(cursor, 'SELECT DISTINCTROW '
                                                      'CONCAT(Employee.firstname," ",Employee.lastname) AS empName '
                                                      'FROM SalesOrder '
                                                      'JOIN Employee '
                                                      'ON SalesOrder.employeeId = Employee.employeeId;')
        assert data[0][0] == 'Sven Buck'
        assert data[8][0] == 'Russell King'

    # MySQL DISTINCT clause
    def test_should_select_distinct_country_customer(self, cursor):
        data = ConnectorUtil.fetch_data_print(cursor, 'SELECT DISTINCT Country FROM Customer;')

        assert data[0][0] == 'Germany'
        assert data[20][0] == 'Poland'

    # MySQL DISTINCTROW clause
    def test_should_select_distinctrow_employee_name_surname_sales_order(self, cursor):
        data = ConnectorUtil.fetch_data_print(cursor, 'SELECT DISTINCTROW Employee.firstname, Employee.lastname '
                                                      'FROM SalesOrder '
                                                      'JOIN Employee '
                                                      'ON SalesOrder.employeeId = Employee.employeeId;')

        assert data[0] == ('Sven', 'Buck')
        assert data[8] == ('Russell', 'King')

    # MySQL IN operator
    def test_should_select_customers_from_uk_and_ireland(self, cursor):
        data = ConnectorUtil.fetch_data_print(cursor, 'SELECT contactName, phone, city, country FROM Customer '
                                                      'WHERE country IN ("UK", "Ireland");')

        assert data[0] == ('Arndt, Torsten', '(171) 456-7890', 'London', 'UK')

    # MySQL IN operator
    def test_should_select_supplier_with_title_sales(self, cursor):
        data = ConnectorUtil.fetch_data_print(cursor, 'SELECT contactName, contactTitle, phone FROM Supplier '
                                                      'WHERE contactTitle '
                                                      'IN ("Sales Representative", "Sales Agent", "Sales Manager");')

        assert data[0] == ('Parovszky, Alfons', 'Sales Representative', '(313) 555-0109')
        assert data[2] == ('Basalik, Evan', 'Sales Agent', '031-345 67 89')
        assert data[9] == ('Leoni, Alessandro', 'Sales Manager', '89.01.23.45')

    # MySQL NOT IN operator
    def test_should_select_territory_id_and_description_where_region_id_is_not_1_3(self, cursor):
        data = ConnectorUtil.fetch_data_print(cursor, 'SELECT territoryId, territorydescription FROM Territory '
                                                      'WHERE regionId '
                                                      'NOT IN (1, 3);')
        assert data[0] == ('29202', 'Columbia')
        assert data[22] == ('98104', 'Seattle')

    # MySQL BETWEEN Operator
    def test_should_select_products_unit_price_between_100_200(self, cursor):
        data = ConnectorUtil.fetch_data_print(cursor, 'SELECT productId, productName, unitPrice FROM Product '
                                                      'WHERE unitPrice '
                                                      'BETWEEN 100 AND 200;')

        assert data[0] == (29, 'Product VJXYN', Decimal('123.79'))

    # MySQL NOT BETWEEN Operator
    def test_should_select_products_unit_price_not_between_10_300(self, cursor):
        data = ConnectorUtil.fetch_data_print(cursor, 'SELECT productId, productName, unitPrice FROM Product '
                                                      'WHERE unitPrice '
                                                      'NOT BETWEEN 10 AND 300;')

        assert data[0] == (13, 'Product POXFU', Decimal('6.00'))
        assert data[10] == (75, 'Product BWRLG', Decimal('7.75'))

    # MySQL LIKE operator
    def test_should_select_customer_company_starts_on_letter_a(self, cursor):
        data = ConnectorUtil.fetch_data_print(cursor, 'SELECT custId, companyName, contactName FROM Customer '
                                                      'WHERE companyName '
                                                      'LIKE "Customer A%";')

        assert data[0] == (25, 'Customer AZJED', 'Carlson, Jason')
        assert data[1] == (58, 'Customer AHXHT', 'Fakhouri, Fadi')
        assert data[2] == (72, 'Customer AHPOP', 'Welcker, Brian')

    # MySQL NOT LIKE operator
    def test_should_select_customer_company_starts_on_lette(self, cursor):
        data = ConnectorUtil.fetch_data_print(cursor, 'SELECT custId, companyName, contactName FROM Customer '
                                                      'WHERE companyName '
                                                      'NOT LIKE "Customer A%";')

        assert data[0] == (1, 'Customer NRZBB', 'Allen, Michael')
        assert AssertionUtil.is_data_contains_element(data, (25, 'Customer AZJED', 'Carlson, Jason')) is False
