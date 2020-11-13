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
class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(),nullable=False)
    completed = db.Column(db.Boolean,nullable=False,default=False)

    def __repr__(self):
        return f'<TODO ID:{self.id} Description:{self.description}>'

#Tables creation if not exists
#Table creation will be handled from Flask Migrate
#db.create_all()

@app.route('/')
def index():
    return render_template('index.html', data=Todo.query.all())

@app.route('/todos/create',methods=['POST'])
def create():
    description = request.form.get('description','')

    todo = Todo(description=description)
    db.session.add(todo)
    db.session.commit()
    db.session.close()

    return redirect(url_for('index'))

@app.route('/todos/createAjax',methods=['POST'])
def createAjax():
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






# if __name__ == '__main__':
#     app.run()