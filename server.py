from flask import Flask, render_template,request,redirect,url_for,flash,session,g
from dbCode import loginVerify,addUser,studentPopulateClasses,ownerPopulateClasses,retrieveClassData,addClass,joinClassroom,allUsers

app = Flask(__name__)
app.secret_key = 'somesecretkeythatonlyishouldknow'
UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 

@app.before_request
def before_request():
    g.user = None
    if('user_id' in session):
        g.user = 'user_id'

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html',message="")
    elif request.method == 'POST':
        session.pop('user_id',None)
        print("SumbissionLogDebug")
        user=request.form['user']
        pwd=request.form['pwd']
        token=loginVerify(user,pwd)
        if(token[0]==0):
            return render_template('login.html',message="Invalid password")
        elif(token[0]==-1):
            return render_template('login.html',message="User does not exist")
        else:
            session['user_id']=token[1]
            session['user_name']=token[0]
            session['user_role']=token[2]
            print(session['user_role'])
            return redirect(url_for('dashboard'))
        

@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        name=request.form['fname']
        email=request.form['email']
        phone=request.form['phone']
        pwd=request.form['pwd']
        role=request.form["role"]
        addUser(name,email,phone,pwd,role)
        return redirect(url_for('login'))


@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    if not g.user:
        return redirect(url_for('login'))
    if request.method == 'GET':
        if(session['user_role']=="3"):
            classes=studentPopulateClasses(session['user_id'])
            return render_template('studentDashboard.html',classes=classes)
        elif(session['user_role']=="2"):
            classes=ownerPopulateClasses(session['user_id'])
            return render_template('ownerDashboard.html',classes=classes)
        elif(session['user_role']=="1"):
            return render_template('adminDashboard.html')


@app.route('/logout',methods=['GET','POST'])
def logout():
    session.pop('user_id',None)
    return redirect(url_for('login'))


@app.route('/classStream',methods=['GET','POST'])
def classStream():
    if not g.user:
        return redirect(url_for('login'))
    if request.method == 'POST':
        classid=request.form['goclass']
        if(session['user_role']=="3"):
            classes=retrieveClassData(classid)
            print("Student")
            return render_template('studentClassStream.html',classes=classes)
        elif(session['user_role']=="Owner"):
            classes=retrieveClassData(classid)
            return render_template('ownerClassStream.html',classes=classes)
        return render_template('classStream.html')


@app.route('/ownerClasses',methods=['GET','POST'])
def ownerClasses():
    if not g.user:
        return redirect(url_for('login'))
    if request.method == 'GET':
        return render_template('ownerClasses.html')


@app.route('/newClass',methods=['GET','POST'])
def newClass():
    if not g.user:
        return redirect(url_for('login'))
    if request.method == 'GET':
        return render_template('newClass.html')
    elif request.method == 'POST':
        className = request.form['classname']
        addClass(className,session['user_id'])
        return redirect(url_for('dashboard'))

@app.route('/joinClass',methods=['GET','POST'])
def joinClass():
    if not g.user:
        return redirect(url_for('login'))
    if request.method == 'GET':
        return render_template('joinClass.html')
    elif request.method == 'POST':
        classid = request.form['classname']
        joinClassroom(classid,session['user_id'])
        return redirect(url_for('dashboard'))

@app.route('/deleteUser',methods=['GET','POST'])
def deleteUser():
    if not g.user:
        return redirect(url_for('login'))
    if request.method == 'GET':
        users=allUsers()
        return render_template('deleteUser.html',users=users)
    """elif request.method == 'POST':
        classid = request.form['classname']
        joinClassroom(classid,session['user_id'])
        return redirect(url_for('dashboard'))"""

@app.route('/upload/',methods = ['GET','POST'])
def upload_file():
    if request.method =='POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            return hello()
    return render_template('file_upload.html')
    

if __name__ == '__main__':
   app.run(debug=True)
