from controller import *
from models import *
from forms import LoginForm, form

createDB()
createTables()

def createAdmin(): #creates admin user
    db.session.add(User(userid = 20150012, password='password' ))
    db.session.commit()

if User.query.filter_by(userid=20150012).first()==None: #prevents creating another admin user
    createAdmin()
else:
    pass


@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method=='POST' and form.validate_on_submit():
        userid = User.query.filter_by(userid=20150012).first()
        passwd = User.query.filter_by(password='password').first()
        if userid.userid == int(form.userid.data):
            if passwd.password == form.password.data:
                print "error"
                msg = 'WHOOOO MANA JUD'
                return render_template('success.html', msg=msg)#redirect(url_for('logged'))
    return render_template('index.html', form=form)

@app.route('/loginsuccess', methods=['GET', 'POST'])
def logged():
    pass

if __name__ == '__main__':
    app.run(debug=True)

