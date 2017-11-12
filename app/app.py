from controller import *
from models import *
from forms import LoginForm, NewMember

createDB()
createTables()

def createAdmin(): #creates admin user
    db.session.add(User(userid = 20150012, password='password', roleid=1 ))
    db.session.commit()

if User.query.filter_by(userid=20150012).first()==None: #prevents creating another admin user
    createAdmin()
else:
    pass

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_roleid):
    return User.query.get(int(user_roleid))

@login_manager.unauthorized_handler
def unauthorized():
    return "Admin rights needed to access this page!"


@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method=='POST' and form.validate_on_submit():
        userid = User.query.filter_by(userid=20150012).first()
        passwd = User.query.filter_by(password='password').first()
        if userid.userid == int(form.userid.data):
            if passwd.password == form.password.data:
                login_user(userid, remember=True)
                msg = 'You are now logged in!'
                return render_template('success.html', msg=msg)
            else:
                return render_template('index.html', form=form)
        else:
            flash("Username or password is invalid")
            return render_template('index.html', form=form)
    return render_template('index.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    msg = "You are now logged out!"
    return render_template('logout.html', msg=msg)

@app.route('/adminhome')
@login_required
def adminhome():
    msg = 'The current user is ' + str(current_user.userid)
    return render_template('admintools.html', msg=msg)


@app.route('/viewreg', methods=['GET', 'POST'])
def viewreg():
    form = NewMember()
    if request.method == 'POST' and form.validate_on_submit():
        user = Member(memberid=int(form.memberid.data), fname=form.fname.data, mname=form.mname.data, lname=form.lname.data, course=form.course.data, orgCode=form.orgCode.data)
        db.session.add(user)
    return render_template('signup.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)

