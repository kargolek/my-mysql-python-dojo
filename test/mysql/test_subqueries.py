from test.util.connector_util import fetch_data_print


class TestSubQueries:

    # MySQL Subquery
    def test_select_employment_age_when_hired(self, cursor):
        data = fetch_data_print(cursor, 'SELECT * FROM '
                                        '(SELECT employeeId, firstName, lastName, '
                                        'FLOOR((DATEDIFF(hireDate, birthDate) / 365)) as employmentAge '
                                        'FROM Employee '
                                        'ORDER BY employmentAge DESC) AS EmpDate;')
