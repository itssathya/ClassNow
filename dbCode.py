import mysql.connector
from werkzeug import generate_password_hash, check_password_hash
def loginverify(user,pwd):
    mydb = mysql.connector.connect(
      host="localhost",
      user="sathya",
      passwd="password",
      database="classroomdb"
    )
    mycursor = mydb.cursor()
    sql = "SELECT * FROM userdata WHERE mail_id = %s"
    adr = (user, )
    mycursor.execute(sql, adr)
    myresult = mycursor.fetchone()
    if myresult:
      if(check_password_hash(myresult[4],pwd)):
        return [myresult[1],myresult[0]]
      else:
        return [0]
    else:
      return [-1]

def addUser(name,mail,phn,pwd,role):
    mydb = mysql.connector.connect(
      host="localhost",
      user="sathya",
      passwd="password",
      database="classroomdb"
    )
    mycursor = mydb.cursor()
    sql = "INSERT INTO userdata (name, mail_id, ph_no, pwd, role) values (%s,%s,%s,%s,%s);"
    adr = (name, mail, phn, generate_password_hash(pwd), role)
    print(adr)
    mycursor.execute(sql, adr)
    mydb.commit()

def populateClasses(uid):
  mydb = mysql.connector.connect(
      host="localhost",
      user="sathya",
      passwd="password",
      database="classroomdb"
    )
  mycursor = mydb.cursor()
  sql = "select classid,classname from classrooms where classid in (select classID from studentclass where userid="+str(uid)+");"
  mycursor.execute(sql)
  myresult=mycursor.fetchall()
  return myresult

