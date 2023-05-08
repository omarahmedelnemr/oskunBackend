from flask import Flask, render_template, request
import  mysql.connector as DB


app = Flask(__name__)



@app.route('/', methods=['POST'])
def index():
        r = 'finnnn@gmail.com'
        cur = DB.cursor()
        cur.execute( ("UPDATE User SET email={} WHERE id=43;").format(r) )
        mysql.connection.commit()
        cur.close()
        return render_template('hom.html')


if __name__ == '__main__':
    app.run(port=18166)
    