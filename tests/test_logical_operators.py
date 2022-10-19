import datetime
from decimal import Decimal

from util.connector_util import ConnectorUtil


class TestSelectAndOperators:

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

    # MySQL WHERE NOT Clause & AND NOT operator & ORDER BY Keyword
    def test_should_select_countries_where_not_france_brazil_germany_sales_orders(self, cursor):
        data = ConnectorUtil.fetch_data_print(cursor, 'SELECT DISTINCT shipCountry '
                                                      'FROM SalesOrder '
                                                      'WHERE NOT shipCountry = "France" '
                                                      'AND NOT shipCountry = "Germany" '
                                                      'AND NOT shipCountry = "Brazil" '
                                                      'ORDER BY shipCountry ASC;')

        assert data[0][0] == 'Argentina'
        assert data[17][0] == 'Venezuela'
