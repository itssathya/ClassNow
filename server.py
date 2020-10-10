from flask import Flask, render_template,request,redirect,url_for,flash,session,g
from dbCode import loginverify,addUser,populateClasses

app = Flask(__name__)
app.secret_key = 'somesecretkeythatonlyishouldknow'

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
        token=loginverify(user,pwd)
        print(token[0])
        if(token[0]==0):
            return render_template('login.html',message="Invalid password")
        elif(token[0]==-1):
            return render_template('login.html',message="User does not exist")
        else:
            session['user_id']=token[1]
            session['user_name']=token[0]
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
        classes=populateClasses(session['user_id'])
        return render_template('dashboard.html',classes=classes)

@app.route('/logout',methods=['GET','POST'])
def logout():
    session.pop('user_id',None)
    return redirect(url_for('login'))
    

if __name__ == '__main__':
   app.run(debug=True)
