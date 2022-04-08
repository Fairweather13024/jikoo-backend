import os
import flask_sqlalchemy
import flask_praetorian
import flask_cors
import jwt
import datetime
from flask import Flask, redirect, url_for, request, make_response, abort, jsonify
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, logout_user, login_user
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from sqlalchemy_imageattach.entity import Image, image_attachment
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from functools import wraps


#allows the front and ackend servers to communicate effectively between themselves
cors = flask_cors.CORS()

# Initialize flask app 
app = Flask(__name__)

login_manager = LoginManager()

#Token configuration 
app.config['SECRET_KEY'] = 'h8cwe9fujcimdsjf'
app.config['JWT_ACCESS_LIFESPAN'] = {'hours': 24}
app.config['JWT_REFRESH_LIFESPAN'] = {'days': 30}
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = flask_sqlalchemy.SQLAlchemy(app)


login_manager.init_app(app)
login_manager.login_view = 'login'





class User(db.Model, UserMixin):
    __tabelname__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True, index = True)#we want unique emails for resetting accounts
    password = db.Column(db.Text)
    grad_year = db.Column(db.Integer)
    current_work = db.Column(db.Integer)
    admin_auth = db.Column(db.Boolean)
    resume = db.Column(db.VARBINARY)
    resume_public = db.Column(db.Boolean)
    image = image_attachment('UserPicture')
    cover = image_attachment('UserCover')

    roles = db.Column(db.Text)


    def __repr__(self):
        return '<User %r>' % self.name


    def __init__(self, email, name, password):
        '''
        Constructor for the user object as will be passed in from the
        registration form
        The Werkzeug hahsing methods will be used to store hashed passwords 
        & check incoming passwords
        '''
        self.email = email
        self.name = name
        self.password_hash = generate_password_hash(password)#hashing passwords before storage



    def check_password(self, password):
        '''
        Checks the hashed password value in storage against the password that is passed
        '''
        return check_password_hash(self.password_hash, password)

    #The following are helper functions that allow the view functions to quickly check and process the information in the requests
    @classmethod
    def lookup(cls, email):
        '''
        Getting users by their unique emails
        '''
        return cls.query.filter_by(email=email).one_or_none()

    @classmethod
    def identify(cls, id):
        '''
        Getting a user by their id
        '''
        return cls.query.get(id)

    @property
    def identity(self):
        '''
        Returning the id of the user in order to compare it with the current user in the client session (match.params.id)
        '''
        return self.id

    @property
    def rolenames(self):
        '''
        Helper fucntion to call and display the roles that the user may have
        '''
        try:
            return self.roles.split(',')
        except:
            return []


class UserPicture(db.Model, Image):
    """
    Model for the user's avatar/picture
    This should drastically imporve recognizability when someone arrives on the app
    """
    user_id = db.Column(db.Integer, ForeignKey('user.id'), primary_key = True)
    user = relationship('User')

class UserCover(db.Model, Image):
    """
    Model for the user's cover picture
    
    """
    user_id = db.Column(db.Integer, ForeignKey('user.id'), primary_key = True)
    user = relationship('User')


#creating a token required decorator for every view that needs a logged in user to access/post data
def token_required(f):
    '''
    This decorator grabs the token from the request header and tries to decode it with
    the secret key to verify that the current user has a valid token which would allow them 
    to access certain routes
    '''
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token') #gets the token from the request header eg localhost:5000/route?token = uasgdbwibciwlcbnwlcu

        if not token:
            return jsonify({'message': 'Token is missing'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message': 'Token is invalid'}), 403
        return f(*args, **kwargs)
    return decorated

###################
# Routes
@app.route('/api', methods=['GET'])
def home():
    """
    Test route to show that the server is connected too the front end server
    """
    return {
        'name': 'Hello world'
    }


#Rouet to add teh logged in user to the 
@app.route('/api/login', methods=['POST'])
def login():
    """
    Logs a user in by parsing a POST request containing user credentials and
    issuing a JWT token.
    .. example::
       $ curl http://localhost:5000/api/login -X POST \
         -d '{"email":"whatever email","password":"strongpassword&^%*&2564161"}'
    """

    request = request.get_json(force=True)
    emailLogin = request.get('email')
    passwordLogin = request.get('password')

    current_user = User.query.filter_by(emailLogin).first()

    #check if the password is correct and the data is supplied
    if current_user.check_password(passwordLogin) and current_user is not none:
        #creating a json web token which stores the current user
        token = jwt.encode({'user': current_user, 'exp': datetime.datetime.utcnow()+ datetime.timedelta(hours=24)}, app.config['SECRET_KEY'])

        login_user(current_user)
        return jsonify({'token': token.decode('UTF-8')})
    return make_response('Login unsuccessful', 401)

        




@app.route('/api/register', methods=['POST'])
def register():
    """
    Registers a user based on the user model
    .. example::
       $ curl http://localhost:5000/api/register -X POST \
         -d '{"name": "Some name", email":"whatever email","password":"strongpassword&^%*&2564161"}'
    """
    req = request.get_json(force=True)
    print(req)
    nameRegister = req.get('name', None)
    emailRegister = req.get('email', None)
    passwordRegister = req.get('password', None)
    
    new_user = User(name = nameRegister, email = emailRegister, password = passwordRegister)

    db.session.add(new_user)
    db.session.commit()
    return 'Registered'
    


@app.route('/api/logout')
def logout():
    """
    Logs out users from the current session
    """
    logout_user()
    return 'Logged out'


def users_serializer(user):
    """
    Serializes query data so that it is consumable by the front end which expects
    JSON objects or arrays
    """
    return{
    'id': user.id,   
    "name": user.name,
    "email": user.email,
    "password": user.password,
    "grad_year": user.grad_year,
    "current_work": user.current_work,
    "admin_auth": user.admin_auth,
    "resume": user.resume,
    "resume_public": user.resume_public,
    "roles": user.roles
    }

@app.route('/api/users', methods = ['GET'])
def get_all_users():
    """
    Queries the database to get all users
    We apply the serializer to each user object to return an array of JSON objects
    """
    return jsonify(list(map(users_serializer, User.query.all())))


@app.route('/api/refresh', methods=['POST'])
def refresh():
    """
    Refreshes an existing JWT by creating a new one that is a copy of the old
    except that it has a refrehsed access expiration.
    .. example::
       $ curl http://localhost:5000/api/refresh -X GET 
         -H "Authorization: Bearer <your_token>"
    """
    old_token = request.get_data()
    new_token = guard.refresh_jwt_token(old_token)
    ret = {'access_token': new_token}
    return ret, 200



# I have disabled debug mode because we will not serve a page from the flask app without it existing
if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost', port=8000)