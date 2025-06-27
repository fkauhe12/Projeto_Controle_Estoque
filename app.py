from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def conectar():
    return sqlite3.connect('Cadastro.db')

def inicializar():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quarteis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            endereco TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS agentes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            quartel_id INTEGER NOT NULL,
            celular TEXT NOT NULL,
            tamanho_roupa TEXT NOT NULL,
            FOREIGN KEY (quartel_id) REFERENCES quarteis(id)
        )
    ''')

    conn.commit()
    conn.close()

def popular_quarteis_fortaleza():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM quarteis")
    count = cursor.fetchone()[0]

    if count == 0:
        quarteis_fortaleza = [
            ("Quartel do 1º Batalhão", "Rua do Quartel, 123 - Fortaleza"),
            ("Quartel do 2º Batalhão", "Avenida Fortaleza, 456 - Fortaleza"),
            ("Quartel do 3º Batalhão", "Praça dos Soldados, 789 - Fortaleza"),
            ("Quartel do Comando Geral", "Rua Principal, 100 - Fortaleza"),
            ("Quartel da Polícia Militar", "Avenida Central, 200 - Fortaleza"),
        ]
        cursor.executemany("INSERT INTO quarteis (nome, endereco) VALUES (?, ?)", quarteis_fortaleza)
        conn.commit()
    conn.close()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/cadastrar_agente", methods=["GET", "POST"])
def cadastrar_agente():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT id, nome FROM quarteis ORDER BY nome")
    quarteis = cursor.fetchall()

    if request.method == "POST":
        nome = request.form["nome"]
        quartel_id = int(request.form["quartel"])
        celular = request.form["celular"]
        tamanho = request.form["tamanho"]

        cursor.execute("INSERT INTO agentes (nome, quartel_id, celular, tamanho_roupa) VALUES (?, ?, ?, ?)",
                       (nome, quartel_id, celular, tamanho))
        conn.commit()
        conn.close()
        return redirect(url_for("visualizar_agentes"))

    conn.close()
    return render_template("cadastrar_agente.html", quarteis=quarteis)

@app.route("/visualizar_agentes")
def visualizar_agentes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT a.nome, q.nome, a.celular, a.tamanho_roupa
        FROM agentes a
        JOIN quarteis q ON a.quartel_id = q.id
        ORDER BY a.nome
    ''')
    agentes = cursor.fetchall()
    conn.close()
    return render_template("visualizar_agentes.html", agentes=agentes)

if __name__ == "__main__":
    inicializar()
    popular_quarteis_fortaleza()
    app.run(debug=True)
