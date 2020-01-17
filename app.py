from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize flask app
app = Flask(__name__)

# Initialize database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

# Define database entry using object relational mapping (OOM)
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False)
    completed = db.Column(db.Integer, default = 0)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return "<Task %r" % self.id

# URL routing for home page
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        # Get task from HTML form (user input)
        task_content = request.form['content']

        # Create database entry
        new_task = Todo(content = task_content)

        try:
            # Add entry to database
            db.session.add(new_task)
            db.session.commit()

            # Return to home page
            return redirect('/')
        except:
            return "There was a problem adding that task"
    else:
        # Query database and get all tasks
        tasks = Todo.query.order_by(Todo.date_created).all()

        return render_template('index.html', tasks = tasks)

# URL routing for delete task
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        # Delete entry from database
        db.session.delete(task_to_delete)
        db.session.commit()

        # Return to home page
        return redirect('/')
    except:
        return "There was a problem deleting that task"

# URL routing for update task
@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    task_to_update = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task_to_update.content = request.form['content']

        try:
            db.session.commit()

            # Return to home page
            return redirect('/')
        except:
            return "There was a problem updating that task"
    else:
        return render_template('update.html', task = task_to_update)

if __name__ == "__main__":
    app.run(debug=True)
