import os, sqlite3
from functools import wraps
import requests
from flask import Flask, flash, g, jsonify, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key-troque-em-producao")
app.config["DATABASE"] = os.path.join(app.instance_path, "tarefas.sqlite3")
os.makedirs(app.instance_path, exist_ok=True)

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop("db", None)
    if db: db.close()

def init_db():
    db = get_db()
    db.executescript("""
        CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY, nome TEXT NOT NULL, email TEXT NOT NULL UNIQUE, senha TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS tarefas (id INTEGER PRIMARY KEY, titulo TEXT NOT NULL, descricao TEXT, status TEXT DEFAULT 'pendente' CHECK(status IN ('pendente', 'andamento', 'concluida')), usuario_id INTEGER NOT NULL, FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE);
    """)
    db.commit()

@app.cli.command("init-db")
def init_db_command():
    with app.app_context():
        init_db()
    print("DB OK")

def login_required(view):
    @wraps(view)
    def wrapped(*a, **k):
        if g.user is None:
            flash("Faça login para acessar.", "warning")
            return redirect(url_for("login"))
        return view(*a, **k)
    return wrapped

@app.before_request
def load_user():
    g.user = None
    if uid := session.get("user_id"):
        g.user = get_db().execute("SELECT id, nome, email FROM usuarios WHERE id = ?", (uid,)).fetchone()

@app.context_processor
def inject_user():
    return {"current_user": g.user}


@app.route("/registro", methods=("GET", "POST"))
def registro():
    if g.user: return redirect(url_for("dashboard"))
    if request.method == "POST":
        nome, email, senha = request.form.get("nome", "").strip(), request.form.get("email", "").strip().lower(), request.form.get("senha", "")
        if not (nome and email and senha):
            flash("Preencha todos os campos.", "danger")
        elif request.form.get("confirmar_senha", "") != senha:
            flash("Senhas não coincidem.", "danger")
        elif len(senha) < 6:
            flash("Mínimo 6 caracteres.", "danger")
        else:
            try:
                db = get_db()
                cur = db.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", (nome, email, generate_password_hash(senha)))
                db.commit()
                session.clear()
                session["user_id"] = cur.lastrowid
                flash("Conta criada!", "success")
                return redirect(url_for("dashboard"))
            except sqlite3.IntegrityError:
                flash("E-mail já cadastrado.", "danger")
    return render_template("auth/registro.html")

@app.route("/login", methods=("GET", "POST"))
def login():
    if g.user: return redirect(url_for("dashboard"))
    if request.method == "POST":
        email, senha = request.form.get("email", "").strip().lower(), request.form.get("senha", "")
        user = get_db().execute("SELECT * FROM usuarios WHERE email = ?", (email,)).fetchone()
        if user and check_password_hash(user["senha"], senha):
            session.clear()
            session["user_id"] = user["id"]
            flash("Login realizado!", "success")
            return redirect(url_for("dashboard"))
        flash("Credenciais inválidas.", "danger")
    return render_template("auth/login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Logout realizado.", "info")
    return redirect(url_for("login"))


VALID_STATUSES = {"pendente", "andamento", "concluida"}

@app.route("/")
def index():
    return redirect(url_for("dashboard") if g.user else url_for("login"))

@app.route("/dashboard")
@login_required
def dashboard():
    status = request.args.get("status", "todas")
    if status not in {"todas", "pendente", "andamento", "concluida"}:
        status = "todas"
    if status == "todas":
        tarefas = get_db().execute("SELECT * FROM tarefas WHERE usuario_id = ? ORDER BY id DESC", (g.user["id"],)).fetchall()
    else:
        tarefas = get_db().execute("SELECT * FROM tarefas WHERE usuario_id = ? AND status = ? ORDER BY id DESC", (g.user["id"], status)).fetchall()
    return render_template("dashboard.html", tarefas=tarefas, status_filter=status)


