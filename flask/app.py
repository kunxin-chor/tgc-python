from flask import Flask, render_template, request
import os
import pymysql

connection = pymysql.connect(
    host='localhost', # IP address of the database; localhost means "the local machine"
    user="admin",  #the mysql user
    password="password", #the password for the user
    database="Chinook" #the name of database we want to use
)

app = Flask(__name__)


@app.route('/')
def index():
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM Employee"
    cursor.execute(sql)
    # store results in a list
    results = []
    for r in cursor:
        results.append(r)
   
    return render_template('index.html', 
    data=results)

# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)