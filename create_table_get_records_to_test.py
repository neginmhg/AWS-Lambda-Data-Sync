import pymysql


DATABASE_HOST = 'db4free.net'
DATABASE_USER = 'test_user_rabin'
DATABASE_PASSWORD = ''
DATABASE_NAME = 'test_db_rabin'
CREATE_TABLE = True

connection = pymysql.connect(host=DATABASE_HOST, user=DATABASE_USER, passwd=DATABASE_PASSWORD, db=DATABASE_NAME)

create_table_sql_script = f"""
CREATE TABLE IF NOT EXISTS product_sale_summary(
  product_name varchar(255),
  quantity int,
  amount double,
  revenue double,
  file_name varchar(255)
  );
"""

# Create table only if CREATE_TABLE flag is true
if CREATE_TABLE:
    print('-' * 102)
    print('Creating table')

    with connection.cursor() as cursor:
        cursor.execute(create_table_sql_script)

    print('Table Created')
    print('-' * 102)

# Select record from database to validate
print('Getting records from the table')

with connection.cursor() as cursor:
    cursor.execute("SELECT * FROM product_sale_summary;")
    result = cursor.fetchall()

for row in result:
    print(row)

print('-' * 102)
