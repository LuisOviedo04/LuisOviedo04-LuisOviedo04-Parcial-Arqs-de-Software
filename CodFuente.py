from flask import Flask,render_template,request
from flask_mysqldb import MySQL
import json
import redis

class Adapter:
    def __init__(self, temp, tiempo):
        self.Temperature = temp
        self.Time = tiempo

    def convert(self):
        Dictionary = {'Temperature': self.Temperature, 'Time': self.tiempo}
        JSON = json.dumps(Dictionary)
        return JSON


class SQL:
    def __init__(self, cursor, json, mysql):
        self.cur = cursor
        self.Json = json
        self.MySQL = mysql

    def Create_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS info ( info JSON NOT NULL )")
    
    def Insert_data(self):
        self.cursor.execute("INSERT INTO info  VALUES (%s)",(self.Json,) )
        self.mysql.connection.commit()
        self.cursor.close()

class Redis:
    def __init__(self, host, jfile):
        self.Host = host
        self.JsonFile = jfile

    def Insert_data(self):
        r_server = redis.Redis(self.Host)
        r_server.incr("index", 1) 
        index = r_server.get("index").decode("utf-8")
        key = int(index)
        new_d = json.loads(self.JsonFile)
        r_server.hmset(key,new_d)

def app():

    app = Flask(__name__,instance_relative_config=True)
    app.config['MYSQL_HOST'] = 'ContainerSQL'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'oviedo'
    app.config['MYSQL_DB'] = 'mysql'
    mysql = MySQL(app)

    @app.route('/', methods=["GET","POST"])
    def main():
        
        if(request.method == 'POST'):
            temperature = request.form['temperature']
            time = request.form['time']
            
            if(temperature and time):                
                SQLDataBase = Adapter(temperature , time)
                Json = SQLDataBase.convert()

                ConexSQLDB = SQL(mysql.connection.cursor(), Json  ,mysql)
                ConexSQLDB.Create_table()
                ConexSQLDB.Insert_data()

                ConexRedis = Redis("redis", Json)
                ConexRedis.Insert_data()
        return render_template("input.html")

    @app.route("/iot", methods=['GET', 'POST'])
    def iot():
        ata = request.get_json()
        if(request.method=='POST' and ata):
            data = json.dumps(ata)

            conecSQL = ConexionSQL( mysql.connection.cursor(), data  ,mysql )
            conecSQL.Create_table()
            conecSQL.Insert_data()

            conecRedis = ConexionRedis("redis",data)
            conecRedis.Insert_data()
            return data    
    
    return app