from flask import Flask, request, render_template, redirect, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    task = db.Column(db.String(50),nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return f'{self.task}'

@app.route('/')
def index():
    tasks = Todo.query.all()
    return render_template('index.html',tasks=tasks)

@app.route('/add',methods=['POST'])
def add():
    task = request.form['todo']
    try:
        todo = Todo(task=task)
        db.session.add(todo)
        db.session.commit()
    except Exception as e:
        print(e)
    return redirect('/')    

@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    todo = Todo.query.get_or_404(id)
    tasks = Todo.query.all()
    if request.method == 'POST':
        try:
            new_task = request.form['todo']
            todo.task = new_task
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(e) 
            return abort(404) 

    return render_template('index.html',new_todo=todo.task,task_id=id,tasks=tasks)

@app.route('/delete/<int:id>',methods=['GET','POST'])
def delete(id):
    todo = Todo.query.get_or_404(id)
    try:
        db.session.delete(todo)
        db.session.commit()
        return redirect('/')
        
    except Exception as e:
        print(e)
        return abort(404) 
    

if __name__ == '__main__':
    app.run(debug=True)