
from flask import Flask, render_template, request
import pyodbc
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import redis
import hashlib
import time
import pickle


app = Flask(__name__)

driver = '{ODBC Driver 17 for SQL Server}'
database = 'assignment1'
server = 'SERVERNAME'
username = "USERNAME"
password = "PASSWORD"


conn=pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password) 
cursor=conn.cursor()

r = redis.Redis(host='rxg3512.redis.cache.windows.net',
                port=6380, db=0, password='oMtf0mmcsPhDcuNDOFbyRcJfBnMdMue5yAzCaMQPgeQ=',ssl=True)

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/q6')
def q5():
   return render_template('q6.html')


# With using Redis
@app.route('/redis', methods=['POST','GET'])
def redismag():
    
    m1=request.form['m1']
    m2=request.form['m2']
    querry1="Select  *  from all_month WHERE mag  between '"+m1+"' and '"+m2+"'"
    hash = hashlib.sha224(querry1.encode('utf-8')).hexdigest()
    key = "redis_cache:" + hash
    t1 = time.time()
    for i in range(1,500):
        if(r.get(key)):
            pass
        else:
            cursor.execute(querry1)
            data = cursor.fetchall()
            r.set(key, pickle.dumps(data))
            
            r.expire(key,36)
    t2 = time.time()
    total=t2-t1
    
    return render_template("opt.html",time = total)

# without using redis
@app.route('/withoutredis', methods=['POST','GET'])
def withoutredis():
    
    m1=request.form['m1']
    m2=request.form['m2']
    querry1="Select  *  from all_month WHERE mag  between '"+m1+"' and '"+m2+"'"
    t1 = time.time()
    for i in range(1,500):
        cursor.execute(querry1)
        data = cursor.fetchall()
    t2 = time.time()
    total=t2-t1
    
    return render_template("opt.html",time = total)




if __name__ == '__main__':
    app.run(debug=True)
