import constants
import pymysql
import os


print("Getting Values from environment variable")
try:
    DATABASE_HOST = os.environ['DATABASE_HOST']
    DATABASE_USER = os.environ['DATABASE_USER']
    DATABASE_PASSWORD = os.environ['DATABASE_PASSWORD']
    DATABASE_NAME = os.environ['DATABASE_NAME']
except Exception as error:
    print("Exception occurred while getting environment variable")
    print(error)


def summarize_transaction(transaction_data, file_name):
    summary_data = {}
    record_count = 0
    transaction_items = transaction_data.strip().split('\n')
    for transaction in transaction_items:
        record_count = record_count + 1
        product_name, quantity, amount, revenue = transaction.split(',')
        if product_name in summary_data.keys():
            current_quantity, current_amount, current_revenue = summary_data.get(product_name)
            summary_data[product_name] = current_quantity + int(quantity), current_amount + float(amount), \
                                         current_revenue + float(revenue)
        else:
            summary_data[product_name] = int(quantity), float(amount), float(revenue)

    # Store data as [('egg', 5, 100, 10, 'my_file'), ('apple', 1, 200, 20, 'my_file')]
    summary_list = [(key, *value, file_name) for key, value in summary_data.items()]

    return summary_list, record_count


def generate_sql_query(transaction_list):
    print("Generating SQL query")
    column_names = constants.RDS_COLUMN_HEADERS
    data = str(transaction_list).strip('[]')
    sql_query = f'INSERT INTO {constants.TABLE_NAME}({column_names}) VALUES {data};'
    return sql_query


def insert_to_rds(summarized_transaction):
    sql_query = generate_sql_query(summarized_transaction)
    print("Obtaining database connection")
    connection = pymysql.connect(host=DATABASE_HOST, user=DATABASE_USER, passwd=DATABASE_PASSWORD, db=DATABASE_NAME)

    with connection.cursor() as cursor:
        print("Executing SQL query")
        cursor.execute(sql_query)
    connection.commit()
