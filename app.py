
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

from datetime import datetime, date

currdate = datetime.today()
now=datetime.now()
fdate = now.strftime('%Y-%m-%d %H:%M:%S')

app = Flask(__name__)
app.config["SESSION_PERMANENT"]=False
app.config["SESSION_TYPE"]="filesystem"
#Session(app)

app.secret_key = 'abcdef'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'shailesh@12'

app.config['MYSQL_DB'] = 'banking'

mysql = MySQL(app)
@app.route('/')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/loan')
def loan():
    return render_template('loan.html')

@app.route('/bankmain')
def bankmain():
    return render_template('bankmain.html')

@app.route('/signin',methods=['GET', 'POST'])
def signin():
    mesage = ''
    if request.method == 'POST' and 'emailid' in request.form and 'passwd' in request.form:
        emailid = request.form['emailid']
        passwd = request.form['passwd']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('Select * from register where emailid = %s and password = %s',(emailid, passwd))
        user = cursor.fetchone()
        
        if user:
            session['loggedin'] = True
            session['rid'] = user['rid']
            session['fname'] = user['fname']
            session['lname'] = user['lname']
            session['phone'] = user['phone']
            session['emailid'] = user['emailid']
            session['password'] = user['password']
            mesage = 'Logged in successfully !'

            return render_template('bankmain.html', mesage = mesage)
        else:
            mesage = 'Please enter correct emailid or password !'
        
    return render_template('signin.html', mesage = mesage)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('cid', None)
    session.pop('emailid', None)
    return redirect(url_for('index'))
 

@app.route('/signup',methods=['GET','POST'])
def signup():
    msg=''
 
    if request.method == 'POST' and 'fname' in request.form and 'lname' in request.form and 'phone' in request.form and 'emailid' in request.form and 'passwd' in request.form:
  
        n = request.form['fname']
        m = request.form['lname']
        t = request.form['phone']
        d = request.form['emailid']
        g = request.form['passwd']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute('SELECT * FROM register WHERE emailid = % s', (d,))
        
        result = cursor.fetchone()
        if result:
            msg = 'Email id already exists !'
        else:
            cursor.execute('INSERT INTO register VALUES (NULL, % s, % s, % s, % s, %s)', (n, m, t, d, g,))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
            return render_template('signin.html', msg = msg)
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('signup.html', msg = msg)

@app.route('/account',methods=['GET','POST'])
def account():
    if request.method == 'POST' and 'fname' in request.form and 'mname' in request.form and 'lname' in request.form and 'addrs' in request.form and 'city' in request.form and 'state' in request.form and 'pincode' in request.form and 'nominee' in request.form and 'atype'in request.form and 'phone' in request.form and 'emailid' in request.form and 'gender' in request.form and 'balance' in request.form:
        fn = request.form['fname']
        mn = request.form['mname']
        ln = request.form['lname']
        ad = request.form['addrs']
        ct = request.form['city']
        st = request.form['state']
        pc = request.form['pincode']
        no = request.form['nominee']
        at = request.form['atype']
        ph = request.form['phone']
        gd = request.form['gender']
        em = request.form['emailid']
        ba = request.form['balance']
        opendate = fdate

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute('SELECT * FROM accopen WHERE emailid = % s', (em,))
        
        result = cursor.fetchone()
        if result:
            msg = 'Email id already exists !'
        else:
            cursor.execute('INSERT INTO accopen VALUES (NULL, % s, % s, % s, % s, % s, % s ,% s, % s, % s, % s, % s, % s, % s, % s)', (fn, mn, ln, ad, ct, st, pc, no, at, ph, em, gd, ba, fdate,))
            mysql.connection.commit()
            msg = 'Account created Successfully !'
            return render_template('account.html',msg = msg)
    else:
        msg = 'Please fill out the form !'
    return render_template('account.html', msg = msg)

@app.route('/wcheck',methods=['GET','POST'])
def wcheck():
    if request.method == 'POST' and 'phone' in request.form:
        phone = request.form['phone']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute('SELECT * FROM accopen WHERE phone = % s', (phone,))
        
        result = cursor.fetchone()
        if result:
            session['loggedin'] = True
            session['accno'] = result['accno']
            session['fname'] = result['fname']
            session['lname'] = result['lname']
            session['atype'] = result['atype']
            session['balance'] = result['balance']
            
            mesage = 'Passed !'
            return render_template('withdraw.html', mesage = mesage)
        else:
            mesage = 'Please enter correct phone number !'
    return render_template('wcheck.html')

