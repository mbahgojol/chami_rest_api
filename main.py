from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse
from flask.ext.mysql import MySQL



mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'eky123'
app.config['MYSQL_DATABASE_PASSWORD'] = 'roti1212'
app.config['MYSQL_DATABASE_DB'] = 'chami-dev-db'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'


mysql.init_app(app)

api = Api(app)

class AuthUser(Resource):
    def post(self):
        try:
            # Parse the arguments

            parser = reqparse.RequestParser()
            parser.add_argument('nameagent', type=str , help='Nama Agent')
            parser.add_argument('username', type=str, help='Username Agent')
            parser.add_argument('password', type=str, help='Password Agent')
            parser.add_argument('tier', type=int, help='Tier Agent')
            parser.add_argument('email', type=str, help='Email Agent')
            args = parser.parse_args()

            _userAgent = args['name']
            _userName = args['username']
            _userPassword = args['password']
            _userTier  = args['tier']
            _userEmail = args['email']

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_AuthenticateUser',(_userAgent, _userName, _userPassword, _userTier, _userEmail))
            data = cursor.fetchall()

            
            if(len(data)>0):
                if(str(data[0][3])==_userPassword):
                    return {'status':200,'UserId':str(data[0][0][0][0][0])}
                else:
                    return {'status':100,'message':'Authentication failure'}

        except Exception as e:
            return {'error': str(e)}

class Register(Resource):
    def post(self):
        try:
            # Parse the arguments
            parser = reqparse.RequestParser()
            parser.add_argument('nameagent', type=str , help='Nama Agent')
            parser.add_argument('username', type=str, help='Username Agent')
            parser.add_argument('password', type=str, help='Password Agent')
            parser.add_argument('tier', type=int, help='Tier Agent')
            parser.add_argument('email', type=str, help='Email Agent')
            args = parser.parse_args()

            _userAgent = args['name']
            _userName = args['username']
            _userPassword = args['password']
            _userTier  = args['tier']
            _userEmail = args['email']

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('spCreateUser',(_userAgent, _userName, _userPassword, _userTier, _userEmail))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return {'StatusCode':'200','Message': 'User creation success'}
            else:
                return {'StatusCode':'1000','Message': str(data[0])}

        except Exception as e:
            return {'error': str(e)}



api.add_resource(Register, '/Register')
api.add_resource(AuthUser, '/AuthUser')

if __name__ == '__main__':
    app.run(debug=True)