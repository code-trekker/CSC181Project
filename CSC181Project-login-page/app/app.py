from controller import *
from models import *
from forms import LoginForm, form
from werkzeug.security import generate_password_hash,check_password_hash

createDB()
createTables()

def createAdmin(): #creates admin user
    db.session.add(User(userid = "2015-0012", password=generate_password_hash('password') ))
    db.session.commit()

if User.query.filter_by(userid="2015-0012").first()==None: #prevents creating another admin user
    createAdmin()
else:
    pass


@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method=='POST' and form.validate_on_submit():
        try:
            print form.userid.data
            userid = User.query.filter_by(userid=form.userid.data).first()
            print userid.userid
            if userid.userid == form.userid.data:
                if check_password_hash(userid.password, form.password.data):
                    
                    msg = 'WHOOOO MANA JUD'
                    return render_template('success.html', msg=msg)#redirect(url_for('logged'))
                else:
                    msg = "wrong username or password"
                    return render_template("index.html",form=form, msg=msg)
            else:
                msg = "wrong username or password"
                return render_template("index.html",form=form,msg=msg)
        except:
            msg = "wrong username or password"
            return render_template("index.html", form=form, msg=msg)
    return render_template('index.html', form=form)

@app.route('/loginsuccess', methods=['GET', 'POST'])
def logged():
    pass

if __name__ == '__main__':
    app.run(debug=True)

