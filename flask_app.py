# A very simple Flask Hello World app for you to get started with...

from flask import Flask, redirect, render_template, request, url_for
from flask import jsonify
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, current_user, LoginManager, UserMixin, login_required, logout_user
from flask_migrate import Migrate
from werkzeug.security import check_password_hash, generate_password_hash

import commands

import datetime

cmd = commands.Commands()

app = Flask(__name__)

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="animbuddy",
    password="asdfqwer",
    hostname="animbuddy.mysql.pythonanywhere-services.com",
    databasename="animbuddy$animBuddyData",
    #databasename="animbuddy$dummyempty",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.secret_key = "animbroodyisoneofthebesttoolintheworldreally"
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(128))
    trialused = db.Column(db.Boolean, unique=False, default=True)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username

class AnimBuddyData(db.Model):

    __tablename__ = "animBuddyData"

    id = db.Column(db.Integer, primary_key=True)
    license = db.Column(db.String(4096))
    initiated = db.Column(db.DateTime, default=datetime.datetime.now)
    expiry = db.Column(db.DateTime, default=datetime.datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    user = db.relationship('User', foreign_keys=user_id)

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(username=user_id).first()

comments = []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("main_page.html", comments=AnimBuddyData.query.all())

    if "contents" in request.form.to_dict():
        comment = AnimBuddyData(license=request.form["contents"],
                                expiry=datetime.datetime.now() + datetime.timedelta(days=30),
                                user=current_user)
        db.session.add(comment)
        db.session.commit()
    elif "id" in request.form.to_dict():
        comment = AnimBuddyData.query.filter_by(id=int(request.form["id"])).first()
        db.session.delete(comment)
        db.session.commit()
    return redirect(url_for('index'))

@app.route("/users", methods=["GET", "POST"])
def usersTable():
    if request.method == "GET":
        return render_template("user_page.html", comments=User.query.all())

@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login_page.html", error=False)

    user = load_user(request.form["username"])
    if user is None:
        return render_template("login_page.html", error=True)

    if not user.check_password(request.form["password"]):
        return render_template("login_page.html", error=True)

    login_user(user)
    return redirect(url_for('index'))

@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))













def generateKey(keyLength=24):
    """
    """
    import random
    Alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    chars = []
    for i in range(keyLength):
        chars.append(Alphabet[random.randrange(len(Alphabet))])
    return "".join(chars)


def licenseDict():
    """
    """
    licenses = {}
    for license in AnimBuddyData.query.all():
        licenses[license.license] = {}
        licenses[license.license]['initiatedDate'] = license.initiated
        licenses[license.license]['expiryDate'] = license.expiry
        licenses[license.license]['owner'] = license.user.username
        licenses[license.license]['ownerEmail'] = license.user.email
    return licenses
"""
from flask_app
from flask_app import db
updating sql data
x = AnimBuddyData.query.filter_by(license = '1111-2222-3333-4446').first()
x.expiry = datetime(1999, 10, 21, 0, 0)
db.session.commit()
"""
@app.route('/addLicense/<user>/<email>', methods=['GET'])
def addLicense(user, email):
    """
    """
    #print request.args.get('user')
    #print request.args.get('email')

    days = 30
    dbUser = User.query.filter_by(username = user).first()
    if not dbUser:
        userData = User(username = user,email = email)
        db.session.add(userData)
        db.session.commit()
        dbUser = User.query.filter_by(username = user).first()

    license = generateKey()
    data = AnimBuddyData(license=license,
                         expiry=datetime.datetime.now() + datetime.timedelta(days=days))
    db.session.add(data)
    db.session.commit()

    updatedData = AnimBuddyData.query.filter_by(license = license).first()
    updatedData.user = dbUser
    db.session.commit()

    return {'result' : 'Generated'}

def validate(key):
    """
    key validation
    """
    today = datetime.datetime.now()

    license = AnimBuddyData.query.filter_by(license = key).first()
    if not license:
        return {'result' : 'Invalid'}
    if (license.expiry - today).days + 1 >= 0:
        return {'result' : 'Valid'}
    elif (license.expiry - today).days + 1 < 0:
        return {'result' : 'Expired'}

def oldvalidate(key):
    """
    key validation
    """
    today = datetime.date.today()
    x = AnimBuddyData.query.filter_by(license = key).first()
    #licenses = [x.license for x in AnimBuddyData.query.all()]
    licenses = {'1111-2222-3333-4444':{'type':'permanent', 'expiryDate': datetime.date(2080, 12, 20)}, 'owner' : 'beaverhouse',
                '1111-2222-3333-4446':{'type':'monthly',   'expiryDate': datetime.date(2019, 12, 5),   'owner' : 'Me'},
                '1111-2222-3333-4445':{'type':'business',  'expiryDate': datetime.date(2080, 12, 7)},  'owner' : 'ho'}

    if key in licenses.keys():
        if (licenses[key]['expiryDate'] - today).days >= 0:
            return {'result' : 'Valid'}
        elif (licenses[key]['expiryDate'] - today).days < 0:
            return {'result' : 'Expired'}

    else:
        return {'result' : 'Invalid'}


@app.route('/license/<string:key>', methods=['GET'])
def returnOne(key):
    """
    only validating key
    """
    return validate(key)

@app.route('/initialize/<string:key>', methods=['GET'])
def initialize(key):
    """
    main UI init
    """
    if validate(key)['result'] == 'Valid':
        print(cmd.initialize)
        return {'result' : cmd.initialize}
    else:
        return {'result' : 'print("need valid Anim Buddy license")'}

@app.route('/runUI/<string:key>', methods=['GET'])
def runUI(key):
    """
    only validating key
    """
    if validate(key)['result'] == 'Valid':
        return {'result' : cmd.runUI}
    else:
        return {'result' : 'print("need valid Anim Buddy license")'}