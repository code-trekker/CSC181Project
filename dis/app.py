
from login import *

app = Flask(__name__)
app.debug=True
createdb()
createTables()

def createAdmin():
    db.session.add(User(username="uname",passwd="safests"))
    db.session.commit()

if User.query.filter_by(username="uname").first()==None: #prevents creating another admin user
    createAdmin()
else:
    pass

@app.route('/')
def login():
    return render_template('loginpage.html')

@app.route('/u_type',methods=['POST','GET'])
def u_type():
    if request.method == 'POST':
        try:
            id=request.form['id_number']
            if id == '2013-5254':
                print "adminnnnnn"
                msg = 'you are Admin'
                return render_template('frst_admLand.html', msg=msg)
            else:
                msg='you are Viewr'
                return render_template('viewer_land.html', msg=msg)
        except:
            msg ='error'
            return render_template('viewer_land.html',msg=msg)

@app.route('/login',methods=['POST','GET'])
def log_in():

    return render_template('admLogin.html')




@app.route('/verify',methods=['GET','POST'])
def verify():
    print  "hhhhoooowwwwwwww"
    req=request.form['username']
    print req
    uname=User.query.filter_by(username=req).first()
    print "xxxxxxx"
    print uname
    if check_password_hash(uname.passwd,request.form['password']):
        msg="SUCCESS"
        return render_template("admin_land.html",msg=msg)
    else:
        msg='ahahahahha youre a viewer'
        return render_template("viewer_land.html",msg=msg)

@app.route('/register',methods=['GET','POST'])
def register():
    form=request.form
    if request.method =='POST':

        print request.form['username']
        print request.form['password']
        tobe_add = User( request.form['username'], request.form['password'])
        print"im performed"
        db.session.add(tobe_add)
        print "im added"
        db.session.commit()
        msg="added succesfully"
        return render_template('admin_land.html',msg=msg)
    return render_template('adm_reg.html',form=form)

@app.route('/proceed')
def proceed():
    msg="page to be view"
    return render_template('viewing_page.html',msg=msg)

@app.route('/add_dis')
def add_dis():
    return render_template('viewer_reg.html')

if __name__ == '__main__':
    app.run()