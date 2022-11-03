from util.connector_util import fetch_data_print


class TestGroupingData:

    # MySQL GROUP BY clause
    def test_should_select_employee_lastname_buck_from_sales_order(self, cursor):
        data = fetch_data_print(cursor, 'SELECT lastName, firstName FROM SalesOrder '
                                        'JOIN Employee '
                                        'Employee USING (employeeId) '
                                        'WHERE lastName = "Buck" '
                                        'GROUP BY employeeId;')

        assert data[0] == ('Buck', 'Sven')