from flask import Flask, Response, request
from datetime import datetime
import json
from columbia_student_resource import ColumbiaStudentResource
from courses_resource import CoursesResource
from flask_cors import CORS
from sns_notification import Notifications

sns_middleware = Notifications()
print(sns_middleware)

# Create the Flask application object.
app = Flask(__name__,
            static_url_path='/',
            static_folder='static/class-ui/',
            template_folder='web/templates')

CORS(app)


@app.before_request
def before_request_func():
    print("before_request executing!")
    print("request = ", json.dumps(request, indent=2, default=str))


@app.after_request
def after_request_func(response):
    print("after_request executing! Response = \n", json.dumps(response, indent=2, default=str))

    sns_middleware.check_publish(request, response)

    return response


@app.route('/', methods=["GET"])
def index():
    return 'You have reached the index page!'


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
    create_time = json_dict["create_time"] #yyyy-mm-dd HH:mm:ss
    appointment_time = json_dict["appointment_time"] #yyyy-mm-dd HH:mm:ss
    price = float(json_dict["price"])

    # fields = (user_id, teacher_id, create_time, appointment_time, price)
    # res = CoursesResource.create_course_by_field(fields)
    res = []
    for time in appointment_time:
        fields = (user_id, teacher_id, create_time, time, price)
        res.append(CoursesResource.create_course_by_field(fields))

    if res:
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    return rsp

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5011)