@app.route('/withdraw',methods=['GET','POST'])
def withdraw():
    if request.method == 'POST' and 'accno' in request.form and 'fname' in request.form and 'lname' in request.form and 'balance' in request.form and 'wname' in request.form and 'wamount' in request.form:
        ac = request.form['accno']
        f = request.form['fname']
        l = request.form['lname']
        b = request.form['balance']
        wn = request.form['wname']
        wa = request.form['wamount']
        wd = fdate

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute("SELECT balance FROM accopen WHERE accno="+ac)
        
        sql = cursor.fetchall()[0]

        amt = int(wa)

        j = (sql['balance'])

        if amt < j:

            que = ("update accopen set balance= balance-"+wa+" where accno="+ac)
            cursor.execute(que)

            cursor.execute('INSERT INTO withdraw VALUES (NULL, % s, % s, % s, % s )', (ac, wn, wa, wd,))

            cursor.execute('SELECT balance FROM accopen WHERE accno='+ac)

            bal=cursor.fetchone()
            
            i = (bal['balance'])

            credit = 0

            cursor.execute('INSERT INTO passbook VALUES (NULL, % s, % s, % s, % s, % s )', (ac, wd, credit, wa, i,))
            
            mysql.connection.commit()
                
            msg = 'Amount withdrawn Successfully !'
        else:
            msg = 'Insufficient Balance !'
    else:
        msg = 'Please fill out the form !'
    return render_template('withdraw.html', msg=msg)

@app.route('/dcheck',methods=['GET','POST'])
def dcheck():
    if request.method == 'POST' and 'phone' in request.form:
        phone = request.form['phone']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute('SELECT * FROM accopen WHERE phone = % s', (phone,))
        
        result = cursor.fetchone()
        if result:
            session['loggedin'] = True
            session['accno'] = result['accno']
            session['fname'] = result['fname']
            session['lname'] = result['lname']
            session['atype'] = result['atype']
            session['balance'] = result['balance']
            
            mesage = 'Passed !'
            return render_template('deposit.html', mesage = mesage)
        else:
            mesage = 'Please enter correct phone number !'
    return render_template('dcheck.html')

@app.route('/deposit',methods=['GET','POST'])
def deposit():
    if request.method == 'POST' and 'accno' in request.form and 'fname' in request.form and 'lname' in request.form and 'balance' in request.form and 'dname' in request.form and 'damount' in request.form:
        ac = request.form['accno']
        f = request.form['fname']
        l = request.form['lname']
        b = request.form['balance']
        dn = request.form['dname']
        da = request.form['damount']
        dd = fdate

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        que = ("update accopen set balance= balance+"+da+" where accno="+ac)

        cursor.execute(que)

        cursor.execute("INSERT INTO deposit VALUES (NULL, % s, % s, % s, % s)",(ac, dn, da, dd,))

        cursor.execute('SELECT balance FROM accopen WHERE accno='+ac)

        bal = cursor.fetchone()

        i = (bal['balance'])

        debit = 0

        cursor.execute("INSERT INTO passbook VALUES(NULL, % s, % s, % s, % s, % s)",(ac, dd, da, debit, i,))

        mysql.connection.commit()

        msg = 'Amount deposited successfully !'

    else:
        msg = 'Please fill out the form !'
    return render_template('deposit.html', msg=msg)

@app.route('/detailscheck',methods=['GET','POST'])
def detailscheck():
    if request.method == 'POST' and 'phone' in request.form:

        phone = request.form['phone']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute('SELECT * FROM accopen WHERE phone = % s', (phone,))
     
        res = cursor.fetchone()
        if res:
            session['loggedin'] = True
            session['accno'] = res['accno']
            session['fname'] = res['fname']
            session['mname'] = res['mname']
            session['lname'] = res['lname']
            session['atype'] = res['atype']
            session['balance'] = res['balance']
            
            mesage = 'Passed !'
            return render_template('details.html', mesage = mesage)
        else:
            mesage = 'Please enter correct phone number !'
    return render_template('detailscheck.html')

@app.route('/details',methods=['GET','POST'])
def details():
    return render_template('details.html')

