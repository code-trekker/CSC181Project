from flask_sqlalchemy import Pagination
from sqlalchemy import join
from werkzeug.exceptions import abort

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
login_manager.login_view = '/admin'

@login_manager.user_loader
def load_user(user_userid):
    try:
        return User.query.get(user_userid)
    except User.DoesNotExist:
        return None

@login_manager.unauthorized_handler
def unauthorized():
    flash('Admin rights needed to access this page')
    return redirect(url_for('login'))


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

@app.route('/adminbudgets/', defaults={'page_num':1})
@app.route('/adminbudgets/<int:page_num>')
@login_required
def adminbudgets(page_num):
    query = Budget.query.filter_by(Organization_orgCode=current_user.orgCode).order_by(Budget.schoolyear).paginate(per_page=10, page=page_num, error_out=True)
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

@app.route('/adminevents/', defaults={'page_num':1})
@app.route('/adminevents/<int:page_num>', methods=['GET', 'POST'])
@login_required
def adminevents(page_num):
    query = Event.query.filter_by(Event_orgCode=current_user.orgCode).order_by(Event.eventDate).paginate(per_page=10, page=page_num, error_out=True)
    return render_template('events.html', query=query)

@app.route('/newevent', methods=['GET','POST']) #DONE
@login_required
def newevent():
    form = NewEvent()
    msgs = ''
    if request.method=='POST' and form.validate_on_submit():
        check = Event.query.filter_by(eventid=int(form.eventid.data)).first()
        if check is None:
            db.session.add(Event(eventid=int(form.eventid.data), eventName=form.eventName.data, eventDate=form.eventDate.data, allocation=form.allocation.data, Event_orgCode=current_user.orgCode))
            db.session.commit()
            flash(" Success! You have added a new event!")
            return redirect(url_for('adminevents'))
        elif check.eventid == int(form.eventid.data):
            msgs = 'ID already exists in the system!'
            return render_template('events_new.html', form=form, msgs=msgs)
    return render_template('events_new.html', form=form, msgs=msgs)

@app.route('/updateevent/<int:eventid>', methods=['GET', 'POST'])
def updateevent(eventid):
    form = UpEvent()
    msgs =''
    if request.method=='POST' and form.validate_on_submit():
        check = Event.query.filter_by(eventid=eventid).first()
        if check is None:
            msgs = 'Event does not exist!'
            return render_template('events_update.html', form=form, msgs=msgs)
        elif check.eventid == eventid:
            check.eventName = form.eventName.data
            check.eventDate = form.eventDate.data
            check.allocation = form.allocation.data
            db.session.commit()
            flash(' Record changes saved successfully!')
            return redirect(url_for('adminevents'))
    return render_template('events_update.html', form=form, msgs=msgs, eventid=eventid)

@app.route('/deleteevent/', defaults={'page_num':1})
@app.route('/deleteevent/<int:page_num>/<int:eventid>', methods=['GET','POST'])
def deleteevent(eventid, page_num):
    try:
        Event.query.filter_by(eventid=eventid).delete()
        db.session.commit()
        flash(' Event removed successfully!')
        return redirect(url_for('adminevents'))
    except:
        flash(' Cannot delete events that have existing expenses/attendance records!')
        query = Event.query.filter_by(Event_orgCode=current_user.orgCode).order_by(Event.eventDate).paginate(per_page=10, page=page_num, error_out=True)
        return render_template('events.html', query=query)

@app.route('/newattendance/<int:eventid>/<eventdate>', methods=['GET', 'POST'])
@login_required
def newattendance(eventid, eventdate):
    form = NewAttendance()
    if request.method=='POST' and form.validate_on_submit():
        check = Attendance.query.filter_by(memberid=form.memberid.data, eventid=eventid).first()
        if check is None:
            if form.attendtype.data=='IN':
                db.session.add(Attendance(memberid=form.memberid.data, eventid=eventid, date=eventdate, signin=form.attendtype.data, signout=None))
                db.session.commit()
                flash(' Student recorded successfully!')
                return redirect(url_for('newattendance', eventid=eventid, eventdate=eventdate))
            if form.attendtype.data=='OUT':
                db.session.add(Attendance(memberid=form.memberid.data, eventid=eventid, date=eventdate, signin=None, signout=form.attendtype.data))
                db.session.commit()
                flash(' Student recorded successfully!')
                return render_template('attendance_new.html', eventid=eventid, form=form, eventdate=eventdate)
        elif check.memberid == form.memberid.data and check.eventid==eventid:
            if form.attendtype.data == 'IN':
                check.signin = form.attendtype.data
                db.session.commit()
                flash(' Student recorded successfully!')
                return render_template('attendance_new.html', eventid=eventid, form=form, eventdate=eventdate)
            if form.attendtype.data == 'OUT':
                check.signout = form.attendtype.data
                db.session.commit()
                flash(' Student recorded successfully!')
                return render_template('attendance_new.html', eventid=eventid, form=form, eventdate=eventdate)
    return render_template('attendance_new.html', eventid=eventid, form=form, eventdate=eventdate)

