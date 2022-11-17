from test.util.connector_util import fetch_data_print


class TestJoinTables:

    # MYSQL Cartesian or CROSS JOIN
    def test_should_select_columns_to_one_where_employee_id_lower_than_3(self, cursor):
        data = fetch_data_print(cursor, 'SELECT employeeId, lastname, firstname, regionId, regiondescription '
                                        'FROM Employee, Region '
                                        'WHERE employeeId < 3')

        assert data == [(1, 'Davis', 'Sara', 4, 'Southern'),
                        (1, 'Davis', 'Sara', 3, 'Northern'),
                        (1, 'Davis', 'Sara', 2, 'Western'),
                        (1, 'Davis', 'Sara', 1, 'Eastern'),
                        (2, 'Funk', 'Don', 4, 'Southern'),
                        (2, 'Funk', 'Don', 3, 'Northern'),
                        (2, 'Funk', 'Don', 2, 'Western'),
                        (2, 'Funk', 'Don', 1, 'Eastern')]

    # MYSQL Cartesian or CROSS JOIN (the same query as above)
    def test_should_select_columns_to_one_where_employee_id_lower_than_3_cross_join(self, cursor):
        data = fetch_data_print(cursor, 'SELECT employeeId, lastname, firstname, regionId, regiondescription '
                                        'FROM Employee '
                                        'CROSS JOIN Region '
                                        'WHERE employeeId < 3')

        assert data == [(1, 'Davis', 'Sara', 4, 'Southern'),
                        (1, 'Davis', 'Sara', 3, 'Northern'),
                        (1, 'Davis', 'Sara', 2, 'Western'),
                        (1, 'Davis', 'Sara', 1, 'Eastern'),
                        (2, 'Funk', 'Don', 4, 'Southern'),
                        (2, 'Funk', 'Don', 3, 'Northern'),
                        (2, 'Funk', 'Don', 2, 'Western'),
                        (2, 'Funk', 'Don', 1, 'Eastern')]

    # MYSQL Cartesian or CROSS JOIN (it works as INNER JOIN if we add WHERE clause)
    def test_should_select_columns_and_join_territory_region_tables(self, cursor):
        data = fetch_data_print(cursor, 'SELECT territoryId, territorydescription, regiondescription '
                                        'FROM Territory '
                                        'CROSS JOIN Region '
                                        'WHERE Territory.regionId = Region.regionId;')

        assert data[0] == ('01581', 'Westboro', 'Eastern')
        assert data[7] == ('03049', 'Hollis', 'Northern')
        assert data[52] == ('98104', 'Seattle', 'Western')

    # MYSQL INNER JOIN
    def test_should_inner_join_employee_staff_committee_tables(self, cursor, staff_committee_fixture):
        data = fetch_data_print(cursor, 'SELECT employeeId, Employee.lastname, '
                                        '   StaffCommittee.committeeId, StaffCommittee.lastname '
                                        'FROM Employee '
                                        'INNER JOIN StaffCommittee;')

        assert data[0] == (1, 'Davis', 3, 'King')
        assert data[1] == (1, 'Davis', 2, 'Buck')
        assert data[2] == (1, 'Davis', 1, 'Lew')
        assert len(data) == 27

    # MYSQL INNER JOIN
    def test_should_inner_join_emp_staff_com_tables_on_the_same_lastname(self,
                                                                         cursor,
                                                                         staff_committee_fixture):
        data = fetch_data_print(cursor, 'SELECT employeeId, Employee.lastname, '
                                        '   committeeId, StaffCommittee.lastname '
                                        'FROM Employee '
                                        'INNER JOIN StaffCommittee '
                                        'ON Employee.lastname = StaffCommittee.lastname;')

        assert data[0] == (3, 'Lew', 1, 'Lew')
        assert data[1] == (5, 'Buck', 2, 'Buck')
        assert data[2] == (7, 'King', 3, 'King')
        assert len(data) == 3

    # MYSQL INNER JOIN (the same as above, but with USING clause, because columns names are the same)
    def test_should_inner_join_emp_staff_com_tables_on_the_same_lastname_with_using(self,
                                                                                    cursor,
                                                                                    staff_committee_fixture):
        data = fetch_data_print(cursor, 'SELECT employeeId, Employee.lastname, '
                                        '   committeeId, StaffCommittee.lastname '
                                        'FROM Employee '
                                        'INNER JOIN StaffCommittee USING (lastname);')

        assert data[0] == (3, 'Lew', 1, 'Lew')
        assert data[1] == (5, 'Buck', 2, 'Buck')
        assert data[2] == (7, 'King', 3, 'King')
        assert len(data) == 3
