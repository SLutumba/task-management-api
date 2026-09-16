from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from pydantic import ValidationError
from app.database import SessionLocal
from app.exceptions import InvalidDateTimeError
from app.schemas.task import CreateTaskRequest
from app.services.task import get_tasks, create_task
from app.utils.helper_functions import task_serialiser, tasks_serialiser

task_blueprint = Blueprint('tasks', 'tasks', url_prefix="/tasks")

@task_blueprint.route("/health", methods=['GET', 'POST'])
def health_check():
    return {"status": "healthy"}

@task_blueprint.route("/create", methods=['POST'])
@jwt_required()
def create_user_task():
    current_user_id = int(get_jwt_identity())

    try:
        payload = request.get_json()
        create_request = CreateTaskRequest.model_validate(payload)
    except ValidationError as exc:
        return {"error": "Invalid request data", 
                "details": exc.errors()}, 400

    db = SessionLocal()
    try:
        task = create_task(db=db, 
                        request=create_request, 
                        user_id=current_user_id)
    except InvalidDateTimeError as e:
        return {"error": str(e)}, 406

    finally:
        db.close()

    return jsonify(task_serialiser(task))

@task_blueprint.route("/", methods=['GET'])
@jwt_required()
def get_user_tasks():

    current_user_id = int(get_jwt_identity())

    db = SessionLocal()
    tasks = get_tasks(db, user_id=current_user_id)
    db.close()
    
    return jsonify(tasks_serialiser(tasks)), 201