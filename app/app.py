import calendar

from flask_sqlalchemy import Pagination
import re
from sqlalchemy import join, func
from werkzeug.exceptions import abort
from datetime import timedelta
from controller import *
from models import *
from forms import *
import os

createDB()
createTables()

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

@app.route('/setup', methods=['GET','POST'])
def setup():
    form = AdminSetup()
    check = Organization.query.first()
    # if check is None:
    if request.method=='POST' and form.validate_on_submit():
            db.session.add(User(userid=form.username.data, password=generate_password_hash(form.password.data), orgCode=form.orgCode.data))
            db.session.add(Organization(orgCode=form.orgCode.data, orgName=form.orgName.data, description=form.description.data))
            list = form.courses.data
            print form.courses.data
            if len(list.replace(" ", "")) != 0:
                new_list = re.split(', |,| ,',list)
                for data in new_list:
                    db.session.add(Courses(coursename=data))
            else:
                db.session.add(Courses(coursename='N/A'))
            db.session.commit()
            return redirect(url_for('login'))
    # else:
    #     return redirect(url_for('viewreg'))
    return render_template('setup.html', form=form)


@app.route('/', methods=['GET', 'POST'])
def viewreg():
        form = NewMember()
        msgs=''
        description = db.session.query(Organization.description).first()
        name = db.session.query(Organization.orgName).first()
        org = db.session.query(Organization.orgCode).first()
        check = Organization.query.first()
        if check is None:
            return redirect(url_for('setup'))
        if request.method == 'POST' and form.validate_on_submit():
            memberid = Member.query.filter_by(memberid=int(form.memberid.data)).first()
            if len(str(form.memberid.data)) < 8 or len(str(form.memberid.data)) > 8:
                msgs = "ID format invalid!"
                return render_template('signup.html', form=form, msgs=msgs, desc=description, name=name)
            if memberid is None:
                if len(str(form.course.data)) == 0:
                    member = Member(memberid=int(form.memberid.data), fname=form.fname.data, mname=form.mname.data,
                                    lname=form.lname.data, course='N/A', orgCode=org.orgCode,
                                    status='ACTIVE', themeid=0)
                    db.session.add(member)
                    db.session.commit()
                    return redirect(url_for('viewerlogin'))
                else:
                    member = Member(memberid=int(form.memberid.data), fname=form.fname.data, mname=form.mname.data,
                            lname=form.lname.data, course=form.course.data, orgCode=org.orgCode, status='ACTIVE', themeid=0)
                    db.session.add(member)
                    db.session.commit()
                    return redirect(url_for('viewerlogin'))
            elif memberid.memberid == int(form.memberid.data):
                msgs = "ID already registered!"
                return render_template('signup.html', form=form, msgs=msgs, desc=description, name=name)
        return render_template('signup.html', form=form, msgs=msgs, desc=description, name=name)

@app.route('/admin', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    name = db.session.query(Organization.orgName).first()
    if request.method=='POST' and form.validate_on_submit():
        userid = User.query.filter_by(userid=form.userid.data).first()
        if userid.userid == form.userid.data:
            if check_password_hash(userid.password, form.password.data):
                login_user(userid, remember=True)
                return redirect(url_for('adminhome'))
            else:
                return render_template('index.html', form=form, name=name)
        else:
            flash("Username or password is invalid")
            return render_template('index.html', form=form, name=name)
    return render_template('index.html', form=form, name=name)

@app.route('/about')
def about():
    name = db.session.query(Organization.orgName).first()
    org = db.session.query(Organization.orgCode).first()
    return render_template('aboutpage.html', name=name, org=org)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('viewreg'))

@app.route('/adminhome')
@login_required
def adminhome():
    msgs = 'Hello there, ' + str(current_user.userid) + '!'
    return render_template('adminhomepage.html', msgs=msgs)


@app.route('/adminbudgets/')
@login_required
def adminbudgets():
    query = Budget.query.filter_by(Budget_orgCode=current_user.orgCode).order_by(Budget.schoolyear)
    return render_template('budgets.html', query=query)

