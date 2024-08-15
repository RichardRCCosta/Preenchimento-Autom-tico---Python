from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3

app = Flask(__name__)

# Função para conectar ao banco de dados e garantir que a tabela exista
def get_db_connection():
    conn = sqlite3.connect('palavras.db')
    conn.row_factory = sqlite3.Row
    
    # Criar a tabela se ainda não existir
    conn.execute('''
    CREATE TABLE IF NOT EXISTS palavras (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        palavra TEXT UNIQUE NOT NULL,
        categoria TEXT NOT NULL
    )
    ''')
    
    return conn

# Rota principal para exibir o formulário
@app.route('/')
def index():
    return render_template('index.html')

# Rota para exibir a tabela de palavras
@app.route('/palavras')
def palavras():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM palavras")
    todas_palavras = cursor.fetchall()
    conn.close()
    return render_template('palavras.html', palavras=todas_palavras)

# Rota para inserir palavras no banco de dados
@app.route('/inserir_palavra', methods=['POST'])
def inserir_palavra():
    palavra = request.form['palavra']
    categoria = request.form['categoria']
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO palavras (palavra, categoria) VALUES (?, ?)", (palavra, categoria))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Ignorar palavras duplicadas

    conn.close()
    return "Palavra inserida com sucesso!", 200

# Rota para excluir uma palavra
@app.route('/excluir_palavra/<int:id>', methods=['POST'])
def excluir_palavra(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM palavras WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('palavras'))

# Rota para fornecer sugestões de autocompletar
@app.route('/sugestoes', methods=['GET'])
def sugestoes():
    termo = request.args.get('termo', '')
    categoria = request.args.get('categoria', '')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT palavra FROM palavras WHERE palavra LIKE ? AND categoria = ?", (termo + '%', categoria))
    resultados = cursor.fetchall()
    sugestoes = [row['palavra'] for row in resultados]

    conn.close()
    return jsonify(sugestoes)

if __name__ == "__main__":
    app.run(debug=True)
