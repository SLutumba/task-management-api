from flask import Flask
from app.api.tasks import tasks

app = Flask(__name__)
app.register_blueprint(tasks)

@app.route("/")
def main():
    return "Landing. This is main."

if __name__ == "__main__":
    app.run(debug=True)
