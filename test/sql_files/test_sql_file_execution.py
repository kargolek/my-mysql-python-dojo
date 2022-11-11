import pytest
from mysql.connector import ProgrammingError

from test.util.connector_util import execute_sql_file, fetch_data_print


class TestSqlFileExecution:

    def test_should_execute_file_wout_error_data_should_match(self, cursor, drop_example_test_table):
        execute_sql_file(cursor, "sample.sql")
        data = fetch_data_print(cursor, 'SELECT * FROM ExampleTable')

        assert data[0] == (1, 'TestName', b'TestDescription')

    def test_should_throw_programming_error_for_bad_sql_syntax(self, cursor, drop_example_test_table):
        with pytest.raises(ProgrammingError):
            execute_sql_file(cursor, "sample_error_syntax.sql")