@app.route('/checkchangepassword',methods=['GET','POST'])
def checkchangepassword():
    if request.method == 'POST' and 'phone' in request.form:
        phone = request.form['phone']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * from register where phone=%s',(phone,))
        res = cursor.fetchone()
        if res:
            session['loggedin'] = True
            session['email'] = res['emailid']
            msg = 'Passed !'
            return render_template('changepassword.html', msg = msg)
    else:
        msg = 'Account not found !'
    return render_template('checkchangepassword.html', msg = msg)

@app.route('/changepassword', methods=['GET','POST'])
def changepassword():
    if request.method == 'POST' and 'email' in request.form and 'passwd' in request.form:
        email = request.form['email']
        passwd = request.form['passwd']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('update register set password=%s where emailid=%s',(passwd,email))
        msg = 'Password Updated successfully !'
        mysql.connection.commit()
        return render_template('changepassword.html', msg = msg)
    else:
        msg = 'Please try again !'
    return render_template('changepassword.html', msg = msg)

@app.route('/accountupdatecheck', methods=['GET','POST'])
def accountupdatecheck():
    if request.method == 'POST' and 'phone' in request.form:
        phone = request.form['phone']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('Select * from accopen where phone = % s',(phone,))
        res = cursor.fetchone()
        if res:
            session['loggedin'] = True
            session['accno'] = res['accno']
            session['fname'] = res['fname']
            session['mname'] = res['mname']
            session['lname'] = res['lname']
            session['addr'] = res['addrs']
            session['city'] = res['city']
            session['state'] = res['state']
            session['pincode'] = res['pincode']
            session['nominee'] = res['nominee']
            session['phone'] = res['phone']
            session['email'] = res['emailid']
            msg = 'Passed !'
            return render_template('accountupdate.html', msg = msg)
    else:
        mesage = 'Please enter correct phone number !'
    return render_template('accountupdatecheck.html')

@app.route('/accountupdate', methods=['GET','POST'])
def accountupdate():
    if request.method == 'POST':
        ac=request.form['accno']
        fn=request.form['fname']
        mn=request.form['mname']
        ln=request.form['lname']
        ad=request.form['addr']
        ct=request.form['city']
        st=request.form['state']
        nom=request.form['nominee']
        ph=request.form['phone']
        em=request.form['emailid']

        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute("UPDATE accopen SET fname=%s, mname=%s, lname=%s, addrs=%s, city=%s, state=%s, nominee=%s, phone=%s, emailid=%s WHERE accno=%s", (fn, mn, ln, ad, ct, st, nom, ph, em, ac))
        msg = 'Updated successfully !'
        mysql.connection.commit()
        return render_template('accountupdate.html', msg = msg)
    else:
        msg='Error'
    return render_template('accountupdate.html',msg=msg)

@app.route('/balcheck',methods=['GET','POST'])
def balcheck():
    if request.method == 'POST' and 'phone' in request.form:
        phone = request.form['phone']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute('SELECT * FROM accopen WHERE phone = % s', (phone,))
        
        result = cursor.fetchone()
        if result:
            session['loggedin'] = True
            session['accno'] = result['accno']
            session['fname'] = result['fname']
            session['lname'] = result['lname']
            session['atype'] = result['atype']
            session['balance'] = result['balance']
            
            mesage = 'Passed !'
            return render_template('balenquiry.html', mesage = mesage)
        else:
            mesage = 'Please enter correct phone number !'
    return render_template('balcheck.html')    

@app.route('/balenquiry',methods=['GET','POST'])
def balenquiry():
    return render_template('balenquiry.html')    

@app.route('/minicheck',methods=['GET','POST'])
def minicheck():
    if request.method == 'POST' and 'phone' in request.form:

        phone = request.form['phone']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute('SELECT * FROM accopen WHERE phone = % s', (phone,))
     
        res = cursor.fetchone()
        
        if res:
            session['accno'] = res['accno']
            session['atype'] = res['atype']
            accno = res['accno']

            que = ("SELECT * FROM passbook WHERE accno="+str(accno)+" order by tid desc")

            cursor.execute(que)

            query = cursor.fetchall()

            return render_template('ministate.html', value = query)
            
        else:
            mesage = 'Please enter correct phone number !'
    return render_template('minicheck.html')

@app.route('/ministate',methods=['GET','POST'])
def ministate():
    return render_template('ministate.html')

