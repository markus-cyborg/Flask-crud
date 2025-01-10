from flask import Flask, render_template, request, redirect, url_for
from mysql import connector

app = Flask(__name__)

# Open connection
db = connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="db_kuliah"
)

if db.is_connected():
    print('Connection successful')

@app.route('/')
def halaman_awal():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM mahasiswa")  # Menggunakan nama tabel mahasiswa
    res = cursor.fetchall()  # Memperbaiki kesalahan penulisan
    cursor.close()
    return render_template('index.html', hasil=res)

@app.route('/tambah/')
def tambah_data():
    return render_template('tambah.html')

@app.route('/proses_tambah/', methods=['POST'])
def proses_tambah():
    nim = request.form['nim']
    nama = request.form['nama']
    asal = request.form['asal']
    cur = db.cursor()
    cur.execute('INSERT INTO mahasiswa (nim, nama, asal) VALUES (%s, %s, %s)', (nim, nama, asal))
    db.commit()
    return redirect(url_for('halaman_awal'))

@app.route('/ubah/<nim>', methods=['GET'])
def ubah_data(nim):
    cur = db.cursor()
    cur.execute('SELECT * FROM mahasiswa WHERE nim=%s', (nim,))
    res = cur.fetchall()  # Memperbaiki kesalahan penulisan
    cur.close()
    return render_template('ubah.html', hasil=res)

@app.route('/proses_ubah/', methods=['POST'])
def proses_ubah():
    nim_ori = request.form['nim_ori']
    nim = request.form['nim']
    nama = request.form['nama']
    asal = request.form['asal']
    cur = db.cursor()
    sql = "UPDATE mahasiswa SET nim=%s, nama=%s, asal=%s WHERE nim=%s"
    value = (nim, nama, asal, nim_ori)
    cur.execute(sql, value)
    db.commit()
    return redirect(url_for('halaman_awal'))

@app.route('/hapus/<nim>', methods=['GET'])
def hapus_data(nim):
    cur = db.cursor()
    cur.execute('DELETE FROM mahasiswa WHERE nim=%s', (nim,))
    db.commit()
    return redirect(url_for('halaman_awal'))

if __name__ == "__main__":
    app.run(debug=True)
