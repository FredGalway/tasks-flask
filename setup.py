
from flask import Flask, request, render_template # Pour activer Flask et le rendu HTML / CSS

from flask_sqlalchemy import SQLAlchemy # Pour interagir avec une base de données

from datetime import datetime # Pour obtenir la date de création d'une tache

from werkzeug.utils import redirect

app = Flask(__name__)

# Configuration Base de données (en Python)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
        )
    
    def __repr__(self):
        return f"Todo : {self.name}"

# Chemins app et requêtes Base de données
@app.route('/', methods=["GET", "POST"])

def index():
    if request.method == "POST":
        name = request.form['name']
        # Ajout d'une tâche
        new_task = Task(name=name)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception:
            return "Une erreur s'est produite"
    else:
        tasks = Task.query.order_by(Task.created_at)
    return render_template("index.html", tasks=tasks)

@app.route("/delete/<int:id>")
def delete(id):
    task = Task.query.get_or_404(id)
    try:
        # Suppression d'une tâche
        db.session.delete(task)
        db.session.commit()
        return redirect("/")
    except Exception:
        return "Une erreur s'est produite"


@app.route('/update/<int:id>/', methods=["GET", "POST"])
def update(id):
    task = Task.query.get_or_404(id)
    if request.method == "POST":
        task.name = request.form["name"]
        try:
            db.session.commit()
            return redirect("/")
        except Exception:
            return "Nous ne pouvons modifier la tâche"
        else:
            title = "Mise à jour"
            return render_template("update.html", title=title, task=task)


@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/infos')
def infos():
    return render_template("infos.html")

@app.route('/404')
def page_non_trouvee():
    return "Cette page devrait vous avoir renvoyé une erreur 404"

if __name__ == "__main__":
    app.run(debug=True)