@app.route('/attendancelist/<int:eventid>')
@login_required
def attendancelist(eventid):
    check = Event.query.filter_by(eventid=eventid).first()
    query = db.session.query(Attendance.signin, Attendance.signout, Attendance.memberid, Member.fname, Member.lname).outerjoin(Member, Event).filter_by(eventid=eventid).order_by(Member.lname)
    return render_template('attendance_list.html', eventid=eventid, query=query, check=check)

@app.route('/adminexpenses/', defaults={'page_num':1})
@app.route('/adminexpenses/<int:page_num>')
@login_required
def adminexpenses(page_num): #TAGGED
    query = db.session.query(Expenses.expid, Expenses.name, Expenses.amount, Expenses.date, Expenses.orNo, Event.eventName).outerjoin(Event).filter_by(Event_orgCode=current_user.orgCode)
    def paginate(query, page, per_page=10, error_out=True): #had to add this to bypass strict rules about paginating a query object LMAO
        if error_out and page < 1:
            abort(404)
        items = query.limit(per_page).offset((page - 1) * per_page).all()
        if not items and page != 1 and error_out:
            abort(404)

        # No need to count if we're on the first page and there are fewer
        # items than we expected.
        if page == 1 and len(items) < per_page:
            total = len(items)
        else:
            total = query.order_by(None).count()

        return Pagination(query, page, per_page, total, items)

    q = paginate(query, page_num)
    return render_template('expenses.html', query=q)

@app.route('/newexpense', methods=['GET', 'POST'])
@login_required
def newexpense():
    form = NewExpense(Expenses_orgCode=current_user.orgCode)
    msgs=''
    if request.method=='POST' and form.validate_on_submit():
        check = Event.query.filter_by(eventid=int(form.eid.data)).first()
        query = Expenses.query.filter_by(expid=int(form.expid.data)).first()
        if check is None:
            msgs='Event does not exist!'
            return render_template('expenses_new.html', form=form, msgs=msgs)
        elif check.eventid == int(form.eid.data) and query is None:
            db.session.add(Expenses(expid=int(form.expid.data), Expenses_eventid=form.eid.data, amount=form.amount.data, date=form.date.data,
                                    orNo=form.orNo.data, name=form.name.data, Expenses_orgCode=current_user.orgCode))
            db.session.commit()
            flash(' Record successfully added!')
            return redirect(url_for('adminexpenses'))
        elif query.expid == int(form.expid.data):
            msgs='Record already exists!'
            return render_template('expenses_new.html', form=form, msgs=msgs)
    return render_template('expenses_new.html', form=form, msgs=msgs)

@app.route('/updateexpense/<int:expid>', methods=['GET', 'POST'])
@login_required
def updateexpense(expid):
    form = UpExpense()
    msgs=''
    if request.method=='POST' and form.validate_on_submit():
        check = Expenses.query.filter_by(expid=expid).first()
        if check is None:
            msgs = 'Record does not exist!'
            return render_template('expenses_update.html', form=form, msgs=msgs)
        elif check.expid == expid:
            check.name = form.name.data
            check.amount = form.amount.data
            check.date = form.date.data
            check.orNo = form.orNo.data
            db.session.commit()
            flash(' Changes saved successfully!')
            return redirect(url_for('adminexpenses'))
    return render_template('expenses_update.html', form=form, msgs=msgs, expid=expid)

@app.route('/deleteexpense/<int:expid>', methods=['GET','POST'])
@login_required #TAGGED
def deleteexpense(expid):
    Expenses.query.filter_by(expid=expid).delete()
    db.session.commit()
    flash(' You have successfully removed a record.')
    return redirect(url_for('adminexpenses'))

