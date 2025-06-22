from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def conectar():
    return sqlite3.connect('estoque.db')

def inicializar():
    conn = conectar()
    cursor = conn.cursor()

    # Tabela insumos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS insumos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            quantidade REAL NOT NULL,
            unidade TEXT NOT NULL
        )
    ''')

    # Tabela produtos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
        )
    ''')

    # Tabela vendas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto TEXT NOT NULL,
            quantidade REAL NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/cadastrar_insumo", methods=["GET", "POST"])
def cadastrar_insumo():
    if request.method == "POST":
        nome = request.form["nome"]
        quantidade = float(request.form["quantidade"])
        unidade = request.form["unidade"]

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO insumos (nome, quantidade, unidade) VALUES (?, ?, ?)",
                       (nome, quantidade, unidade))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    return render_template("cadastrar_insumo.html")

@app.route("/cadastrar_produto", methods=["GET", "POST"])
def cadastrar_produto():
    if request.method == "POST":
        nome = request.form["nome"]
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO produtos (nome) VALUES (?)", (nome,))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    return render_template("cadastrar_produto.html")

@app.route("/registrar_venda", methods=["GET", "POST"])
def registrar_venda():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome FROM produtos")
    produtos = cursor.fetchall()
    conn.close()

    if request.method == "POST":
        produto_id = int(request.form["produto_id"])
        quantidade = float(request.form["quantidade"])

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT nome FROM produtos WHERE id = ?", (produto_id,))
        produto_nome = cursor.fetchone()
        if produto_nome is None:
            conn.close()
            return "Produto não encontrado", 404
        produto_nome = produto_nome[0]

        cursor.execute("INSERT INTO vendas (produto, quantidade) VALUES (?, ?)", (produto_nome, quantidade))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))

    return render_template("registrar_venda.html", produtos=produtos)

@app.route("/visualizar_estoque")
def estoque():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM insumos")
    insumos = cursor.fetchall()
    conn.close()
    return render_template("estoque.html", insumos=insumos)

@app.route("/vendas")
def vendas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vendas")
    vendas = cursor.fetchall()
    conn.close()
    return render_template("vendas.html", vendas=vendas)

if __name__ == "__main__":
    inicializar()
    app.run(debug=True)
