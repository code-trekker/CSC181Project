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
    return redirect(url_for('viewreg'))

@app.route('/adminhome')
@login_required
def adminhome():
    msg = 'Login successful! The current user is ' + str(current_user.userid)
    return render_template('adminhomepage.html', msg=msg)

@app.route('/adminbudgets')
@login_required
def adminbudgets():
    query = Budget.query.filter_by(Organization_orgCode=current_user.orgCode).order_by(Budget.schoolyear)
    return render_template('budgets.html', query=query)

@app.route('/newbudget', methods=['GET', 'POST'])
@login_required
def newbudget():
    form = NewBudget()
    msgs = ''
    if request.method=='POST' and form.validate_on_submit():
        check = Budget.query.filter_by(schoolyear=form.schoolyear.data, semester=form.semester.data).first()
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
    query = Event.query.filter_by(Event_orgCode=current_user.orgCode).order_by(Event.eventid)
    return render_template('events.html', query=query)

@app.route('/newevent', methods=['GET','POST']) #DONE
@login_required
def newevent():
    form = NewEvent()
    msgs = ''
    if request.method=='POST' and form.validate_on_submit():
        check = Event.query.filter_by(eventid=form.eventid.data).first()
        if check is None:
            db.session.add(Event(eventid=form.eventid.data, eventName=form.eventName.data, eventDate=form.eventDate.data, allocation=form.allocation.data, Event_orgCode=current_user.orgCode))
            db.session.commit()
            return redirect(url_for('adminevents'))
        elif check.eventid == form.eventid.data:
            msgs = 'ID already exists in the system!'
            return render_template('events_new.html', form=form, msgs=msgs)
    return render_template('events_new.html', form=form, msgs=msgs)

@app.route('/updateevent', methods=['GET', 'POST'])
def updateevent():
    form = NewEvent()
    msgs =''
    if request.method=='POST' and form.validate_on_submit():
        check = Event.query.filter_by(eventid=form.eventid.data).first()
        if check is None:
            msgs = 'Event does not exist!'
            return render_template('events_update.html', form=form, msgs=msgs)
        elif check.eventid == form.eventid.data:
            check.eventName = form.eventName.data
            check.eventDate = form.eventDate.data
            check.allocation = form.allocation.data
            db.session.commit()
            return redirect(url_for('adminevents'))
    return render_template('events_update.html', form=form, msgs=msgs)

@app.route('/deleteevent', methods=['GET','POST'])
def deleteevent():
    form = DelEvent()
    msgs = ''
    if request.method=='POST' and form.validate_on_submit():
        check = Event.query.filter_by(eventid=form.eventid.data).first()
        if check is None:
            msgs = 'Event does not exist!'
            return render_template('events_delete.html', form=form, msgs=msgs)
        elif check.eventid == form.eventid.data:
            Event.query.filter_by(eventid=form.eventid.data).delete()
            db.session.commit()
            return redirect(url_for('adminevents'))
    return render_template('events_delete.html', form=form, msgs=msgs)

@app.route('/adminexpenses')
@login_required
def adminexpenses():
    return render_template('expenses.html')



@app.route('/admincollection')
@login_required
def admincollection():
    return render_template('collection.html')

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

@app.route('/adminmembers')
@login_required
def adminmembers():
    return render_template('members.html')

@app.route('/viewhome', methods=['GET', 'POST'])
def viewhome():
    return "EMPTY"

if __name__ == '__main__':
    app.run(debug=True)


