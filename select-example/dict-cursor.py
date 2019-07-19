import pymysql

connection = pymysql.connect(host='localhost',
    user="admin",
    password="password",
    database="Chinook"
)

# Use the dictinary cursor
cursor = connection.cursor(pymysql.cursors.DictCursor)
cursor.execute("SELECT * from Employee")
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