@app.route('/newbudget', methods=['GET', 'POST'])
@login_required
def newbudget():
    form = NewBudget()
    msgs = ''
    if request.method=='POST' and form.validate_on_submit():
        check = Budget.query.filter_by(schoolyear=form.schoolyear.data, semester=form.semester.data).first()
        if check is None:
            db.session.add(Budget(schoolyear=form.schoolyear.data, semester=form.semester.data, budgetBal=form.budgetBal.data, Budget_orgCode=current_user.orgCode))
            db.session.commit()
            flash(' Budget recorded successfully!')
            return redirect(url_for('adminbudgets'))
        elif check.schoolyear == form.schoolyear.data and check.semester == form.semester.data:
            msgs = "Budget already exists!"
            return render_template('addbudget.html', form=form, msgs=msgs)
    return render_template('addbudget.html', form=form, msgs=msgs)

@app.route('/updatebudget', methods=['GET','POST'])
@login_required #DONE
def updatebudget():
    form = UpBudget()
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
                flash(' Updated record successfully!')
                return redirect(url_for('adminbudgets'))
    return render_template('updatebudget.html', form=form, msgs=msgs)

@app.route('/adminevents/', methods=['GET', 'POST'])
@login_required
def adminevents():
    now = datetime.datetime.now()
    if now.month >=8:
        schoolyear = str(now.year) + '-' + str(now.year + 1)
        query = Event.query.filter(Event.schoolyear >= schoolyear).order_by(Event.eventDate)
        return render_template('events.html', query=query)
    elif now.month <=7:
        schoolyear = str(now.year-1) + '-' + str(now.year)
        query = Event.query.filter(Event.schoolyear >= schoolyear).order_by(Event.eventDate)
        return render_template('events.html', query=query)

@app.route('/pastevents', methods=['GET', 'POST'])
@login_required
def pastevents():
    now = datetime.datetime.now()
    if now.month >=8:
        schoolyear = str(now.year) + '-' + str(now.year + 1)
        query = Event.query.filter(Event.schoolyear < schoolyear).order_by(Event.eventDate)
        link1 = '/adminhome'
        link2 = '/adminevents'
        return render_template('events_past.html', query=query, link1=link1, link2=link2)
    elif now.month <=7:
        schoolyear = str(now.year-1) + '-' + str(now.year)
        query = Event.query.filter(Event.schoolyear < schoolyear).order_by(Event.eventDate)
        link1 = '/adminhome'
        link2 = '/adminevents'
        return render_template('events_past.html', query=query, link1=link1, link2=link2)

@app.route('/newevent', methods=['GET','POST']) #DONE
@login_required
def newevent():
    form = NewEvent()
    now = datetime.datetime.now()
    if now.month >= 8:
        schoolyear = str(now.year)+'-'+str(now.year+1)
        if request.method=='POST' and form.validate_on_submit():
            db.session.add(Event(eventName=form.eventName.data, eventDate=form.eventDate.data, allocation=form.allocation.data,
                             Event_orgCode=current_user.orgCode, schoolyear=schoolyear))
            db.session.commit()
            flash(" Success! You have added a new event!")
            return redirect(url_for('adminevents'))
    elif now.month <=7:
        schoolyear = str(now.year-1) + '-' + str(now.year)
        if request.method == 'POST' and form.validate_on_submit():
            db.session.add(
                Event(eventName=form.eventName.data, eventDate=form.eventDate.data, allocation=form.allocation.data,
                      Event_orgCode=current_user.orgCode, schoolyear=schoolyear))
            db.session.commit()
            flash(" Success! You have added a new event!")
            return redirect(url_for('adminevents'))
    return render_template('events_new.html', form=form)

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


@app.route('/deleteevent/<int:eventid>', methods=['GET','POST'])
def deleteevent(eventid):
    try:
        Event.query.filter_by(eventid=eventid).delete()
        db.session.commit()
        flash(' Event removed successfully!')
        return redirect(url_for('adminevents'))
    except:
        flash(' Cannot delete events that have existing expenses/attendance records!')
        query = Event.query.filter_by(Event_orgCode=current_user.orgCode).order_by(Event.eventDate)
        return render_template('events.html', query=query)

