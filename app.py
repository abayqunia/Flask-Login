from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL, MySQLdb
import bcrypt

app = Flask(__name__)
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'meja1234'
app.config['MYSQL_DB'] = 'tugas1'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = curl.fetchone()
        curl.close()

        if len(user) > 0:
            if bcrypt.hashpw(password, user["password"].encode('utf-8')) == user["password"].encode('utf-8'):
                session['name'] = user['name']
                session['email'] = user['email']
                return render_template("home.html")
            else:
                return "Error password and email not match"
        else:
            return "Error user not found"
    else:
        return render_template("login.html")


@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.clear()
    return render_template("home.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, email, password) VALUES (%s,%s,%s)",
                    (name, email, hash_password,))
        mysql.connection.commit()
        session['name'] = request.form['name']
        session['email'] = request.form['email']
        return redirect(url_for('home'))

# service
@app.route('/jasa_service')
def service():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM jasa")
    rv = cur.fetchall()
    cur.close()
    return render_template('jasa.html', services=rv)

@app.route('/simpan-service', methods=["POST"])
def saveService():
    nama = request.form['nama']
    harga = request.form['harga']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO jasa (nama, harga) VALUES (%s, %s)", (nama, harga))
    mysql.connection.commit()
    return redirect(url_for('service'))


@app.route('/update-service', methods=["POST"])
def updateService():
    id_data = request.form['id']
    nama = request.form['nama']
    harga = request.form['harga']
    cur = mysql.connection.cursor()
    cur.execute("UPDATE jasa SET nama=%s, harga=%s WHERE Id=%s", (nama,harga,id_data,))
    mysql.connection.commit()
    return redirect(url_for('service'))

@app.route('/hapus-service/<string:id_data>', methods=["GET"])
def hapusService(id_data):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM jasa WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('service'))
# end service

# Sparepart
@app.route('/sparepart')
def sparepart():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM spare")
    rv = cur.fetchall()
    cur.close()
    return render_template('spare.html', spareparts=rv)

@app.route('/simpan-sparepart', methods=["POST"])
def saveSparepart():
    nama = request.form['nama']
    harga = request.form['harga']
    stok = request.form['stok']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO spare (nama, harga, stok) VALUES (%s, %s, %s)", (nama, harga, stok))
    mysql.connection.commit()
    return redirect(url_for('sparepart'))


@app.route('/update-sparepart', methods=["POST"])
def updateSparepart():
    id_data = request.form['id']
    nama = request.form['nama']
    harga = request.form['harga']
    stok = request.form['stok']
    cur = mysql.connection.cursor()
    cur.execute("UPDATE spare SET nama=%s, harga=%s, stok=%s WHERE Id=%s", (nama,harga,stok,id_data,))
    mysql.connection.commit()
    return redirect(url_for('sparepart'))

@app.route('/hapus-sparepart/<string:id_data>', methods=["GET"])
def hapusSparepart(id_data):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM spare WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('sparepart'))
# end Sparepart

# Acsesoris
@app.route('/acsesoris')
def acsesoris():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM aksesoris")
    rv = cur.fetchall()
    cur.close()
    return render_template('aksesoris.html', acsesorises=rv)

@app.route('/simpan-acsesoris', methods=["POST"])
def saveAcsesoris():
    nama = request.form['nama']
    harga = request.form['harga']
    stok = request.form['stok']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO aksesoris (nama, harga, stok) VALUES (%s, %s, %s)", (nama, harga, stok))
    mysql.connection.commit()
    return redirect(url_for('acsesoris'))


@app.route('/update-acsesoris', methods=["POST"])
def updateAcsesoris():
    id_data = request.form['id']
    nama = request.form['nama']
    harga = request.form['harga']
    stok = request.form['stok']
    cur = mysql.connection.cursor()
    cur.execute("UPDATE aksesoris SET nama=%s, harga=%s, stok=%s WHERE Id=%s", (nama,harga,stok,id_data,))
    mysql.connection.commit()
    return redirect(url_for('acsesoris'))

@app.route('/hapus-acsesoris/<string:id_data>', methods=["GET"])
def hapusAcsesoris(id_data):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM aksesoris WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('acsesoris'))
# end Acsessoris

# User
@app.route('/management_user')
def user():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM management_user")
    rv = cur.fetchall()
    cur.close()
    return render_template('management_user.html', users=rv)

@app.route('/simpan-management_user', methods=["POST"])
def saveUser():
    nama = request.form['nama']
    password1 = request.form['password']
    status = request.form['status']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO management_user (name, password, status) VALUES (%s, %s, %s)", (nama, password, status))
    mysql.connection.commit()
    return redirect(url_for('management_user'))


@app.route('/update-management_user', methods=["POST"])
def updateUser():
    nama = request.form['nama']
    password = request.form['password']
    status = request.form['status']
    cur = mysql.connection.cursor()
    cur = mysql.connection.cursor()
    cur.execute("UPDATE management_user SET name=%s, password=%s, status=%s WHERE Id=%s", (nama, password, status, id_data,))
    mysql.connection.commit()
    return redirect(url_for('management_user'))

@app.route('/hapus-management_user/<string:id_data>', methods=["GET"])
def hapusUser(id_data):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM management_user WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('management_user'))
# end Use


if __name__ == '__main__':
    app.secret_key = "^A%DJAJU^JJ123"
    app.run(debug=True)