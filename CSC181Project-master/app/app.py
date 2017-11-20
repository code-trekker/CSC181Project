from controller import *
from models import *
from forms import *
createDB()
createTables()

def createAdmin(): #creates admin user
    db.session.add(User(userid = 'scsadmin', password=generate_password_hash('wolveswolves'), orgCode='SCS' ))
    db.session.commit()

if User.query.filter_by(userid='scsadmin').first()==None: #temporary
    createAdmin()
else:
    pass

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_userid):
    try:
        return User.query.get(user_userid)
    except User.DoesNotExist:
        return None

@login_manager.unauthorized_handler
def unauthorized():
    return "Admin rights needed to access this page!"


@app.route('/', methods=['GET', 'POST'])
def viewreg():
    form = NewMember()
    msgs=''
    if request.method == 'POST' and form.validate_on_submit():
        memberid = Member.query.filter_by(memberid=int(form.memberid.data)).first()
        if memberid is None:
            member = Member(memberid=int(form.memberid.data), fname=form.fname.data, mname=form.mname.data,
                            lname=form.lname.data, course=form.course.data, orgCode=form.orgCode.data)
            db.session.add(member)
            db.session.commit()
            return redirect(url_for('viewhome'))
        elif memberid.memberid == int(form.memberid.data):
            msgs = "ID already registered!"
            return render_template('signup.html', form=form, msgs=msgs)
    return render_template('signup.html', form=form, msgs=msgs)


@app.route('/admin', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method=='POST' and form.validate_on_submit():
        userid = User.query.filter_by(userid=form.userid.data).first()
        if userid.userid == form.userid.data:
            if check_password_hash(userid.password, form.password.data):
                login_user(userid, remember=True)
                return redirect(url_for('adminhome'))
            else:
                return render_template('index.html', form=form)
        else:
            flash("Username or password is invalid")
            return render_template('index.html', form=form)
    return render_template('index.html', form=form)

@app.route('/logout')

def logout():
    logout_user()
    msg = "You are now logged out!"
    return render_template('logout.html', msg=msg)

@app.route('/adminhome')
@login_required
def adminhome():
    msg = 'Login successful! The current user is ' + str(current_user.userid)
    return render_template('adminhomepage.html', msg=msg)

@app.route('/adminbudgets')
@login_required
def adminbudgets():
    return render_template('budgets.html')

@app.route('/newbudget', methods=['GET', 'POST'])
@login_required
def newbudget():
    form = NewBudget()
    msgs = ''
    if request.method=='POST' and form.validate_on_submit():
        check = Budget.query.filter_by(schoolyear=form.schoolyear.data, semester=form.semester.data).first_or_404()
        if check is None:
            db.session.add(Budget(schoolyear=form.schoolyear.data, semester=form.semester.data, budgetBal=form.budgetBal.data, Organization_orgCode=current_user.orgCode))
            db.session.commit()
            return redirect(url_for('adminbudgets'))
        elif check.schoolyear == form.schoolyear.data and check.semester == form.semester.data:
            msgs = "Budget already exists!"
            return render_template('addbudget.html', form=form, msgs=msgs)
    return render_template('addbudget.html', form=form, msgs=msgs)

@app.route('/updatebudget', methods=['GET','POST'])
@login_required #DONE
def updatebudget():
    form = NewBudget()
    msgs=''
    if request.method=='POST' and form.validate_on_submit():
        check = Budget.query.filter_by(schoolyear=form.schoolyear.data, semester=form.semester.data).first()
        if check is None:
            msgs = 'Budget does not exist!'
            return render_template('updatebudget.html', form=form, msgs=msgs)
        elif check.schoolyear == form.schoolyear.data:
            if check.semester == form.semester.data:
                check.budgetBal = form.budgetBal.data
                db.session.commit()
                return redirect(url_for('adminbudgets'))
    return render_template('updatebudget.html', form=form, msgs=msgs)

@app.route('/adminevents')
@login_required
def adminevents():
    return render_template('events.html')

@app.route('/admincollection')
@login_required
def admincollection():
    return render_template('collection.html')

@app.route('/col',methods=['POST','GET'])
@login_required
def cre_tab():
    print "meeeeee"
    if request.method == 'POST':
        try:
            print request.form['type'],request.form['cname'],request.form['fee']
            tob_add= collection(request.form['cname'],request.form['fee'],request.form['type'])
            add_col(tob_add)
            msg = "SUCCESS"
            return render_template("added.html",msg=msg)
        except:
            msg = "error"
            return render_template("collectionx.html",msg=msg)

    return render_template('collectionx.html')

@app.route('/pay',methods=['POST','GET'])
@login_required
def pay():
    if request.method == 'POST':
        try:
            checkRow = collection.query.filter_by(col_name=request.form['cname']).first()
            print checkRow
            if checkRow:
                cid=checkRow.col_id
                print cid
                print request.form['studid']
                print request.form['date']
                ch_id=pays.query.filter_by(pcol_id=cid).first()
                ch_stud=pays.query.filter_by(studid=request.form['studid']).first()
                print ch_id.pcol_id

                if ch_id.pcol_id ==cid and ch_stud.studid==request.form['studid']:
                    msg = "student has already paid this collection"
                    return render_template("pays.html", msg=msg)
        except:
            tob_add = pays(request.form['studid'], request.form['date'])
            add_col(tob_add)
            # cname = checkRow.col_name
            # v_u(cname, request.form['studid'])
            msg = "Student with id number " + request.form['studid'] + "- PAID"
            return render_template("pays.html", msg=msg)
    return render_template('pay.html')
    

@app.route('/adminpays')
@login_required
def adminpays():
    return render_template('pays.html')

@app.route('/adminlogs')
@login_required
def adminlogs():
    return render_template('logs.html')

@app.route('/adminattendance')
@login_required
def adminattendance():
    return render_template('attendance.html')

@app.route('/adminexpenses')
@login_required
def adminexpenses():
    return render_template('budgets.html')

@app.route('/adminmembers')
@login_required
def adminmembers():
    return render_template('members.html')

@app.route('/viewhome', methods=['GET', 'POST'])
def viewhome():
    return "EMPTY"

if __name__ == '__main__':
    app.run(debug=True)