@app.route('/adminattendance',methods=['POST', 'GET']) #datatables
@login_required
def adminattendance():
    form = AdminAttendance()
    msgs = ''
    if request.method=='POST' and form.validate_on_submit():
        now=datetime.datetime.now()
        query =Event.query.filter_by(eventName=str(form.ev_name.data)).first()
        check = Attendance.query.filter_by(memberid=form.memberid.data, eventid=query.eventid).first()
        member = Member.query.filter_by(memberid=form.memberid.data).first()
        if member is None:
            msgs = 'Student does not exist!'
            return render_template('adminattendance.html', form=form, msgs=msgs)
        if check is None:
            if form.attendtype.data == 'IN':
                db.session.add(Attendance(memberid=form.memberid.data, eventid=query.eventid, date=now.strftime("%Y-%m-%d %H:%M"),
                                          signin=form.attendtype.data, signout=None))
                db.session.commit()
                msgs='Student recorded successfully!'
                return render_template('adminattendance.html',form=form, msgs=msgs)
            if form.attendtype.data == 'OUT':
                db.session.add(Attendance(memberid=form.memberid.data, eventid=query.eventid, date=now.strftime("%Y-%m-%d %H:%M"), signin=None,
                                          signout=form.attendtype.data))
                db.session.commit()
                msgs='Student recorded successfully!'
                return render_template('attendance_new.html',form=form, msgs=msgs)
        elif check.memberid == form.memberid.data and check.eventid == query.eventid:
            if form.attendtype.data == 'IN':
                check.signin = form.attendtype.data
                db.session.commit()
                msgs='Student recorded successfully!'
                return render_template('adminattendance.html',form=form, msgs=msgs)
            if form.attendtype.data == 'OUT':
                check.signout = form.attendtype.data
                db.session.commit()
                msgs='Student recorded successfully!'
                return render_template('adminattendance.html',form=form, msgs=msgs)
    return render_template('adminattendance.html', form=form, msgs=msgs)


@app.route('/newattendance/<int:eventid>/<eventdate>', methods=['GET', 'POST'])
@login_required
def newattendance(eventid, eventdate):
    form = NewAttendance()
    msgs = ""
    if request.method=='POST' and form.validate_on_submit():
        check = Attendance.query.filter_by(memberid=form.memberid.data, eventid=eventid).first()
        query = Member.query.filter_by(memberid=form.memberid.data).first()
        if query is None:
            msgs = 'Student does not exist!'
            return render_template('attendance_new.html', eventid=eventid, form=form, eventdate=eventdate, msgs=msgs)
        if check is None:
            if form.attendtype.data=='IN':
                db.session.add(Attendance(memberid=form.memberid.data, eventid=eventid, date=eventdate, signin=form.attendtype.data, signout=None))
                db.session.commit()
                msgs='Student recorded successfully!'
                return redirect(url_for('newattendance', eventid=eventid, eventdate=eventdate))
            if form.attendtype.data=='OUT':
                db.session.add(Attendance(memberid=form.memberid.data, eventid=eventid, date=eventdate, signin=None, signout=form.attendtype.data))
                db.session.commit()
                msgs = 'Student recorded successfully!'
                return render_template('attendance_new.html', eventid=eventid, form=form, eventdate=eventdate, msgs=msgs)
        elif check.memberid == form.memberid.data and check.eventid==eventid:
            if form.attendtype.data == 'IN':
                check.signin = form.attendtype.data
                db.session.commit()
                msgs = 'Student recorded successfully!'
                return render_template('attendance_new.html', eventid=eventid, form=form, eventdate=eventdate, msgs=msgs)
            if form.attendtype.data == 'OUT':
                check.signout = form.attendtype.data
                db.session.commit()
                msgs = 'Student recorded successfully!'
                return render_template('attendance_new.html', eventid=eventid, form=form, eventdate=eventdate, msgs=msgs)
    return render_template('attendance_new.html', eventid=eventid, form=form, eventdate=eventdate, msgs=msgs)

@app.route('/attendancelist/<int:eventid>/')
@login_required
def attendancelist(eventid):
    check = Event.query.filter_by(eventid=eventid).first()
    query = db.session.query(Attendance.signin, Attendance.signout, Attendance.memberid,
                             Member.fname, Member.lname).outerjoin(Member, Event).filter_by(eventid=eventid).order_by(Member.lname)

    return render_template('attendance_list.html', eventid=eventid, query=query, check=check)

@app.route('/pastattendance/<int:eventid>')
@login_required
def pastattendance(eventid):
    check = Event.query.filter_by(eventid=eventid).first()
    query = db.session.query(Attendance.signin, Attendance.signout, Attendance.memberid, Member.fname,
                             Member.lname).outerjoin(Member, Event).filter_by(eventid=eventid).order_by(Member.lname)
    return render_template('attendance_list_past.html', eventid=eventid, query=query, check=check)