@app.route('/passcheck',methods=['GET','POST'])
def passcheck():
    if request.method == 'POST' and 'phone' in request.form:
        phone = request.form['phone']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('SELECT * FROM accopen WHERE phone = % s', (phone,))
        acc=cursor.fetchone()

        if acc:
            session['accno'] = acc['accno']
            session['fname'] = acc['fname']
            session['mname'] = acc['mname']
            session['lname'] = acc['lname']
            session['phone'] = acc['phone']
            session['atype'] = acc['atype']
            accnum = acc['accno']

            cursor.execute('SELECT * FROM passbook WHERE accno = % s', (accnum,))
        
            result = cursor.fetchall()
            if result:
                return render_template('passbook.html', result = result)
            else:
                mesage = 'No record found!'
    else:
        mesage = 'Please enter correct phone number !'
    return render_template('passcheck.html')

@app.route('/passbook', methods=['GET', 'POST'])
def passbook():
    return render_template('passbook.html')

@app.route('/personalloan')
def personalloan():
    return render_template('personalloan.html')

@app.route('/educationloan')
def educationloan():
    return render_template('educationloan.html')

@app.route('/vehicleloan')
def vehicleloan():
    return render_template('vehicleloan.html')

@app.route('/homeloan')
def homeloan():
    return render_template('homeloan.html')

@app.route('/loanapply', methods=['GET', 'POST'])
def loanapply():
    if request.method == 'POST' and 'phone' in request.form:
        phone = request.form['phone']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * from accopen where phone= %s',(phone,))
        res = cursor.fetchone()
        if res:
            session['loggedin'] = True
            session['accno'] = res['accno']
            session['fname'] = res['fname']
            session['mname'] = res['mname']
            session['lname'] = res['lname']
            session['email'] = res['emailid']
            session['phone'] = res['phone']
            session['addr'] = res['addrs']
            session['city'] = res['city']
            session['state'] = res['state']
            session['pincode'] = res['pincode']
            msg = 'Passed'
            return render_template('loanapplication.html', msg = msg)
        else:
            msg = 'Enter correct contact number !'
    return render_template('loanapply.html')

