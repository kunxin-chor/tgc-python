import pymysql
from flask import Flask,render_template

app = Flask(__name__)

connection = pymysql.connect(host='localhost',
    user="admin",
    password="password",
    database="Chinook"
)