@app.route('/adminexpenses/')
@login_required
def adminexpenses():
    now = datetime.datetime.now()
    if now.month >=8:
        schoolyear = str(now.year) + '-' + str(now.year + 1)
        query = db.session.query(Expenses.expid, Expenses.name, Expenses.amount, Expenses.date, Expenses.orNo, Event.eventName).outerjoin(Event).filter(Event.schoolyear >= schoolyear)
        return render_template('expenses.html', query=query)
    elif now.month <=7:
        schoolyear = str(now.year-1) + '-' + str(now.year)
        query = db.session.query(Expenses.expid, Expenses.name, Expenses.amount, Expenses.date, Expenses.orNo,
                                 Event.eventName).outerjoin(Event).filter(Event.schoolyear >= schoolyear)
        return render_template('expenses.html', query=query)

@app.route('/pastexpenses')
@login_required
def pastexpenses():
    now = datetime.datetime.now()
    if now.month >=8:
        schoolyear = str(now.year) + '-' + str(now.year + 1)
        query = db.session.query(Expenses.expid, Expenses.name, Expenses.amount, Expenses.date, Expenses.orNo,
                             Event.eventName).outerjoin(Event).filter(Event.schoolyear < schoolyear)
        link1 = '/adminhome'
        link2 = '/adminexpenses'
        return render_template('expenses_past.html', query=query, link1=link1, link2=link2)
    elif now.month <=7:
        schoolyear = str(now.year) + '-' + str(now.year + 1)
        query = db.session.query(Expenses.expid, Expenses.name, Expenses.amount, Expenses.date, Expenses.orNo,
                                 Event.eventName).outerjoin(Event).filter(Event.schoolyear < schoolyear)
        link1 = '/adminhome'
        link2 = '/adminexpenses'
        return render_template('expenses_past.html', query=query, link1=link1, link2=link2)

@app.route('/newexpense', methods=['GET', 'POST'])
@login_required
def newexpense():
    form = NewExpense(Expenses_orgCode=current_user.orgCode)
    now = datetime.datetime.now()
    query = Event.query.filter_by(eventName=str(form.eid.data)).first()
    msgs=''
    if now.month >=8:
        schoolyear = str(now.year) + '-' + str(now.year + 1)
        if request.method=='POST' and form.validate_on_submit():
            db.session.add(Expenses(Expenses_eventid=query.eventid, amount=form.amount.data, date=form.date.data,
                                    orNo=form.orNo.data, name=form.name.data, Expenses_orgCode=current_user.orgCode, schoolyear=schoolyear))
            db.session.commit()
            flash(' Record successfully added!')
            return redirect(url_for('adminexpenses'))
    elif now.month <=7:
        schoolyear = str(now.year) + '-' + str(now.year + 1)
        if request.method=='POST' and form.validate_on_submit():
            db.session.add(Expenses(Expenses_eventid=query.eventid, amount=form.amount.data, date=form.date.data,
                                    orNo=form.orNo.data, name=form.name.data, Expenses_orgCode=current_user.orgCode, schoolyear=schoolyear))
            db.session.commit()
            flash(' Record successfully added!')
            return redirect(url_for('adminexpenses'))
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


@app.route('/adminmembers/')
@login_required
def adminmembers():
    query = Member.query.filter_by(status='ACTIVE').order_by(Member.lname)
    return render_template('members.html', query=query)


@app.route('/admincollection/', methods=['GET', 'POST'])
@login_required
def admincollection():
    now = datetime.datetime.now()
    if now.month >= 8:
        schoolyear = str(now.year) + '-' + str(now.year + 1)
        query = Collection.query.filter(Collection.schoolyear >= schoolyear).order_by(Collection.colid).all()
        check = db.session.query(Collection.colid, Payments.Payments_colid)
        return render_template('collection.html', query=query)
    elif now.month <=7:
        schoolyear = str(now.year-1) + '-' + str(now.year)
        query = Collection.query.filter(Collection.schoolyear >= schoolyear).order_by(Collection.colid).all()
        check = db.session.query(Collection.colid, Payments.Payments_colid)
        return render_template('collection.html', query=query)

