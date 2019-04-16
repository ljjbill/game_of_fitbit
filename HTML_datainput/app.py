# import necessary libraries
from sqlalchemy import func

from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db/vital.sqlite"

db = SQLAlchemy(app)


class Vital(db.Model):
    __tablename__ = 'vital'

    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer)
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)

    def __repr__(self):
        return '<Vital %r>' % (self.name)


@app.before_first_request
def setup():
    # Recreate database each time for demo
    db.drop_all()
    db.create_all()


# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")


# Query the database and send the jsonified results
@app.route("/send", methods=["GET", "POST"])
def send():
    db.drop_all()
    db.create_all()
    if request.method == "POST":
        age = request.form["userAge"]
        height = request.form["userHeight"]
        weight = request.form["userWeight"]
        vital = Vital(age=age, height=height, weight=weight)
        db.session.add(vital)
        db.session.commit()
        return redirect("/api/vitals", code=302)

    return render_template("form.html")


# create route that returns data for plotting
@app.route("/api/vitals")
def pals():
   

    results = db.session.query(Vital.age,Vital.height,Vital.weight).all()

    age = [result[0] for result in results]
    height = [result[1] for result in results]
    weight = [result[2] for result in results]

    trace = {
        "age": age,
        "height": height,
        "weight": weight
    }

    return jsonify(trace)


if __name__ == "__main__":
    app.run()
