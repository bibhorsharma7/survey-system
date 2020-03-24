# Routes.py

from flask import Flask, redirect, render_template, request, url_for
from server import app
#from create_csv import write_to_csv, read_from_csv
from user import Admin, User

from surveyItems import Survey, Question
from flask_login import login_required, login_user, logout_user, current_user
from server import login_manager

from databaseCreator import Library
from login_db import Database
from enrolments_db import Enrolment
from course_database import Course_library

import csv
import sys

#global variable for question id.. (should reset every time a survey is created)
q_id = 1
global role
role = ""

globalAdmin = Admin("admin", "pass")
surveyList = []

# Need a statement to check if the database already exists or not
data = Database("users")
if not data.has_table("users"):
    data.create_table()
    with open('passwords.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            data.insert_user(row[0], row[1], row[2])

# Need a statement to check if the database exists or not
enrol = Enrolment("courses")
if not enrol.has_table("courses"):
    enrol.create_table()
    with open('enrolments.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            l = [row[1],row[2]]
            l = "_".join(l)
            enrol.insert_row(row[0],l)

course_status = Course_library('course_status')
if not course_status.has_table('course_status'):
    course_status.create_table()
    with open('courses.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            l = [row[0],row[1]]
            l = "_".join(l)
            course_status.insert_course(l,0)
            
def max_id_in_db(course_name):
    max_id = 0
    check_library = Library(course_name)
    question_list = check_library.retrieve_table()
    for question in question_list:
        if question[6] > max_id:
            max_id = question[6]
    return (max_id + 1)

@login_manager.user_loader
def load_user(userid):
    return User(userid)

def authenticate(uname, paswd):
    # Check if its admin
    global role
    if (data.authenticate("users", uname, paswd) == False):
        return False
    else:
        role = data.authenticate("users", uname, paswd)
        user = User(uname)
        login_user(user)
        return True

@app.route("/mySurvey", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # check for authentication
        if authenticate(username, password):
            global role
            print(role , file=sys.stderr)
            if (role == "admin"):
                return redirect(url_for("admin_course"))
            elif (role == "student"):
                return redirect(url_for("student_course"))
            elif (role == "staff"):
                return redirect(url_for("staff_course"))
        else:
            return redirect(url_for("incorrect",e=401))

    return render_template("login.html")

@app.errorhandler(401)
@app.route("/incorrect/<e>/", methods=["GET", "POST"])
def incorrect(e):
    if request.method == "POST":
        return redirect(url_for("index"))

    return render_template("incorrect.html")
 
@app.route("/cannot_access_currently", methods=["GET", "POST"])
def no_access():
    if request.method == "POST":
        return redirect(url_for("index"))
    
    return render_template("no_access.html")

@app.route("/mySurvey/admin_create_survey/<course>", methods=["GET", "POST"])
@login_required
def create_admin(course):
    global role
    if (role != "admin"):
        return redirect(url_for("no_access"))

    library = Library(course)
    library.create_table()
    currSurvey = library.retrieve_table()
    generic_library = Library('GENERIC_POOL')
    generic_library.create_table()
    optional_library = Library('OPTIONAL_POOL')
    optional_library.create_table()
    if request.method == "POST":

#collects info on new generic questions
        generic_multi_quest = request.form["generic_multi_question"]

        generic_opt_1 = request.form["generic_option_1"]
        generic_opt_2 = request.form["generic_option_2"]
        generic_opt_3 = request.form["generic_option_3"]
        generic_opt_4 = request.form["generic_option_4"]

        #import pdb; pdb.set_trace()
        generic_text_quest = request.form["generic_text_question"]

        #collects info on new optional questions
        optional_multi_quest = request.form["optional_multi_question"]

        optional_opt_1 = request.form["optional_option_1"]
        optional_opt_2 = request.form["optional_option_2"]
        optional_opt_3 = request.form["optional_option_3"]
        optional_opt_4 = request.form["optional_option_4"]

        optional_text_quest = request.form["optional_text_question"]

# a multi question is added to the generic list
        if 'add_multi_question_to_generic_list' in request.form:
            l = [generic_opt_1, generic_opt_2, generic_opt_3, generic_opt_4]
            q_id = max_id_in_db('GENERIC_POOL')
            newQuestion = Question(0, generic_multi_quest,l, q_id)
            linear = newQuestion.convertLinear()
            generic_library.insert_question(linear[0], linear[1], linear[2], linear[3], linear[4], linear[5], linear[6])

            return render_template("admin_create_survey.html", questions_in_survey = library.retrieve_table(), generic_questions = generic_library.retrieve_table(), optional_questions = optional_library.retrieve_table(), course_name = course)

        # a text question is added to the generic list
        elif 'add_text_question_to_generic_list' in request.form:
            l = ["", "", "", ""]
            q_id = max_id_in_db('GENERIC_POOL')
            newQuestion = Question(1, generic_text_quest,l, q_id)
            linear = newQuestion.convertLinear()
            generic_library.insert_question(linear[0], linear[1], linear[2], linear[3], linear[4], linear[5], linear[6])

            return render_template("admin_create_survey.html", questions_in_survey = library.retrieve_table(), generic_questions= generic_library.retrieve_table(), optional_questions=optional_library.retrieve_table(), course_name = course)

        # a multi question is added to the optional list
        elif 'add_multi_question_to_optional_list' in request.form:

            l = [optional_opt_1, optional_opt_2, optional_opt_3, optional_opt_4]
            q_id = max_id_in_db('OPTIONAL_POOL')
            newQuestion = Question(0, optional_multi_quest,l, q_id)
            linear = newQuestion.convertLinear()
            optional_library.insert_question(linear[0], linear[1], linear[2], linear[3], linear[4], linear[5], linear[6])

            return render_template("admin_create_survey.html", questions_in_survey = library.retrieve_table(), generic_questions= generic_library.retrieve_table(), optional_questions=optional_library.retrieve_table(), course_name = course)

        # a text question is added to the optional list
        elif 'add_text_question_to_optional_list' in request.form:

            l = ["", "", "", ""]
            q_id = max_id_in_db('OPTIONAL_POOL')
            newQuestion = Question(1, optional_text_quest, l, q_id)
            linear = newQuestion.convertLinear()
            optional_library.insert_question(linear[0], linear[1], linear[2], linear[3], linear[4], linear[5], linear[6])
            return render_template("admin_create_survey.html", questions_in_survey = library.retrieve_table(), generic_questions= generic_library.retrieve_table(), optional_questions=optional_library.retrieve_table(), course_name = course)

        # a generic question is added to the survey
        elif 'add_generic_question_to_survey' in request.form:
            q_number = -1
            q_number = request.form["add_generic_question_to_survey"]
            q_number = int(q_number)
            generic_questions=generic_library.retrieve_table()
            q_id = max_id_in_db(course)
            library.insert_question(generic_questions[q_number][0], generic_questions[q_number][1], generic_questions[q_number][2], generic_questions[q_number][3], generic_questions[q_number][4], generic_questions[q_number][5], q_id)
            
            return render_template("admin_create_survey.html", questions_in_survey = library.retrieve_table(), generic_questions= generic_library.retrieve_table(), optional_questions=optional_library.retrieve_table(), course_name = course)
       
#commented out as this isn't meant to appear on the admin page
#        # an optional question is added to the survey
#        elif 'add_optional_question_to_survey' in request.form:
#            q_number = -1
#            q_number = request.form["add_optional_question_to_survey"]
#            q_number = int(q_number)
#            optional_questions=optional_library.retrieve_table()
#            q_id = max_id_in_db(course)
#            library.insert_question(optional_questions[q_number][0], optional_questions[q_number][1], optional_questions[q_number][2], optional_questions[q_number][3], optional_questions[q_number][4], optional_questions[q_number][5], q_id)
#            return render_template("admin_create_survey.html", questions_in_survey = library.retrieve_table(), generic_questions= generic_library.retrieve_table(), optional_questions=optional_library.retrieve_table(), course_name = course)
 
        # the survey is submitted
        elif 'finish' in request.form:
            course_status = Course_library('course_status')
            course_status.update_status(course, 1)
            # Course status 1 = course open for review
            return redirect(url_for("survey_created"))

    return render_template("admin_create_survey.html", questions_in_survey = library.retrieve_table(), generic_questions= generic_library.retrieve_table(), optional_questions=optional_library.retrieve_table(), course_name = course)

@app.route("/mySurvey/staff_create_survey/<course>", methods=["GET", "POST"])
@login_required
def create_staff(course):
    global role
    if (role != "staff"):
        return redirect(url_for("no_access"))

    library = Library(course)
    currSurvey = library.retrieve_table()
    optional_library = Library('OPTIONAL_POOL')
    if request.method == "POST":
        # an optional question is added to the survey
        if 'add_question_to_survey' in request.form:
            q_number = -1
            q_number = request.form["add_question_to_survey"]
            q_number = int(q_number)
            questions=optional_library.retrieve_table()
            q_id = max_id_in_db(course)
            library.insert_question(questions[q_number][0], questions[q_number][1], questions[q_number][2], questions[q_number][3], questions[q_number][4], questions[q_number][5], q_id)
            
            return render_template("staff_create_survey.html", questions_in_survey = library.retrieve_table(), optional_questions= optional_library.retrieve_table(), course_name = course)
        

        # the survey is submitted
        elif 'finish' in request.form:
            course_status = Course_library('course_status')
            # Course status 2 = course survey open for response
            course_status.update_status(course, 2)
            return redirect(url_for("survey_created"))

    return render_template("staff_create_survey.html", questions_in_survey=library.retrieve_table(), optional_questions=optional_library.retrieve_table(), course_name = course)

@app.route("/mySurvey/created_survey", methods=["GET", "POST"])
@login_required
def survey_created():
    if request.method == "POST":
        return redirect(url_for("index"))
    return render_template("created.html")

@app.route("/mySurvey/admin_choose_subject", methods=["GET", "POST"])
@login_required
def admin_course():
    global role
    if (role != "admin"):
        return redirect(url_for("no_access"))
    course_status = Course_library('course_status')
    course_list = course_status.get_course_array(0)
    courses_to_enrol = course_status.get_all_courses()
    login_db = Database("users")
    user_list = login_db.return_all_users()
    enrol_db = Enrolment("courses")
    if request.method == "POST":
        if 'logout' in request.form:
            logout_user()
            return redirect(url_for("index"))
        elif 'choose_course' in request.form:
            course_selected = request.form["Item_name"]
            return redirect(url_for("create_admin",course = course_selected))
        else:
            course_selected = request.form["course_for_enrol"]
            user_selected = request.form["enrol"]
            enrol_db.insert_row(user_selected, course_selected)
            return render_template("admin_choices.html", courses = course_list, users = user_list, all_courses = courses_to_enrol)

    return render_template("admin_choices.html", courses = course_list, users = user_list, all_courses = courses_to_enrol)

@app.route("/mySurvey/staff_choose_subject", methods=["GET", "POST"])
@login_required
def staff_course():
    global role
    if (role != "staff"):
        return redirect(url_for("no_access"))
    enrol_db = Enrolment("courses")
    u_id = current_user.get_id()
    course_list = enrol_db.get_courselist("courses", u_id)
    course_status = Course_library('course_status')
    courses_for_review = course_status.match_courses_and_status(course_list, 1)
    courses_for_results = course_status.match_courses_and_status(course_list, 2)
#needs fixing but this is a start to use the status of the course and return the correct list
#    courses_under_review = get_courselist(status_is_under_review (we'll probably use 1))
#    courses_to_return = in_both(courses_under_review, course_list)
    for x in course_list:
        print(x, file=sys.stderr)

    if request.method == "POST":
        if 'logout' in request.form:
            logout_user()
            return redirect(url_for("index"))
        elif 'choose_course' in request.form:
            course_selected = request.form["Item_name"]
            return redirect(url_for("create_staff", course = course_selected))
        else:
            course_selected = request.form["course_for_results"]
            return redirect(url_for("show_responses", course = course_selected))
    return render_template("staff_choices.html", courses = courses_for_review, results_courses = courses_for_results)

@app.route("/student_choose_subject", methods=["GET", "POST"])
@login_required
def student_course():
    global role
    if (role != "student"):
        return "Cannot access this page with current login."
    enrol_db = Enrolment("courses")
    u_id = current_user.get_id()
    course_list = enrol_db.get_courselist("courses", u_id)
    course_status = Course_library('course_status')
    courses_for_response = course_status.match_courses_and_status(course_list, 2)
#needs fixing but this is a start to use the status of the course and return the correct list
#    courses_open = get_courselist(status_is_under_review (we'll probably use 2))
#    courses_to_return = in_both(courses_open, course_list)
    if request.method == "POST":
        if 'logout' in request.form:
            logout_user()
            return redirect(url_for("index"))
        elif 'choose_course' in request.form:
            course_selected = request.form["Item_name"]
            return redirect(url_for("response", course = course_selected))

    return render_template("test.html", courses = courses_for_response)

@app.route("/respond/<course>", methods=["GET", "POST"])
@login_required
def response(course):
    global role
    if (role != "student"):
        return "Cannot access this page with current login."
    library = Library(course)
    currSurvey = library.retrieve_table()
    counter = 0
    if request.method == "POST":
        for question in currSurvey:
            if question[0] == 0:
                response = library.getResponses(question[6])
                check = str(counter)
                currResponse = request.form[check]
                old_response_count = 0;
                print(currResponse)
                print(response[0],response[1],response[2],response[3])
                if int(currResponse) == 1:
                    old_response_count = response[0]
                    response[0] = response[0] + 1
                elif int(currResponse) == 2:
                    old_response_count = response[1]
                    response[1] = response[1] + 1
                elif int(currResponse) == 3:
                    old_response_count = response[2]
                    response[2] = response[2] + 1
                elif int(currResponse) == 4:
                    response[3] = response[3] + 1
                library.addResponses(response[0], response[1], response[2], response[3], response[4], question[6])
            elif question[0] == 1:
                response = library.getResponses(question[6])
                check = str(counter)                
                currResponse = request.form[check]
                response[4] = "\n".join([response[4], currResponse])
                library.addResponses(response[0], response[1], response[2], response[3], response[4], question[6])
            counter+=1
        return redirect(url_for("show_responses", course = course))
    return render_template("respondents.html", course_name = course, questions = library.retrieve_table())

@app.route("/responses/<course>", methods=["GET","POST"])
@login_required
def show_responses(course):
    library = Library(course)
    rows_of_table = []
    rows_of_table = library.get_rows()
    if request.method == "POST":
        logout_user()
        return redirect(url_for("index"))
    return render_template("show_results.html", course_name = course, questions_in_survey = rows_of_table)