@app.route('/pastcollection')
@login_required
def pastcollection():
    now = datetime.datetime.now()
    if now.month >= 8:
        schoolyear = str(now.year) +  '-' + str(now.year + 1)
        query = Collection.query.filter(Collection.schoolyear < schoolyear).order_by(Collection.schoolyear)
        return render_template('collection_past.html', query=query)
    elif now.month <=7:
        schoolyear = str(now.year-1) + '-' + str(now.year)
        query = Collection.query.filter(Collection.schoolyear < schoolyear).order_by(Collection.schoolyear)
        return render_template('collection_past.html', query=query)


@app.route('/newcollection', methods=['GET', 'POST'])
@login_required
def newcollection():
    form = NewCollection()
    now = datetime.datetime.now()
    if now.month >= 8:
        schoolyear = str(now.year)+'-'+str(now.year+1)
        if request.method == 'POST' and form.validate_on_submit():
            db.session.add(Collection(colname=form.colname.data, fee = form.fee.data, Collection_orgCode=current_user.orgCode, schoolyear=schoolyear, amountcollected=0))
            db.session.commit()
            flash(' Collection added successfully!')
            return redirect(url_for('admincollection'))
    elif now.month <=7:
        schoolyear = str(now.year-1)+'-'+str(now.year)
        if request.method == 'POST' and form.validate_on_submit():
            db.session.add(Collection(colname=form.colname.data, fee = form.fee.data, Collection_orgCode=current_user.orgCode, schoolyear=schoolyear, amountcollected=0))
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
            # check.fee = form.fee.data
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

@app.route('/adminpayment', methods=['GET','POST'])
@login_required
def adminpayment():
    form = AdminPayment()
    if request.method=="POST" and form.validate_on_submit():
        check = Member.query.filter_by(memberid=form.memberid.data).first()
        colid = Collection.query.filter_by(colname = form.colname.data).first()
        payment = Payments.query.filter_by(Payments_memberid=form.memberid.data, Payments_colid=colid.colid).first()
        if check is None:
            msgs = 'Student does not exist!'
            return render_template('adminpayment.html', form=form, msgs=msgs)
        elif payment is not None:
            msgs = 'Student has already paid!'
            return render_template('adminpayment.html', form=form, msgs=msgs)
        else:
            query = Collection.query.filter_by(colname=str(form.colname.data)).first()
            now = datetime.datetime.now()
            db.session.add(Payments(Payments_colid=query.colid, Payments_memberid=form.memberid.data,
                                    datepaid=now.strftime("%Y-%m-%d"), Payments_orgCode=current_user.orgCode))
            increment = Collection.query.filter_by(colid=query.colid).first()
            increment.amountcollected += increment.fee
            db.session.commit()
            db.session.commit()
            msgs='Payment saved successfully!'
            return render_template('adminpayment.html', form=form, msgs=msgs)
    return render_template('adminpayment.html', form=form)

@app.route('/newpayment/<int:colid>', methods=['GET', 'POST'])
@login_required
def newpayment(colid):
    form = NewPayment()
    msgs = ''
    if request.method=='POST' and form.validate_on_submit():
        check = Member.query.filter_by(memberid=form.memberid.data).first()
        payment = Payments.query.filter_by(Payments_memberid=form.memberid.data, Payments_colid=colid).first()
        if check is None:
            msgs = 'Student not yet registered!'
            return render_template('payment_new.html', form=form, colid=colid, msgs=msgs)
        elif payment is not None:
            msgs = 'Student has already paid!'
            return render_template('payment_new.html', form=form, colid=colid, msgs=msgs)
        else:
            db.session.add(Payments(Payments_colid=colid, Payments_memberid=form.memberid.data, datepaid=form.datetime.data, Payments_orgCode=current_user.orgCode))
            increment = Collection.query.filter_by(colid=colid).first()
            increment.amountcollected += increment.fee
            db.session.commit()
            flash(' Payment saved successfully!')
            return redirect(url_for('admincollection'))
    return render_template('payment_new.html', form=form, colid=colid, msgs=msgs)


@app.route('/viewpayment/<int:colid>/', methods=['GET','POST'])
@login_required
def viewpayment(colid):
    query = db.session.query(Member.memberid, Member.fname, Member.lname, Payments.datepaid, Payments.Payments_colid, Payments.pid).outerjoin(Payments).filter_by(Payments_colid=colid).order_by(Member.lname)
    collectname = Collection.query.filter_by(colid=colid).first()
    return render_template('paytables.html', colid=colid, result=query, collectname=collectname)