@app.route("/nova_tarefa", methods=("GET", "POST"))
@login_required
def nova_tarefa():
    if request.method == "POST":
        titulo, descricao, status = request.form.get("titulo", "").strip(), request.form.get("descricao", "").strip(), request.form.get("status", "pendente")
        if not titulo:
            flash("Título obrigatório.", "danger")
        elif status not in VALID_STATUSES:
            flash("Status inválido.", "danger")
        else:
            get_db().execute("INSERT INTO tarefas (titulo, descricao, status, usuario_id) VALUES (?, ?, ?, ?)", (titulo, descricao, status, g.user["id"]))
            get_db().commit()
            flash("Tarefa criada!", "success")
            return redirect(url_for("dashboard"))
    return render_template("tarefa_form.html", tarefa=None)

def get_user_task(task_id):
    return get_db().execute("SELECT * FROM tarefas WHERE id = ? AND usuario_id = ?", (task_id, g.user["id"])).fetchone()

@app.route("/editar/<int:task_id>", methods=("GET", "POST"))
@login_required
def editar(task_id):
    tarefa = get_user_task(task_id)
    if not tarefa:
        flash("Tarefa não encontrada.", "danger")
        return redirect(url_for("dashboard"))
    if request.method == "POST":
        titulo, descricao, status = request.form.get("titulo", "").strip(), request.form.get("descricao", "").strip(), request.form.get("status", "pendente")
        if not titulo:
            flash("Título obrigatório.", "danger")
        elif status not in VALID_STATUSES:
            flash("Status inválido.", "danger")
        else:
            get_db().execute("UPDATE tarefas SET titulo = ?, descricao = ?, status = ? WHERE id = ? AND usuario_id = ?", (titulo, descricao, status, task_id, g.user["id"]))
            get_db().commit()
            flash("Tarefa atualizada!", "success")
            return redirect(url_for("dashboard"))
    return render_template("tarefa_form.html", tarefa=tarefa)

@app.post("/excluir/<int:task_id>")
@login_required
def excluir(task_id):
    if get_user_task(task_id):
        get_db().execute("DELETE FROM tarefas WHERE id = ? AND usuario_id = ?", (task_id, g.user["id"]))
        get_db().commit()
        flash("Tarefa excluída.", "success")
    else:
        flash("Tarefa não encontrada.", "danger")
    return redirect(url_for("dashboard"))

@app.post("/concluir/<int:task_id>")
@login_required
def concluir(task_id):
    tarefa = get_user_task(task_id)
    if tarefa:
        novo = "concluida" if tarefa["status"] != "concluida" else "pendente"
        get_db().execute("UPDATE tarefas SET status = ? WHERE id = ? AND usuario_id = ?", (novo, task_id, g.user["id"]))
        get_db().commit()
        flash("Status atualizado.", "success")
    else:
        flash("Tarefa não encontrada.", "danger")
    return redirect(url_for("dashboard"))


@app.get("/api/progresso")
@login_required
def api_progresso():
    rows = get_db().execute("SELECT status, COUNT(*) AS quantidade FROM tarefas WHERE usuario_id = ? GROUP BY status", (g.user["id"],)).fetchall()
    counts = {"pendente": 0, "andamento": 0, "concluida": 0}
    for row in rows:
        counts[row["status"]] = row["quantidade"]
    return jsonify(counts)


@app.route("/dashboard/progresso")
@login_required
def dashboard_progresso():
    return render_template("progresso.html")


@app.get("/api/frase")
@login_required
def api_frase():
    try:
        r = requests.get("https://api.adviceslip.com/advice", timeout=5, headers={"Accept": "application/json"})
        r.raise_for_status()
        return jsonify({"frase": r.json()["slip"]["advice"]})
    except:
        return jsonify({"frase": "Continue aprendendo: pequenos passos constroem grandes resultados."})


@app.get("/health")
def health():
    return jsonify({"status": "ok"})

with app.app_context():
    init_db()

if __name__ == "__main__":
    app.run(debug=os.environ.get("DEBUG", "1") == "1")