@app.route('/loanapplication', methods=['GET', 'POST'])
def loanapplication():
    if request.method == 'POST' and 'accno' in request.form and 'fname' in request.form and 'mname' in request.form and 'lname' in request.form and 'emailid' in request.form and 'phone' in request.form and 'addrs' in request.form and 'city' in request.form and 'state' in request.form and 'pincode' in request.form and 'loantype' in request.form and 'amount' in request.form and 'tenure' in request.form:
        ac = request.form['accno']
        fn = request.form['fname']
        mn = request.form['mname']
        ln = request.form['lname']
        em = request.form['emailid']
        ph = request.form['phone']
        ad = request.form['addrs']
        ct = request.form['city']
        st = request.form['state']
        pc = request.form['pincode']
        lt = request.form['loantype']
        amt = request.form['amount']
        tn = request.form['tenure']
        status = 'pending' 
        submitdate = fdate
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('insert into loanapplication values(NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(ac, fn, mn, ln, em, ph, ad, ct, st, lt, amt, tn, status, submitdate))
        mysql.connection.commit()
        msg = 'Application submitted successfully !'
        return render_template('loanapplication.html', msg = msg)
    else:
        msg  = 'Please fill out the form !'

    return render_template('loanapplication.html', msg = msg)

@app.route('/termsandconditions')
def termsandconditions():
    return render_template('termsandconditions.html')

@app.route('/loandownloadcheck', methods=['GET','POST'])
def loandownloadcheck():
    if request.method == 'POST' and 'phone' in request.form:
        phone = request.form['phone']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * from loanapplication where contact= %s',(phone,))
        res = cursor.fetchone()
        if res:
            session['accno'] = res['accno']
            session['fname'] = res['fname']
            session['mname'] = res['mname']
            session['lname'] = res['lname']
            session['email'] = res['email']
            session['contact'] = res['contact']
            session['addrs'] = res['addrs']
            session['city'] = res['city']
            session['state'] = res['state']
            session['loantype'] = res['loantype']
            session['amount'] = res['amount']
            session['tenure'] = res['tenure']
            session['status'] = res['status']
            return render_template('loanapplicationdownload.html')
        else:
            msg = 'Record not found !'
            render_template('loandownloadcheck.html', msg = msg)
    return render_template('loandownloadcheck.html')

@app.route('/loanapplicationdownload', methods=['GET','POST'])
def loanapplicationdownload():
    render_template('loanapplicationdownload.html')

@app.route('/loancheck', methods=['GET', 'POST'])
def loancheck():
    if request.method == 'POST' and 'accno' in request.form:
        accno = request.form['accno']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        #cursor.execute('select * from accopen where phone= %s',(phone,))
        #res = cursor.fetchone()
        #accno = res['accno']
        cursor.execute('select * from loanview where accno= %s',(accno,))
        que = cursor.fetchone()
        if que:
            session['accno'] = que['accno']
            session['amount'] = que['amount']
            session['rate'] = que['rate']
            session['tenure'] = que['tenure']
            msg = 'Passed !' 
            return render_template('calloan.html', msg = msg)
        else:
            msg = 'Not found !'
            return render_template('loancheck.html', msg = msg)
    return render_template('loancheck.html')
            
@app.route('/calloan', methods=['GET', 'POST'])
def calloan():
    if request.method == 'POST' and 'accno' in request.form and 'amount' in request.form and 'interest' in request.form and 'years' in request.form and 'totalpayment' in request.form and 'monthlypayment' in request.form and 'totalinterest' in request.form:
        ac = request.form['accno']
        amt = request.form['amount']
        interest = request.form['interest']
        years = request.form['years']
        totpay = request.form['totalpayment']
        monpay = request.form['monthlypayment']
        totint = request.form['totalinterest']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO loancalculation values(NULL, %s, %s, %s, %s, %s, %s, %s)',(ac, amt,interest,years,totpay,monpay,totint,))
        mysql.connection.commit()
        msg = 'Calculation Saved !'
        return render_template('calloan.html', msg = msg)
    else:
        msg = 'Invalid !'
        return render_template('calloan.html', msg= msg)

@app.route('/loanreceiptcheck',methods=['GET','POST'])
def loanreceiptcheck():
    if request.method == 'POST' and 'phone' in request.form:
        phone = request.form['phone']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * from accopen where phone= %s',(phone,))
        res = cursor.fetchone()
        accno = res['accno']
        cursor.execute('select * from loancalculation where accno='+str(accno))
        que = cursor.fetchone()
        if que:
            session['accno'] = que['accno']
            session['amount'] = que['amount']
            session['interest'] = que['interest']
            session['tenure'] = que['tenure']
            session['totalpay'] = que['totalpay']
            session['monthpay'] = que['monthpay']
            session['totalint'] = que['totalint']
            return render_template('loanreceipt.html')
        else:
            msg = 'Receipt not found !'
            return render_template('loanreceiptcheck.html', msg = msg)
    return render_template('loanreceiptcheck.html')

@app.route('/loanreceipt')
def loanreceipt():
    return render_template('loanreceipt.html')

@app.route('/contactus')
def contactus():
    return render_template('contactus.html')

@app.route('/portallogin', methods=['GET', 'POST'])
def portallogin():
    mesage = ''
    if request.method == 'POST' and 'username' in request.form and 'passw' in request.form:
        uname = request.form['username']
        passed = request.form['passw']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('Select * from portal where user = %s and passwd = %s',(uname,passed))
        membr = cursor.fetchone()

        if membr:
            session['logged'] = True
            session['id'] = membr['id']
            session['user'] = membr['user']
            session['passwd'] = membr['passwd']
            mesage = 'Logged in!'
            return render_template('portalindex.html', mesage = mesage)
        
        else:
            mesage = 'Please enter correct email and password!'
    
    return render_template('portallogin.html', mesage = mesage)

@app.route('/portalindex')
def portalindex():
    return render_template('portalindex.html')

@app.route('/portalaccounts',methods=['GET','POST'])
def portalaccounts():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accopen')
    result = cursor.fetchall()
    return render_template('portalaccounts.html', result = result)

@app.route('/portalusers')
def portalusers():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('Select * from register')
    user = cursor.fetchall()
    return render_template('portalusers.html', user = user)

@app.route('/userupdate', methods=['GET','POST'])
def userupdate():
    if request.method == 'POST' and 'phone' in request.form:
        phone = request.form['phone']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * from register where phone = %s',(phone,))
        res = cursor.fetchone()
        if res:
            session['fname'] = res['fname']
            session['lname'] = res['lname']
            session['phone'] = res['phone']
            msg = 'Passed !'
            return render_template('updateuser.html', msg = msg)
        else:
            msg = 'Please enter correct phone number !'
    return render_template('userupdate.html')

@app.route('/updateuser',methods=['GET','POST'])
def updateuser():
    if request.method == 'POST' and 'fname' in request.form and 'lname' in request.form and 'phone' in request.form:
        fn = request.form['fname']
        ln = request.form['lname']
        ph = request.form['phone']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        quer=('update register set fname=%s, lname=%s where phone=%s')
        data=(fn,ln,ph)
        cursor.execute(quer,data)
        mysql.connection.commit()
        msg = 'Update successfully !'
        return render_template('updateuser.html', msg = msg)
    else:
        msg = 'Error'
    return render_template('updateuser.html', msg = msg)

@app.route('/portalpass', methods=['GET','POST'])
def portalpass():
    if request.method == 'POST' and 'accno' in request.form:
        accnum = request.form['accno']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * from accopen where accno = %s', (accnum,))
        acc = cursor.fetchone()
        if acc:
            accnos = acc['accno']
            cursor.execute('select * from passbook where accno = %s',(accnos,))
            res = cursor.fetchall()
            if res:
                return render_template('portalpassbook.html', res = res)
            else:
                mesage = 'No record!'
    else:
        mesage = 'Please enter correct account number.'
    return render_template('portalpass.html')

@app.route('/portalpassbook', methods=['GET','POST'])
def portalpassbook():
    return render_template('portalpassbook.html')

@app.route('/portalapplication', methods=['GET','POST'])
def portalapplication():
    status = 'pending'
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('select * from loanapplication where status=%s',(status,))
    result = cursor.fetchall()
    return render_template('loanapprove.html', result = result)
    
@app.route('/loanapprove',methods=['GET','POST'])
def loanapprove():
    if request.method == 'POST' and 'accno' in request.form and 'amount' in request.form and 'applid' in request.form:
        accno = request.form['accno']
        amount = request.form['amount']
        applid = request.form['applid']
        status = 'Approved'
        dd = fdate
        name = 'Loan deposited'
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('update loanapplication set status=%s where id=%s',(status,applid,))
        
        que = ("update accopen set balance= balance+"+amount+" where accno="+accno)
        cursor.execute(que)
        cursor.execute('insert into deposit values(NULL, %s, %s, %s, %s)',(accno,name,amount,dd))
        cursor.execute('select balance from accopen where accno='+accno)
        que = cursor.fetchone()
        bal = (que['balance'])
        debit = 0
        cursor.execute('insert into passbook values(NULL,%s, %s, %s, %s, %s)',(accno,dd,amount,debit,bal))
        mysql.connection.commit()
        msg = 'Loan approved !'
    else:
        msg = 'Please try again !'
    return render_template('loanapprove.html', msg = msg)

@app.route('/loanapproved')
def loanapproved():
    status = 'approved'
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('select * from loanapplication where status=%s',(status,))
    res = cursor.fetchall()
    return render_template('loanapproved.html', res = res)

@app.route('/loans', methods=['GET','POST'])
def loans():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('select * from loans')
    result = cursor.fetchall()
    return render_template('portalloanupdate.html', result = result)

@app.route('/portalloanupdate', methods=['GET','POST'])
def portalloanupdate():
    if request.method == 'POST' and 'id' in request.form and 'loantype' in request.form and 'rate' in request.form:
        lid = request.form['id']    
        loantype = request.form['loantype']
        rate = request.form['rate']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE loans SET loantype=%s , rate=%s WHERE id=%s',(loantype, rate, lid))
        mysql.connection.commit()
        msg = 'Updated Successfully !'
        return render_template('portalloanupdate.html', msg = msg)
    else:
        msg = 'Error'
        return render_template('portalloanupdate.html', msg = msg)

@app.route('/portalloandelete/<string:id>', methods=['Get','POST'])
def portalloandelete(id):
    flash('Record has been Deleted')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('delete from loans where id=%s',(id,))
    mysql.connection.commit()
    return render_template('portalloanupdate.html')


@app.route('/loggedout')
def loggedout():
    session.pop('logged', None)
    session.pop('id', None)
    session.pop('user', None)
    session.pop('passwd', None)
    return redirect(url_for('portallogin'))

if __name__ == '__main__':
    app.run(port=5000,debug=True)        