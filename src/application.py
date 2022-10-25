from flask import Flask, Response, request
from datetime import datetime
import json
from columbia_student_resource import ColumbiaStudentResource
from courses_resource import CoursesResource
from flask_cors import CORS

# Create the Flask application object.
app = Flask(__name__,
            static_url_path='/',
            static_folder='static/class-ui/',
            template_folder='web/templates')

CORS(app)


@app.get("/api/health")
def get_health():
    t = str(datetime.now())
    msg = {
        "name": "F22-Starter-Microservice",
        "health": "Good",
        "at time": t
    }

    # DFF TODO Explain status codes, content type, ... ...
    result = Response(json.dumps(msg), status=200, content_type="application/json")

    return result


@app.route("/api/students/<uni>", methods=["GET"])
def get_student_by_uni(uni):
    result = ColumbiaStudentResource.get_by_key(uni)

    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    return rsp


@app.route("/course/user/<user_id>", methods=["GET"])
def get_courses_by_userid(user_id):
    result = CoursesResource.get_by_userid(user_id)

    if result:
        rsp = Response(json.dumps(result, default=str), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    return rsp


# @app.route("/courses?teacher=<teacher_id>", methods=["GET"])
# def get_courses_by_teacherid(teacher_id):
#     result = CoursesResource.get_by_teacherid(teacher_id)
#
#     if result:
#         rsp = Response(json.dumps(result), status=200, content_type="application.json")
#     else:
#         rsp = Response("NOT FOUND", status=404, content_type="text/plain")
#
#     return rsp

@app.route("/course/create", methods=["POST"])
def create_course():
    json_dict = request.get_json()
    user_id = str(json_dict["user_id"])
    teacher_id = str(json_dict["teacher_id"])
    create_time = str(datetime.now())
    appointment_time = json_dict["appointment_time"]
    price = float(json_dict["price"])

    fields = (user_id, teacher_id, create_time, appointment_time, price)
    CoursesResource.create_course_by_field(fields)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5011)
