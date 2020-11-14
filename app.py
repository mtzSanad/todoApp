from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys


app = Flask(__name__)
#db uri
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:postgres@localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Linking sqlalchemy with application
db = SQLAlchemy(app)
# db = SQLAlchemy(app,session_options={"expire_on_commit":False})

#Linking migrate with application and db
migrate = Migrate(app,db)


#Models
class TodoList(db.Model):
    __tablename__ = 'todolists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(),nullable=False)
    todos = db.relationship('Todo',backref='list',lazy=True)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(),nullable=False)
    completed = db.Column(db.Boolean,nullable=False,default=False)
    list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'),nullable=False)

    def __repr__(self):
        return f'<TODO ID:{self.id} Description:{self.description}>'

#Tables creation if not exists
#Table creation will be handled from Flask Migrate
#db.create_all()

@app.route('/')
def index():
    return redirect(url_for('getTodoListById',listId=1))
    # return render_template('index.html', data=Todo.query.order_by('id').all())

@app.route('/list/<listId>')
def getTodoListById(listId):
    return render_template('index.html', 
    todoLists= TodoList.query.order_by('id').all(), 
    active_list = TodoList.query.get(listId) ,
    data=Todo.query.filter_by(list_id=listId).order_by('id').all())

@app.route('/todos/create',methods=['POST'])
def create():
    description = request.form.get('description','')

    todo = Todo(description=description)
    db.session.add(todo)
    db.session.commit()
    db.session.close()

    return redirect(url_for('index'))

@app.route('/todos/createAjax',methods=['POST'])
def createAjax1():
    error = False
    body ={}
    try:
        description = request.get_json()['description']

        todo = Todo(description=description)
        db.session.add(todo)
        db.session.commit()
        body['description'] = todo.description
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if not error:
        return jsonify(body)
    else:
        abort(400)

@app.route('/todos/<todoId>/update-completed',methods=['POST'])
def updateCompleted(todoId):
    try:
        todo = Todo.query.get(todoId)
        completed = request.get_json()['completed']
        todo.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()

    return redirect(url_for('index'))

@app.route('/todos/<todoId>',methods=['DELETE'])
def deleteById(todoId):
    try:
        todo = Todo.query.get(todoId)
        db.session.delete(todo)
        db.session.commit()
    except:
        db.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()

    return jsonify({ 'success': True })
    




# if __name__ == '__main__':
#     app.run()