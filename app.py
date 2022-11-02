import datetime
from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import xmlrpc.client
# from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
# from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'
db = SQLAlchemy(app)

s = xmlrpc.client.ServerProxy('http://localhost:8000')

class TrainingForm(FlaskForm):
    sessionName = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Session Name"})
    dataSetName = StringField(validators=[
                            InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Data Set Name"})

    submit = SubmitField('Start Training')

class TrainingSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sessionName = db.Column(db.String(20), nullable=False, unique=True)
    dataSetName = db.Column(db.String(80), nullable=False)
    timeStamp = db.Column(db.DateTime, nullable=False)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/control_panel', methods=['GET', 'POST'])
def control_panel():
    form = TrainingForm()
    if form.validate_on_submit():
        new_session = TrainingSession(
            sessionName=form.sessionName.data, 
            dataSetName=form.dataSetName.data, 
            timeStamp=datetime.datetime.now())
        print(new_session.sessionName)
        # new process call
        s.train()
        # requests.get("146.", 
        #     params={
        #         'sessionName': form.sessionName.data, 
        #         'dataSetName': form.dataSetName.data})
        db.session.add(new_session)
        db.session.commit()
        return redirect(url_for('training_log'))
    return render_template('control_panel.html', form=form)


@app.route("/training_logs", methods=['GET'])
def training_log():
    all_sessions = TrainingSession.query.all()
    for session in all_sessions:
        print(session.sessionName)
    return render_template('training_log.html', all_sessions=all_sessions)


if __name__ == "__main__":
    app.run(debug=True)