from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'biblioteca'
app.config['MYSQL_HOST'] = 'localhost'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_book', methods=['POST'])
def add_book():
    titulo = request.form['titulo']
    autor = request.form['autor']
    genero = request.form['genero']
    editora = request.form['editora']
    ano = request.form['ano']
    quantidade = request.form['quantidade']

    cursor = mysql.connection.cursor()
    cursor.execute('INSERT INTO livros (titulo, autor, genero, editora, ano, quantidade) VALUES (%s, %s, %s, %s, %s, %s)', (titulo, autor, genero, editora, ano, quantidade))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('index'))

@app.route('/search_books', methods=['GET'])
def search_books():
    query = request.args.get('query')
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM livros WHERE titulo LIKE %s OR autor LIKE %s", ('%' + query + '%', '%' + query + '%'))
    result = cursor.fetchall()
    cursor.close()
    return jsonify(result)

@app.route('/edit_book/<int:id>', methods=['POST'])
def edit_book(id):
    quantidade = request.form['quantidade']
    cursor = mysql.connection.cursor()
    cursor.execute('UPDATE livros SET quantidade = %s WHERE id = %s', (quantidade, id))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('all_books'))

@app.route('/delete_book/<int:id>', methods=['POST'])
def delete_book(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM livros WHERE id = %s', (id,))
    mysql.connection.commit()
    cursor.execute('SET @num := 0')
    cursor.execute('UPDATE livros SET id = @num := (@num+1)')
    cursor.execute('ALTER TABLE livros AUTO_INCREMENT = 1')
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('all_books'))

@app.route('/all_books')
def all_books():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM livros")
    livros = cursor.fetchall()
    cursor.close()
    return render_template('all_books.html', livros=livros)

if __name__ == '__main__':
    app.run(debug=True)
