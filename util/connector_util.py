from mysql.connector.cursor_cext import CMySQLCursor


class ConnectorUtil:

    def print_query(self: CMySQLCursor):
        print(f"\n{self.column_names}")
        data = self.fetchall()
        if len(data) > 0:
            print('\n'.join(str(x) for x in data))
        else:
            print('NO DATA')
        pass
