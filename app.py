from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    priority = db.Column(db.String(20),nullable= False,default = 'Medium')

@app.route('/')
def index():
    tasks = Task.query.order_by(Task.priority.desc()).all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task_content = request.form.get['content']
    task_priority = request.form['priority']
    new_task = Task(content=task_content,priority=task_priority)
    db.session.add(new_task)
    db.session.commit()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
