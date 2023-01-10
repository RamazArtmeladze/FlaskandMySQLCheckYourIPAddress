from flask import Flask, render_template, request
import MySQLdb as db

app = Flask(__name__)

dbconfig = {"host" : "ramaz13.mysql.pythonanywhere-services.com",
            "user" : "ramaz13",
            "password" : "python13",
            "database" : "ramaz13$newdb"}

@app.route('/', methods = ['POST', 'GET'])
def entry_page():
  return render_template('index.html')


@app.route('/myip', methods = ['POST', 'GET'])
def greeting():
    global user_name, ip_addr
    user_name = request.form['user_name']
    ip_addr = request.remote_addr
    results = f"Hello {user_name}! Your IP is {ip_addr}."
    persons_request(user_name, ip_addr)
    return render_template('myip.html', results = results)


def persons_request(user_name, ip_addr):
    connection =db.connect(**dbconfig)
    cursor = connection.cursor()
    _SQL = """INSERT INTO persons
                (fName, ip)
                VALUES
                (%s, %s)"""
    cursor.execute(_SQL,(user_name,ip_addr))
    connection.commit()
    cursor.close()
    connection.close()


@app.route('/viewlog')
def view_log():
    titles = ["id", "Date", "Name", "ip"]
    connection =db.connect(**dbconfig)
    cursor = connection.cursor()

    _SQL = "SELECT * FROM persons"
    cursor.execute(_SQL)
    contents = cursor.fetchall()

    cursor.close()
    connection.close()
    return render_template('viewlog.html', the_data=contents, the_row_titles = titles)

if __name__ == '__main__':
  app.run(debug = True)