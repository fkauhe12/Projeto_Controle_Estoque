from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

def conectar():
    return sqlite3.connect('estoque.db')

def inicializar():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            tamanho TEXT NOT NULL,
            materia_prima_por_unidade REAL NOT NULL
        )
    ''')


    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id INTEGER,
            quantidade_vendida INTEGER,
            data TEXT,
            FOREIGN KEY (produto_id) REFERENCES produtos(id)
        )
    ''')

    conn.commit()
    conn.close()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/cadastrar_produto", methods=["GET", "POST"])
def cadastrar_produto():
    if request.method == "POST":
        nome = request.form["nome"]
        tamanho = request.form["tamanho"]
        materia = float(request.form["materia"])

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO produtos (nome, tamanho, materia_prima_por_unidade) VALUES (?, ?, ?)",
            (nome, tamanho, materia)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("index"))

    return render_template("cadastrar_produto.html")

@app.route("/registrar_venda", methods=["GET", "POST"])
def registrar_venda():
    conn = conectar()
    cursor = conn.cursor()

    # Buscar id, nome e tamanho dos produtos para o select
    cursor.execute("SELECT id, nome, tamanho FROM produtos")
    produtos = cursor.fetchall()

    if request.method == "POST":
        produto_id = int(request.form["produto_id"])
        quantidade = int(request.form["quantidade"])
        data_venda = datetime.now().strftime("%Y-%m-%d")

        cursor.execute(
            "INSERT INTO vendas (produto_id, quantidade_vendida, data) VALUES (?, ?, ?)",
            (produto_id, quantidade, data_venda)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("index"))

    conn.close()
    return render_template("registrar_venda.html", produtos=produtos)


@app.route("/relatorio_vendas", methods=["GET"])
def relatorio_vendas():
    mes = request.args.get("mes")
    produto_id = request.args.get("produto_id")

    conn = conectar()
    cursor = conn.cursor()
    query = """
        SELECT p.nome, v.quantidade_vendida, v.data 
        FROM vendas v 
        JOIN produtos p ON v.produto_id = p.id 
        WHERE 1=1
    """
    params = []

    if mes:
        query += " AND strftime('%m', v.data) = ?"
        params.append(mes.zfill(2))
    if produto_id:
        query += " AND p.id = ?"
        params.append(produto_id)

    cursor.execute(query, params)
    vendas = cursor.fetchall()
    
    cursor.execute("SELECT id, nome FROM produtos")
    produtos = cursor.fetchall()
    
    conn.close()

    return render_template("relatorio_vendas.html", vendas=vendas, produtos=produtos)

@app.route("/calcular_materia", methods=["GET", "POST"])
def calcular_materia():
    conn = conectar()
    cursor = conn.cursor()

    calculos = []

    if request.method == "POST":
        produto_id = int(request.form["produto_id"])
        quantidade_produzida = int(request.form["quantidade"])

        # Buscar dados do produto escolhido
        cursor.execute("SELECT nome, materia_prima_por_unidade FROM produtos WHERE id = ?", (produto_id,))
        produto = cursor.fetchone()
        if not produto:
            conn.close()
            return "Produto não encontrado", 404

        nome_produto, materia_prima_por_unidade = produto

        # Calcular matéria-prima total
        total_materia = quantidade_produzida * materia_prima_por_unidade

        # Buscar insumos relacionados ao produto, se tiver (se quiser implementar)
        # Aqui vamos apenas retornar o cálculo direto

        calculos.append({
            "produto": nome_produto,
            "quantidade_produzida": quantidade_produzida,
            "materia_prima_por_unidade": materia_prima_por_unidade,
            "total_materia": total_materia
        })

    # Para preencher o select de produtos
    cursor.execute("SELECT id, nome FROM produtos")
    produtos = cursor.fetchall()

    conn.close()
    return render_template("calcular_materia.html", produtos=produtos, calculos=calculos)


if __name__ == "__main__":
    inicializar()
    app.run(debug=True)