@app.route('/pastpayment/<int:colid>', methods=['GET', 'POST'])
@login_required
def pastpayment(colid):
    query = db.session.query(Member.memberid, Member.fname, Member.lname, Payments.datepaid, Payments.Payments_colid,
                             Payments.pid).outerjoin(Payments).filter_by(Payments_colid=colid).order_by(Member.lname)
    collectname = Collection.query.filter_by(colid=colid).first()
    return render_template('payment_past.html', colid=colid, result=query, collectname=collectname)


@app.route('/deletepayment/<int:pid>', methods=['GET', 'POST'])
@login_required
def deletepayment(pid):
    query = Payments.query.filter_by(pid=pid).first()
    Payments.query.filter_by(pid=pid).delete()
    decrement = Collection.query.filter_by(colid=query.Payments_colid).first()
    decrement.amountcollected -= decrement.fee
    db.session.commit()
    flash(' Successfully removed!')
    return redirect(url_for('viewpayment', colid=query.Payments_colid))


@app.route('/adminlogs/')
@login_required
def adminlogs():
    now = datetime.datetime.now()
    if now.month >=8:
        schoolyear = str(now.year) + '-08' + '-01' + ' 12:00 AM'
        query = Logs.query.filter(Logs.dnt >= schoolyear).order_by(Logs.i)
        return render_template('logs.html', query=query)
    elif now.month <=7:
        schoolyear = str(now.year-1) + '-07' + '-30' + ' 12:00 AM'
        query = Logs.query.filter(Logs.dnt <= schoolyear).order_by(Logs.i)
        return render_template('logs.html', query=query)

@app.route('/deactivate', methods=['GET', 'POST'])
@login_required
def deactivate():
    form = Deactivator()
    if request.method=='POST' and form.validate_on_submit():
        query = User.query.filter_by(userid=current_user.userid).first()
        if check_password_hash(query.password, form.password.data):
            for row in Member.query.all():
                row.status = 'INACTIVE'
                db.session.add(row)
            db.session.commit()
            flash(' Members deactivated successfully!')
            return redirect(url_for('adminmembers'))
        else:
            flash(' Incorrect password!')
            return render_template('deactivate.html', form=form)
    return render_template('deactivate.html', form=form)

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=120)

@app.route('/viewerlogin', methods=['GET','POST'])
def viewerlogin():
    form = ViewLogin()
    name = db.session.query(Organization.orgName).first()
    if request.method=='POST' and form.validate_on_submit():
        session.pop('user', None)
        check = Member.query.filter_by(memberid=form.memberid.data).first()
        if check is None:
            flash('This student is not registered yet!')
            return render_template('viewlogin.html', form=form, name=name)
        else:
            now = datetime.datetime.now()
            addis = Logs(idno=check.memberid, fname=check.fname, lname=check.lname, dnt=now.strftime("%Y-%m-%d %H:%M %p"), orgCode=check.orgCode)
            db.session.add(addis)
            db.session.commit()
            session['user'] = check.fname
            session['memberid'] = check.memberid
            session['themeid'] = check.themeid
            return redirect(url_for('viewhome'))
    return render_template('viewlogin.html', form=form, name=name)


@app.route('/swaptheme/<int:themeid>', methods=['GET', 'POST'])
def swaptheme(themeid):
    member = Member.query.filter_by(memberid=session['memberid']).first()
    print(session['memberid'])
    member.themeid = themeid
    db.session.commit()
    session['themeid'] = themeid
    return "hahahah"

@app.route('/viewhome', methods=['GET', 'POST'])
def viewhome():
    form = ViewLogin()
    if 'user' in session:
        return render_template("viewerhomepage.html")
    else:
        flash('Log in again to access this page')
        return redirect(url_for('viewerlogin'))

@app.route('/viewbudgets', methods=['GET', 'POST'])
def viewbudgets():
    query = Budget.query.filter().order_by(Budget.schoolyear)
    return render_template("viewer_budgets.html", query=query)

@app.route('/viewexpenses', methods=['GET', 'POST'])
def viewexpenses():
    now = datetime.datetime.now()
    if now.month >=8:
        schoolyear = str(now.year) + '-' + str(now.year + 1)
        query = db.session.query(Expenses.expid, Expenses.name, Expenses.amount, Expenses.date, Expenses.orNo,
                             Event.eventName).outerjoin(Event).filter(Event.schoolyear >= schoolyear)
        return render_template('viewer_expenses.html', query=query)
    elif now.month <=7:
        schoolyear = str(now.year-1) + '-' + str(now.year)
        query = db.session.query(Expenses.expid, Expenses.name, Expenses.amount, Expenses.date, Expenses.orNo,
                                 Event.eventName).outerjoin(Event).filter(Event.schoolyear >= schoolyear)
        return render_template('viewer_expenses.html', query=query)

