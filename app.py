
from flask import Flask, render_template, request, redirect,url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'oracle://hr:hr@127.0.0.1:1521/xe'
db = SQLAlchemy(app)


class Students(db.Model):
    First_Name = db.Column(db.String(20), unique=False)
    Last_Name = db.Column(db.String(20), unique=False)
    DEPARTMENT = db.Column(db.String(20), unique=False)
    EVENT = db.Column(db.String(20), unique=False)
    Email_Id = db.Column(db.String(20), unique=False)
    tele = db.Column(db.Integer(), primary_key=True)


@app.route("/")
def met():
    return render_template("met.html")


@app.route("/datalist")
def datalist():
    # query all students from the database
    students = Students.query.all()

    # pass the list of students to the template
    return render_template('datalist.html', students=students)



@app.route("/FORM", methods=['GET', 'POST'])
def StuInfo():
    if request.method == 'POST':
        'add entry to DB'

        First_Name = request.form.get('First_Name')
        Last_Name = request.form.get('Last_Name')
        DEPARTMENT = request.form.get('DEPARTMENT')
        EVENT = request.form.get('EVENT')
        Email_Id = request.form.get('Email_Id')
        tele = request.form.get("tele")

        entry = Students(First_Name=First_Name, Last_Name=Last_Name, DEPARTMENT=DEPARTMENT, EVENT=EVENT,
                         Email_Id=Email_Id, tele=tele)
        db.create_all()
        db.session.add(entry)
        db.session.commit()
    return render_template('FORM.html')


@app.route ('/datalist/update/<int:tele>', methods=['GET', 'POST'])
def update(tele):
    entry = Students.query.get(tele)
    if request.method == 'POST':
        entry.First_Name = request.form.get('First_Name')
        entry.Last_Name = request.form.get('Last_Name')
        entry.DEPARTMENT = request.form.get('DEPARTMENT')
        entry.EVENT = request.form.get('EVENT')
        entry.Email_Id = request.form.get('Email_Id')
        entry.tele = request.form.get('tele')
        db.session.commit()
        return redirect(url_for('datalist'))
    return render_template('update.html',entry=entry)

@app.route("/datalist/delete/<int:tele>", methods=["POST"])
def delete(tele):
    entry = Students.query.get(tele)
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for('datalist'))




if __name__ == "__main__":
    app.run(debug=True)


