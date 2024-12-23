from flask import Flask, jsonify, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mega.db'
db = SQLAlchemy(app)

# My Database Models
class User(db.Model):
    __tablename__ = 'users' 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text)
    priority = db.Column(db.String(20), nullable=False)  # low, medium, high
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref='tasks')


@app.get('/users')
def users_index():
    users = User.query.all()
    return render_template('/users/index.html', users=users)

@app.get('/users/create')
def users_create():
    return render_template('/users/create.html')

@app.post('/users')
def users_store():
    form_name = request.form.get('name')
    user = User(name=form_name)
    db.session.add(user)
    db.session.commit()
    return redirect('/users')

@app.get('/users/edit/<int:id>')
def users_edit(id):
    user = User.query.get_or_404(id)
    return render_template('/users/edit.html', user=user)

@app.route('/users/<int:id>', methods=['POST', 'PUT'])
def users_update(id):
    user = User.query.get_or_404(id)
    name = request.form.get('name')
    user.name = name
    db.session.commit()
    return redirect('/users')

@app.route('/users/delete/<int:id>', methods=['POST', 'DELETE'])
def users_destroy(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')



@app.get('/tasks')
def tasks_index():
    tasks = Task.query.all()
    return render_template('/tasks/index.html', tasks=tasks)

@app.get('/tasks/create')
def tasks_create():
    users = User.query.all()
    return render_template('/tasks/create.html', users=users)

@app.post('/tasks')
def tasks_store():
    task = Task(
        name=request.form.get('name'),
        description=request.form.get('description'),
        priority=request.form.get('priority'),
        user_id=request.form.get('user_id')
    )
    db.session.add(task)
    db.session.commit()
    return redirect('/tasks')

@app.get('/tasks/edit/<int:id>')
def tasks_edit(id):
    task = Task.query.get_or_404(id)
    users = User.query.all()
    return render_template('/tasks/edit.html', task=task, users=users)

@app.route('/tasks/<int:id>', methods=['POST', 'PUT'])
def tasks_update(id):
    task = Task.query.get_or_404(id)
    task.name = request.form.get('name')
    task.description = request.form.get('description')
    task.priority = request.form.get('priority')
    task.user_id = request.form.get('user_id')
    db.session.commit()
    return redirect('/tasks')

@app.route('/tasks/delete/<int:id>', methods=['POST', 'DELETE'])
def tasks_destroy(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect('/tasks')



if __name__ == '__main__':
    # with app.app_context():
        # db.create_all()
    app.run(debug=True)