@app.route('/viewpastexpenses', methods=['GET','POST'])
def viewpastexpenses():
    now = datetime.datetime.now()
    if now.month >=8:
        schoolyear = str(now.year) + '-' + str(now.year + 1)
        query = db.session.query(Expenses.expid, Expenses.name, Expenses.amount, Expenses.date, Expenses.orNo,
                             Event.eventName).outerjoin(Event).filter(Event.schoolyear < schoolyear)
        return render_template('viewer_expenses_past.html', query=query)
    elif now.month <=7:
        schoolyear = str(now.year-1) + '-' + str(now.year)
        query = db.session.query(Expenses.expid, Expenses.name, Expenses.amount, Expenses.date, Expenses.orNo,
                                 Event.eventName).outerjoin(Event).filter(Event.schoolyear < schoolyear)
        return render_template('viewer_expenses_past.html', query=query)

@app.route('/viewevent', methods=['GET','POST'])
def viewevents():
    now = datetime.datetime.now()
    if now.month >=8:
        schoolyear = str(now.year) + '-' + str(now.year + 1)
        query = Event.query.filter(Event.schoolyear >= schoolyear).order_by(Event.eventDate)
        return render_template('viewer_events.html', query=query)
    elif now.month <=7:
        schoolyear = str(now.year) + '-' + str(now.year + 1)
        query = Event.query.filter(Event.schoolyear >= schoolyear).order_by(Event.eventDate)
        return render_template('viewer_events.html', query=query)

@app.route('/viewpastevent', methods=['GET','POST'])
def viewpastevent():
    now = datetime.datetime.now()
    if now.month >= 8:
        schoolyear = str(now.year) + '-' + str(now.year + 1)
        query = Event.query.filter(Event.schoolyear < schoolyear).order_by(Event.eventDate)
        return render_template('viewer_events_past.html', query=query)
    elif now.month <= 7:
        schoolyear = str(now.year) + '-' + str(now.year + 1)
        query = Event.query.filter(Event.schoolyear < schoolyear).order_by(Event.eventDate)
        return render_template('viewer_events_past.html', query=query)


@app.route('/viewlogout', methods=['GET', 'POST'])
def viewlogout():
    session.pop('user', None)
    session.pop('org', None)
    return redirect(url_for('viewerlogin'))

@app.route('/unpaid/<int:colid>')
@login_required
def unpaid(colid):
    result = db.engine.execute("select * from member where member.status = 'ACTIVE' and memberid not in (Select payments.Payments_memberid from payments where payments.Payments_colid = %s );" %(colid))
    collectname = Collection.query.filter_by(colid=colid).first()
    return render_template('notpaid.html', result = result, collectname=collectname )

@app.route('/summary')
@login_required
def summary():
    now = datetime.date.today()
    if now.month >= 8:
        schoolyear = str(now.year) + '-' + str(now.year + 1)
        qry = db.session.query(func.sum(Collection.amountcollected)).filter(Collection.schoolyear == schoolyear)
        qry1 = db.session.query(func.sum(Expenses.amount)).filter(Expenses.schoolyear == schoolyear)
        collected = []
        spent = []
        for tot in qry:
            result = str(tot).strip("Decimal,()'")
            collected.append(result)

        for tot in qry1:
            result = str(tot).strip("Decimal,()'")
            spent.append(result)
        return render_template('summary.html', collected=collected, spent=spent)
    elif now.month <=7:
        schoolyear = str(now.year-1) + '-' + str(now.year)
        qry = db.session.query(func.sum(Collection.amountcollected)).filter(Collection.schoolyear == schoolyear)
        qry1 = db.session.query(func.sum(Expenses.amount)).filter(Expenses.schoolyear == schoolyear)
        collected = []
        spent = []
        for tot in qry:
            result = str(tot).strip("Decimal,()'")
            collected.append(result)

        for tot in qry1:
            result = str(tot).strip("Decimal,()'")
            spent.append(result)
        return render_template('summary.html', collected=collected, spent=spent)


if __name__ == '__main__':
    app.run(debug=True)


