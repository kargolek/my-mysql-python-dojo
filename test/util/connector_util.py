def print_query_data(cursor, query: str, data: list):
    print(f'\nSQL query: {query}')
    print(f'{cursor.column_names}')
    if len(data) > 0:
        print('\n'.join(str(x) for x in data))
    else:
        print('NO DATA')
    print(f'Size: {len(data)}')


def fetch_data_print(cursor, query: str):
    cursor.execute(query)
    data = cursor.fetchall()
    print_query_data(cursor, query, data)
    return data
