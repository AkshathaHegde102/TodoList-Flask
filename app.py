# import flask
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Setup application
app = Flask(__name__)

# Tell our app where the DB is located, can use mysql or postgres but here we use sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# initialize database
db = SQLAlchemy(app)
# create model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    # Have a string returned everytime we create a new element
    def __repr__(self):
        return '<Task %r>' % self.id

# create index route so that when we browse the URL, we dont 404
# Instead of GET by default we now have POST (and send data to our database) as well
@app.route('/', methods = ['POST', 'GET'])

# Define function for that route , render_templates makes the code look in the 'templates' file
# Add 
def index():
    if request.method == 'POST':
        # form is the form we created, id is content
        task_content = request.form['content']
        # create todo object
        new_task = Todo(content = task_content)

        # push to db
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue adding your task"
    else:
        # Finds all content in the db and returns all
        tasks = Todo.query.order_by(Todo.date_created).all()
        # tasks = tasks - passes to the template
        return render_template('index.html', tasks = tasks)
    
# add the delete
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "error"

@app.route('/update/<int:id>', methods = ['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Update ErrorS'
    else:
        return render_template('update.html', task = task)

if __name__ == "__main__":
    app.run(debug = True)