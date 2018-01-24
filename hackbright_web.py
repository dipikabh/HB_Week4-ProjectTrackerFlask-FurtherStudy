"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/")
def show_homepage():

    students = hackbright.get_all_students()
    projects = hackbright.get_all_projects()
    return render_template("homepage.html", students=students, projects=projects)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)
    title_grade = hackbright.get_grades_by_github(github)

    return render_template("student_info.html", first=first, last=last,
                            github=github, title_grade=title_grade)


@app.route("/student-search")
def get_student_form():

    return render_template("student_search.html")


@app.route("/enter-student")
def enter_student():

    return render_template("student_add.html")


@app.route("/student-add", methods=['POST'])
def student_add():

    first = request.form.get("first_name")
    last = request.form.get("last_name")
    github = request.form.get("github")

    hackbright.make_new_student(first, last, github)
    return render_template("student_added.html", first=first, last=last,
                           github=github)


@app.route("/enter-project")
def enter_project():

    return render_template("project_add.html")


@app.route("/project-add", methods=['POST'])
def project_add():

    title = request.form.get("title")
    desc = request.form.get("desc")
    grade = request.form.get("grade")

    hackbright.make_new_project(title, desc, grade)
    return render_template("project_added.html", title=title, desc=desc,
                           grade=grade)


@app.route("/enter-grade")
def enter_grade():

    student_names = hackbright.get_all_students()
    projects = hackbright.get_all_projects()

    return render_template("grade_add.html", students=student_names, projects=projects)


@app.route("/grade-add", methods=["POST"])
def grade_add():

    name = request.form.get("name")
    project = request.form.get("project")
    grade = request.form.get("grade")

    first_name, last_name = name.split()
    github = hackbright.get_github_by_student(first_name, last_name)
    hackbright.assign_grade(github, project, grade)


@app.route("/project")
def show_project_info():

    project_title = request.args.get('title')

    project_info = hackbright.get_project_by_title(project_title)
    student_grade_info = hackbright.get_grades_by_title(project_title)

    return render_template("project_info.html",
                           project_info=project_info,
                           student_grade_info=student_grade_info)



if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