@app.route('/adminmembers/', defaults={'page_num':1})
@app.route('/adminmembers/<int:page_num>')
@login_required
def adminmembers(page_num):
    query = Member.query.filter_by(orgCode=current_user.orgCode).order_by(Member.lname).paginate(per_page=10, page=page_num, error_out=True)
    return render_template('members.html', query=query)

@app.route('/admincollection/', defaults={'page_num':1})
@app.route('/admincollection/<int:page_num>')
@login_required
def admincollection(page_num):
    query = Collection.query.filter_by(Collection_orgCode = current_user.orgCode).order_by(Collection.colid).paginate(per_page=10, page=page_num, error_out=True)
    return render_template('collection.html', query=query)

@app.route('/newcollection', methods=['GET', 'POST'])
@login_required
def newcollection():
    form = NewCollection()
    if request.method == 'POST' and form.validate_on_submit():
        db.session.add(Collection(colname=form.colname.data, fee = form.fee.data, Collection_orgCode=current_user.orgCode))
        db.session.commit()
        flash(' Collection added successfully!')
        return redirect(url_for('admincollection'))
    return render_template('collection_new.html', form=form)

@app.route('/updatecollection/<int:colid>', methods=['GET', 'POST'])
@login_required
def updatecollection(colid):
    form = UpCollection()
    msgs = ''
    if request.method=='POST' and form.validate_on_submit():
        check = Collection.query.filter_by(colid=colid).first()
        if check.colid == colid:
            check.colname = form.colname.data
            check.fee = form.fee.data
            db.session.commit()
            flash(' Changes saved successfully!')
            return redirect(url_for('admincollection'))
    return render_template('collection_update.html', form=form, msgs=msgs, colid=colid)

@app.route('/deletecollection/<int:colid>', methods=['GET', 'POST'])
@login_required
def deletecollection(colid):
    try:
        Collection.query.filter_by(colid=colid).delete()
        db.session.commit()
        flash(' You have successfully removed a record.')
        return redirect(url_for('admincollection'))
    except:
        flash(' Payment records still exist for this collection!')
        return redirect(url_for('admincollection'))

@app.route('/newpayment/<int:colid>', methods=['GET', 'POST'])
@login_required
def newpayment(colid):
    form = NewPayment()
    msgs = ''
    if request.method=='POST' and form.validate_on_submit():
        check = Member.query.filter_by(memberid=form.memberid.data).first()
        if check is None:
            msgs = 'Student not yet registered!'
            return render_template('payment_new.html', form=form, colid=colid, msgs=msgs)
        else:
            db.session.add(Payments(Payments_colid=colid, Payments_memberid=form.memberid.data, datepaid=form.datetime.data, Payments_orgCode=current_user.orgCode))
            db.session.commit()
            flash(' Payment saved successfully!')
            return redirect(url_for('admincollection'))
    return render_template('payment_new.html', form=form, colid=colid, msgs=msgs)

@app.route('/viewpayment/<int:colid>', methods=['GET','POST'])
@login_required
def viewpayment(colid):
    q = db.session.query(Member.memberid, Member.fname, Member.lname, Payments.datepaid).outerjoin(Payments).filter_by(Payments_colid=colid).order_by(Member.lname)
    collectname = Collection.query.filter_by(colid=colid).first()
    return render_template('paytables.html', colid=colid, result=q, collectname=collectname)

@app.route('/deletepayment/<int:colid>', methods=['GET', 'POST'])
@login_required
def deletepayment(colid):
    Payments.query.filter_by(Payments_colid=colid).delete()
    db.session.commit()
    flash(' Successfully deleted payment records!')
    return redirect(url_for('admincollection'))

@app.route('/adminlogs')
@login_required
def adminlogs():
    return render_template('logs.html')

@app.route('/viewerlogin', methods=['GET','POST'])
def viewerlogin():
    form = ViewLogin()
    if request.method=='POST' and form.validate_on_submit():
        pass
    return render_template('viewlogin.html', form=form)

@app.route('/viewhome', methods=['GET', 'POST'])
def viewhome():
    return "EMPTY"

if __name__ == '__main__':
    app.run(debug=True)


