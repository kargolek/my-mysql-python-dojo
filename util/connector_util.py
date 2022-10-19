from mysql.connector.cursor_cext import CMySQLCursor


class ConnectorUtil:

    def fetch_data_print(self: CMySQLCursor, query: str):
        print(f'\nSQL query: {query}')
        self.execute(query)
        print(f'{self.column_names}')
        data = self.fetchall()
        if len(data) > 0:
            print('\n'.join(str(x) for x in data))
        else:
            print('NO DATA')
        print(f'Size: {len(data)}')
        return data
