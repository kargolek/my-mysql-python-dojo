import os
import sys

from mysql.connector.cursor_cext import CMySQLCursor


def print_query_data(cursor: CMySQLCursor, query: str, data: list):
    print(f'\nSQL query: {query}')
    print(f'{cursor.column_names}')
    if len(data) > 0:
        print('\n'.join(str(x) for x in data))
    else:
        print('NO DATA')
    print(f'Size: {len(data)}')


def fetch_data_print(cursor: CMySQLCursor, query: str):
    cursor.execute(query)
    data = cursor.fetchall()
    print_query_data(cursor, query, data)
    return data


def _get_sql_file(file_name: str):
    return open(os.path.abspath(sys.path[0] + '/sql_files/' + file_name), "r")


def _get_sql_queries(file_name: str):
    sql_file = _get_sql_file(file_name)
    x = ''.join(str(line).replace("\n", "") for line in sql_file)
    queries_temp = x.split(";")
    return [query + ";" for query in queries_temp if query != '']


def execute_sql_file(cursor: CMySQLCursor, file_name: str):
    for query in _get_sql_queries(file_name):
        print(f'SQL FILE ({file_name}) QUERY: {query}')
        cursor.execute(query, multi=False)
