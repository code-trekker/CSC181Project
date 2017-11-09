
from login import *

app = Flask(__name__)
app.debug=True
createdb()
createTables()

def createAdmin():
    db.session.add(User(id="2013-5254",username="uname",passwd="curlytops"))
    db.session.commit()

if User.query.filter_by(username="uname").first()==None: #prevents creating another admin user
    createAdmin()
else:
    pass

@app.route('/',methods=['POST','GET'])
def u_type():
    if request.method == 'POST':
        try:
            eye_D = User.query.filter_by(id=request.form['id_number']).first()

            if eye_D.id == request.form['id_number']:
                msg = 'you are Admin'
                return render_template('frst_admLand.html', msg=msg)
            else:
                msg='you are Viewr'
                return render_template('viewer_land.html', msg=msg)
        except:
            msg ="you're a viewer"
            return render_template('viewer_land.html',msg=msg)
    return render_template('loginpage.html')


@app.route('/login',methods=['POST','GET'])
def log_in():
    if request.method == 'POST':
        try:

            req = request.form['username']
            print req
            uname = User.query.filter_by(username=req).first()
            print uname.username
            if uname.username == req and check_password_hash(uname.passwd, request.form['password']):
                msg = "SUCCESS"
                return render_template("admin_land.html", msg=msg)
            else:
                msg = 'wrong username or password'
                return render_template("admLogin.html", msg=msg)
        except:
            msg = 'wrong username or password'
            return render_template("admLogin.html", msg=msg)

    return render_template('admLogin.html')




@app.route('/register',methods=['GET','POST'])
def register():
    form=request.form
    if request.method =='POST':

        print request.form['username']
        print request.form['password']
        tobe_add = User(request.form['id'], request.form['username'], request.form['password'])
        db.session.add(tobe_add)
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