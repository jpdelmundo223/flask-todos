from flask import Blueprint, render_template, request, flash, redirect, url_for, request
from flask_login import login_required, current_user
from . import db
from .models import Todos
from .forms import TodosForm

todo = Blueprint('todo', __name__, url_prefix='/todos')

# todos = [
#     {
#         "title": "Clean up my desk",
#         "description": "Needs to clean up desk for the upcoming meeting",
#         "status": "In Progress",
#         "priority": "High",
#         "date_added": "April 23, 1997"
#     },
#     {
#         "title": "Clean up my desk 2",
#         "description": "Needs to clean up desk for the upcoming meeting",
#         "status": "Complete",
#         "priority": "High",
#         "date_added": "April 23, 1997"
#     },
#     {
#         "title": "Clean up my desk 3",
#         "description": "Needs to clean up desk for the upcoming meeting",
#         "status": "In Progress",
#         "priority": "High",
#         "date_added": "April 23, 1997"
#     },
# ]

@todo.route('/', methods=['GET'])
@login_required
def index():
    title = 'Todos'
    todos = Todos.query.filter_by(user_id=current_user.id).all()
    return render_template('main/todo.html', todos=todos,
                                                title=title)

@todo.route('/add', methods=['GET', 'POST'])
@login_required
def add_todo():
    title = 'Add Todo'
    form = TodosForm()
    if request.method == "POST":
        if form.validate_on_submit():
            todo = Todos.query.filter_by(title=form.title.data).first()
            if todo is None:
                new_todo = Todos(title=form.title.data,
                                    description=form.description.data,
                                    status=True if int(form.status.data) == 1 else False, # uses ternary operator to convert binary to boolean value
                                    priority=form.priority.data,
                                    user_id=current_user.id)
                db.session.add(new_todo)
                db.session.commit()
                flash("You've successfully added a new todo item!", "success")
                return redirect(url_for('todo.index'))
            else:
                flash("Todo with the same title already exists!", "danger")
            # form_data = f"<Todo title: {form.title.data}, description: {form.description.data}, status: {form.status.data}, priority: {form.priority.data}>"
            # print(form_data)
    return render_template('main/create_todo.html', form=form, 
                                                        title=title)

@todo.route('/update/<int:todo_id>', methods=['GET', 'POST'])
@login_required
def update_todo(todo_id):
    title = 'Update Todo'
    todo_data = Todos.query.filter_by(id=todo_id, user_id=current_user.id).first()
    todo_title = todo_data.title
    todo_description = todo_data.description
    todo_status = True if int(todo_data.status) == 1 else False
    todo_priority = todo_data.priority
    if request.method == "POST":
        Todos.query.filter_by(id=todo_id).update({Todos.title: request.form.get('title'),
                                                         Todos.description: request.form.get('description'), 
                                                         Todos.status: True if int(request.form.get('status')) == 1 else False,
                                                         Todos.priority: request.form.get('priority')})
        db.session.commit()
        flash("Todo item successfully updated!", "success")
        return redirect(url_for('todo.index'))
    return render_template('main/update_todo.html', todo_title=todo_title,
                                                        todo_description=todo_description,
                                                        todo_status=todo_status,
                                                        todo_priority=todo_priority,
                                                        title=title)

@todo.route('/delete/<int:todo_id>')
@login_required
def delete_todo(todo_id):
    Todos.query.filter_by(id=todo_id).delete()
    db.session.commit()
    return redirect(url_for('todo.index'))