from controller import *

app = Flask(__name__)
app.debug = True
createDB()

@app.route('/')
def login():
    return render_template('loginpage.html')

if __name__=='__main__':
    app.run()