import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import os
SECRET_KEY = os.urandom(32)
from flask_restplus import Api, Resource, fields
from werkzeug.middleware.proxy_fix import ProxyFix
import enum
from datetime import datetime, date

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'task'
app.config['SECRET_KEY'] = SECRET_KEY
db = MySQL(app)

class EnumStatus(enum.Enum):
    blank = ''
    nostart = "Not Starterd"
    progress = "In Progress"
    finish = "Finished"

app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='TodoMVC API',
    description='A simple TodoMVC API',
)

ns = api.namespace('todos', description='TODO operations')

todo = api.model('Todo', {
    'id': fields.Integer(readonly=True, description='The task unique identifier'),
    'task': fields.String(required=True, description='The task details'),
    'Dueby': fields.Date(required=True, description='The task deadline'),
    'status': fields.String(required=True, description='Progress of the Task', enum=EnumStatus._member_names_)  
})


class TodoDAO(object):
    def __init__(self):
        self.counter = 0
        self.todos = []

    def get(self, id):
        for todo in self.todos:
            if todo['id'] == id:
                return todo
        api.abort(404, "Todo {} doesn't exist".format(id))

    def create(self, data):
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        todo = data
        todo['id'] = self.counter = self.counter + 1
        self.todos.append(todo)
        cursor.execute('INSERT INTO todo VALUES (NULL,% s, % s, % s)',(todo["task"],todo["Dueby"],todo["status"], ))
        db.connection.commit()
        return todo
    
    def update(self, id, data):
        todo = self.get(id)
        todo.update(data)
        return todo

    def delete(self, id):
        todo = self.get(id)
        self.todos.remove(todo)


DAO = TodoDAO()
# DAO.create({'task': 'Build an API','Dueby':'2022-03-30','status':'Finished'})
# DAO.create({'task': '?????','Dueby':'2022-04-30','status':'In Progress'})
# DAO.create({'task': 'profit!','Dueby':'2022-05-30','status':'Not Starterd'})


@ns.route('/')
class TodoList(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''
    @ns.doc('list_todos')
    @ns.marshal_list_with(todo)
    def get(self):
        '''List all tasks'''
        return DAO.todos

    @ns.doc('create_todo')
    @ns.expect(todo)
    @ns.marshal_with(todo, code=201)
    def post(self):
        '''Create a new task'''
        return DAO.create(api.payload), 201


@ns.route('/<int:id>')
@ns.response(404, 'Todo not found')
@ns.param('id', 'The task identifier')
class Todo(Resource):
    '''Show a single todo item and lets you delete them'''
    @ns.doc('get_todo')
    @ns.marshal_with(todo)
    def get(self, id):
        '''Fetch a given resource'''
        return DAO.get(id)

    @ns.doc('delete_todo')
    @ns.response(204, 'Todo deleted')
    def delete(self, id):
        '''Delete a task given its identifier'''
        DAO.delete(id)
        return '', 204

    @ns.expect(todo)
    @ns.marshal_with(todo)
    def put(self, id):
        '''Update a task given its identifier'''
        return DAO.update(id, api.payload)
    
@ns.route('/<string:status>')
@ns.response(404,'Todo not found')
@ns.param('status','The task progress')
class statustodo(Resource):
    @ns.doc('gettodo')
    @ns.marshal_with(todo)
    def get(self, status):
        fd = []
        for todo in DAO.todos:
            if todo["status"] == status:
                fd.append(todo)
        return fd

@ns.route('/due/<string:Dueby>')
@ns.response(404,'Todo not found')
@ns.param('Dueby','The task Deadline')
class duedate(Resource):
    @ns.doc('gettodo')
    @ns.marshal_with(todo)
    def get(self, Dueby):
        fd = []
        for todo in DAO.todos:
            if todo["Dueby"] == Dueby:
                fd.append(todo)
        return fd

@ns.route('/overdue')
@ns.response(404,'Todo not found')
class overdue(Resource):
    @ns.doc('gettodo')
    @ns.marshal_with(todo)
    def get(self):
        fd = []
        date_format = "%Y-%m-%d"
        for todo in DAO.todos:
            delta = datetime.strptime(str(date.today()), date_format) - datetime.strptime(str(todo["Dueby"]), date_format)
            if(delta.days>=1 and todo["status"]!="Finished"):
                fd.append(todo)
            else:
                continue
        return fd

if __name__ == '__main__':
    app.run(debug=True)