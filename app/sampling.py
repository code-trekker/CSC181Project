from controller import *
from models import *


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'
login_manager.login_message='Log in required!'
login_manager.refresh_view = 'login'
login_manager.needs_refresh_message = 'You need to re-login to access this page'

createDB()
createTables()


def createAdmin(): #creates admin user
    db.session.add(User(userid = 20150012, password='password' ))
    db.session.commit()

if User.query.filter_by(userid='admin').first()==None: #prevents creating another admin user
    createAdmin()
else:
    pass

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#@app.route('/')
#def start():
#    user = User.query.filter_by(userid='admin').first()
#   login_user(user)
#   return 'You are now logged in!'
@app.route('/login')
def login():
    session['next'] = request.args.get('next')
    return render_template('login.html')

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

@app.route('/logmein', methods=['POST'])
def logmein():
    userid = request.form['userid']

    user = User.query.filter_by(userid=userid).first()

    if not user:
        return '<h1>USER NOT FOUND!</h1>'

    login_user(user, remember=True)

    if 'next' in session:
        next = session['next']
        if is_safe_url(next):
            return redirect(next)

    return '<h1>Logged in successfully!</h1>'


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'You are now logged out!'

@app.route('/home')
@login_required
def home():
    return 'The current user is ' + current_user.userid

@app.route('/fresh')
@fresh_login_required
def fresh():
    return '<h1>You have a fresh login!</h1>'

if __name__ == '__main__':
    app.run(debug=True)