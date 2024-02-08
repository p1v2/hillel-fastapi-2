text = open('test.txt').readlines()

sql_query = "insert into products (name, price) values "

for line in text:
    sql_query += f"('{line.strip()}', 100),"

open('test.txt', 'w').write(sql_query)
