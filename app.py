import os
from flask import Flask, render_template, request, redirect, url_for,flash,get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import Date
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.config['SECRET_KEY'] = os.urandom(24) 


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    priority = db.Column(db.String(20), nullable=False, default='Medium')
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    category = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f'<Task {self.id} - {self.content} - {self.category}>'


@app.route('/' , methods=['GET','POST'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Task(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return 'There was an issue adding your task'

    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    task_content = request.form.get('content')
    task_priority = request.form.get('priority')
    task_category = request.form.get('category', '')

    if not task_content:
        flash('Task content is required!', 'danger')
        return redirect(url_for('index'))

    try:
        new_task = Task(content=task_content, priority=task_priority, category=task_category)
        db.session.add(new_task)
        db.session.commit()
        #flash('Task added successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        #flash(f'Error adding task: {e}', 'danger')

    return redirect(url_for('index'))



@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    try:
        db.session.delete(task)
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return 'There was an issue deleting your task'
    
@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if request.method == 'POST':
        task.content = request.form['content']
        task.priority = request.form['priority']
        task.category = request.form['category']

        try:
            db.session.commit()
            flash('Task updated successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating task: {e}', 'danger')

    return render_template('edit_task.html', task=task)

if __name__ == '__main__':
    app.run(debug=True)
