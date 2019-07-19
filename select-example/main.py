import pymysql

connection = pymysql.connect(host='localhost',
    user="admin",
    password="password",
    database="Chinook"
)

cursor = connection.cursor()
cursor.execute("SELECT * from Employee")
for r in cursor:
    # print (r)
    # We have to refer each field by its index
    print ("Name: " + r[1] + " " + r[2] + " is a " + r[3])
