import pymysql

connection = pymysql.connect(host='localhost',
    user="admin",
    password="password",
    database="Chinook"
)

title = input("Please enter the title you want to look for: ")

sql = """SELECT * FROM Employee WHERE Title LIKE '%{}%'""".format(title)

cursor = connection.cursor(pymysql.cursors.DictCursor)
cursor.execute(sql)
for r in cursor:
    output = """
First Name: {}
Last Name: {}
Title: {}
Birthday: {}
"""
    # if using the dictionary cursor, I can refer to each field by its name
    output = output.format(r['FirstName'], r['LastName'], r['Title'], r['BirthDate'])
    print(output)

