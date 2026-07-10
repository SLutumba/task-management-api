from flask import Blueprint

tasks = Blueprint('tasks', 'tasks', url_prefix="/tasks")

@tasks.route("/health", methods=['GET', 'POST'])
def health_check():
    return {"status": "healthy"}