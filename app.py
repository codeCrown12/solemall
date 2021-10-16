import re
import string
import random
import datetime
import os

from flask.helpers import flash
from passlib.hash import sha256_crypt
from flask import Flask,request,render_template,redirect,url_for,session
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOADS_FOLDER = 'static/products'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'solemall'
app.config['UPLOAD_FOLDER'] = UPLOADS_FOLDER

mysql = MySQL(app)
app.secret_key="codecrown123"

app.config['MAIL_SERVER']='mail.crowndidactic.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'info@crowndidactic.com'
app.config['MAIL_PASSWORD'] = 'Passw0rdx123#'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

#Function to count orders
def countorders():
    cur = mysql.connection.cursor()
    cur.execute('SELECT COUNT(*) AS total FROM orders')
    record = cur.fetchone()
    if record:
        return record
    return []

#Function to count users
def countusers():
    cur = mysql.connection.cursor()
    cur.execute('SELECT COUNT(*) AS total FROM users')
    record = cur.fetchone()
    if record:
        return record 
    return []

#Function to count products
def countproducts():
    cur = mysql.connection.cursor()
    cur.execute('SELECT COUNT(*) AS total FROM products')
    record = cur.fetchone()
    if record:
        return record
    return []

#Function to get all orders
def getorders():
    cur = mysql.connection.cursor()
    cur.execute('SELECT O_ID, total, status, date_created, U_ID FROM orders')
    record = cur.fetchall()
    if record:
        return record
    return []

#Function to get all products
def getproducts():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM products')
    record = cur.fetchall()
    if record:
        return record
    return []

#Function to get all users
def getusers():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM users')
    record = cur.fetchall()
    if record:
        return record
    return []

#Function to get total earnings
def countprofit():
    cur = mysql.connection.cursor()
    cur.execute('SELECT SUM(total) AS total FROM orders')
    record = cur.fetchone()
    if record:
        return record
    return []


#Function to check valide image extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

#Function to get date
def getDate():
    x = datetime.datetime.now()
    return x.strftime("%Y-%m-%d")

#Function to generate a random string
def genRandomStr():
    S = 30 
    ran = ''.join(random.choices(string.ascii_lowercase + string.digits, k = S))    
    return str(ran)

#Function to generate token
def genToken():
    S = 6 
    ran = ''.join(random.choices(string.digits, k = S))    
    return str(ran)

#Function to get current formatted date
# def getDate(x):
#     datestr = x.strftime("%b, -%d")
#     return datestr

#Function to check if user email already exists
def emailexists(email):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM users WHERE email = %s', [email])
    record = cur.fetchone()
    if record:
        return True
    return False

#Function to get user token
def getUserToken(email):
    cur = mysql.connection.cursor()
    cur.execute('SELECT token FROM users WHERE email = %s', [email])
    record = cur.fetchone()
    if record:
        return record[0]
    return False

#Function to update email verification status
def confirmVerification(email):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE users SET email_verified = 'true' WHERE email = %s", [email])
    mysql.connection.commit()
    cur.close()
    return True

#Function to change email address
def confirmnewemail(email, newemail):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE users SET email = %s WHERE email = %s", (newemail, email))
    mysql.connection.commit()
    cur.close()
    return True

#Function to update token for new users
def updateToken(email):
    newToken = genToken()
    cur = mysql.connection.cursor()
    cur.execute('UPDATE users SET token = %s WHERE email = %s', (newToken, email))
    mysql.connection.commit()
    cur.close()
    return newToken

#Function to get all the categories
def getcategories():
    cur = mysql.connection.cursor()
    cur.execute('SELECT category FROM categories')
    record = cur.fetchall()
    if record:
        return record

#Function to get all products
def getAllProducts(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    record = cur.fetchall()
    if record:
        return record
    return []

#Function to retrieve a particular product
def getProduct(pid):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products WHERE P_ID = %s", [pid])
    record = cur.fetchone()
    if record:
        return record
    return []

#Function to clear cart
def clearcart():
    if 'key' in session:
        uid = session['key']
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM cart WHERE U_ID = %s", [uid])
        mysql.connection.commit()
        cur.close()
        return True
    else:
        return False

#Function to get user details
def getuser():
    if 'key' in session:
        uid = session['key']
        cur = mysql.connection.cursor()
        cur.execute("SELECT U_ID, firstname, lastname, email, mobile, street, state, city, zip FROM users WHERE U_ID = %s", [uid])
        record = cur.fetchone()
        if record:
            return record
        return []

#Function to cconvert string to list
def stringToList(string):
   li = list(string.split(","))
   return li

#Function to add item to cart
def addToCart(pid, qty, color, size):
    if 'key' in session:
        uid = session['key']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO cart (U_ID, P_ID, quantity, color, size) VALUES (%s, %s, %s, %s, %s)', (uid, pid, qty, color, size))
        mysql.connection.commit()
        cur.close()
        return True
    return False

#Function to add item to wishlist
def addToWish(pid):
    if 'key' in session:
        uid = session['key']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO wishlist (U_ID, P_ID) VALUES (%s, %s)', (uid, pid))
        mysql.connection.commit()
        cur.close()
        return True
    return False

#Function to check if an item is in cart
def checkCart(pid):
    if 'key' in session:
        uid = session['key']
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM cart WHERE P_ID = %s AND U_ID = %s', (pid, uid))
        record = cur.fetchone()
        if record:
            return True
    return False

#Function to check if an item is in wishlist
def checkWish(pid):
    if 'key' in session:
        uid = session['key']
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM wishlist WHERE P_ID = %s AND U_ID = %s', (pid, uid))
        record = cur.fetchone()
        if record:
            return True
    return False

#Function to get all items in the cart
def getcartitems():
    if 'key' in session:
        uid = session['key']
        cur = mysql.connection.cursor()
        cur.execute('SELECT cart.color, cart.size, cart.quantity, products.imgurl, products.price, products.name, cart.C_ID, products.quantity, products.colors, products.sizes, products.P_ID FROM cart INNER JOIN products ON cart.P_ID = products.P_ID WHERE cart.U_ID = %s', [uid])
        record = cur.fetchall()
        if record:
            return record
    return []

#Function to get all items in wishlist
def getwishitems():
    if 'key' in session:
        uid = session['key']
        cur = mysql.connection.cursor()
        cur.execute('SELECT wishlist.date_added, products.imgurl, products.price, products.name, products.quantity, wishlist.P_ID, wishlist.W_ID, products.sizes, products.colors FROM wishlist INNER JOIN products ON wishlist.P_ID = products.P_ID WHERE wishlist.U_ID = %s', [uid])
        record = cur.fetchall()
        if record:
            return record
    return []

def getorderitems():
    if 'key' in session:
        uid = session['key']
        cur = mysql.connection.cursor()
        cur.execute('SELECT O_ID, total, status, date_created FROM orders WHERE U_ID = %s', [uid])
        record = cur.fetchall()
        if record:
            return record
    return []

def getshipping():
    return 30

def countcartitems():
    if 'key' in session:
        uid = session['key']
        cur = mysql.connection.cursor()
        cur.execute('SELECT COUNT(*) AS total FROM cart WHERE U_ID = %s', [uid])
        record = cur.fetchone()
        if record:
            return record
    return [0]


@app.route('/')
def index():
    nav_show = "d-block"
    u_show = "d-none"
    totalcartitems = countcartitems()
    query = "SELECT P_ID, name, price, imgurl, colors, sizes FROM products LIMIT 6"
    items = getAllProducts(query)
    qlatest = "SELECT P_ID, name, price, imgurl, colors, sizes FROM products ORDER BY P_ID DESC LIMIT 3"
    itemslatest = getAllProducts(qlatest)
    sizeofitems = len(items)
    sizelatest = len(itemslatest)
    if 'key' in session:
        nav_show = 'd-none'
        u_show = 'd-block'
    return render_template('index.html', nav_show = nav_show, u_show = u_show, totalcartitems = totalcartitems, itemslatest = itemslatest, items = items, size = sizeofitems, sizelatest = sizelatest, checkCart = checkCart, stringToList = stringToList)

@app.route('/shop', methods=['POST','GET'])
def shop():
    totalcartitems = countcartitems()
    query = "SELECT P_ID, name, price, imgurl, colors, sizes FROM products ORDER BY P_ID DESC"
    categories = getcategories()
    nav_show = "d-block"
    u_show = 'd-none'
    if 'key' in session:
        nav_show = 'd-none'
        u_show = 'd-block'
    
    #sorting code snippet
    if request.method == 'POST':
        details = request.form.get
        cat = details('category') 
        size = details('size')
        price = details('price')
        if cat != "":
            query = f"SELECT P_ID, name, price, imgurl, colors, sizes FROM products WHERE category = '{cat}'"
        elif size != "":
            query = f"SELECT P_ID, name, price, imgurl, colors, sizes FROM products WHERE sizes LIKE '%{size}%'"
        elif price != "":
            if price == "lowest":
                query = f"SELECT P_ID, name, price, imgurl, colors, sizes FROM products ORDER BY price"
            elif price == "highest":
                query = f"SELECT P_ID, name, price, imgurl, colors, sizes FROM products ORDER BY price DESC"

    if request.method == 'POST' and 'keyword' in request.form:
        details = request.form.get
        keyword = details('keyword')
        if keyword != "":
            query = f"SELECT P_ID, name, price, imgurl, colors, sizes FROM products WHERE name LIKE '%{keyword}%'"

    items = getAllProducts(query)
    sizeofitems = len(items)
    return render_template('shop.html', nav_show = nav_show, u_show = u_show, items = items, categories = categories, size = sizeofitems, totalcartitems = totalcartitems, checkCart = checkCart, stringToList = stringToList)

@app.route('/login', methods=['POST','GET'])
def login():
    msg = ""
    if request.method == 'POST' and 'login' in request.form:
        details = request.form.get
        email = details('email')
        password = details('pass')
        if email == "" or password == "":
            msg = "All fields are required"
        else:
            cur = mysql.connection.cursor()
            cur.execute('SELECT passkey, U_ID FROM users WHERE email = %s', [email])
            record = cur.fetchone()
            if record:
                passvalid = sha256_crypt.verify(password, record[0])
                if passvalid == True:
                    session['key'] = record[1]
                    return redirect(url_for('shop'))
                else:
                    msg = "Invalid login details!"
            else:
                msg = "Invalid login details!"
    return render_template('login.html', msg = msg)

@app.route('/verifyemail', methods=['POST','GET'])
def verifyemail():
    email = ""
    e_msg = ""
    s_msg = ""
    if 'temp_email' not in session:
        return redirect(url_for('signup'))     
    else:
        email = session['temp_email']   
        #Process form request
        if request.method == 'POST' and 'verify' in request.form:
            details = request.form.get
            formtoken = details('token')
            usertoken = getUserToken(email)
            if formtoken == usertoken:
                confirmVerification(email)
                session.pop('temp_email', None)
                return redirect(url_for('login'))
            else:
                msg = "Token is invalid"
        
        #Snippet to request a new token
        if 'reqtoken' in request.args:
            newtoken = updateToken(email)
            msg = Message('New Token Request', sender = 'info@crowndidactic.com', recipients = [email])
            msg.body = f"Hello chief, you requested for a new token. Your new token is {newtoken}"
            mail.send(msg)
            s_msg = "New token has been sent to your email address"
    return render_template('verifyemail.html', msg = e_msg, s_msg = s_msg)


@app.route('/changemail', methods=['POST','GET'])
def verifynewemail():
    email = ""
    e_msg = ""
    s_msg = ""
    if 'temp_email' not in session and 'new_email' not in session:
        return redirect(url_for('login'))     
    else:
        email = session['temp_email']  
        newemail = session['new_email'] 
        #Process form request
        if request.method == 'POST' and 'verify' in request.form:
            details = request.form.get
            formtoken = details('token')
            usertoken = getUserToken(email)
            if formtoken == usertoken:
                confirmnewemail(email, newemail)
                session.pop('temp_email', None)
                session.pop('new_email', None)
                return redirect(url_for('login'))
            else:
                msg = "Token is invalid"
        
        #Snippet to request a new token
        if 'reqtoken' in request.args:
            newtoken = updateToken(email)
            msg = Message('New Token Request', sender = 'info@crowndidactic.com', recipients = [newemail])
            msg.body = f"Hello chief, you requested for a new token. Your new token is {newtoken}"
            mail.send(msg)
            s_msg = "New token has been sent to your email address"
    return render_template('changemail.html', msg = e_msg, s_msg = s_msg)


@app.route('/verifychangepass', methods=['POST','GET'])
def verifychangepass():
    e_msg = ""
    s_msg = ""
    if 'temp_email' not in session:
        return redirect(url_for('login'))
    else:
        email = session['temp_email']   
        #Process form request
        if request.method == 'POST' and 'verify' in request.form:
            details = request.form.get
            formtoken = details('token')
            usertoken = getUserToken(email)
            if formtoken == usertoken:
                return redirect(url_for('changepass'))
            else:
                msg = "Token is invalid"
        
        #Snippet to request a new token
        if 'reqtoken' in request.args:
            newtoken = updateToken(email)
            msg = Message('New Token Request', sender = 'info@crowndidactic.com', recipients = [email])
            msg.body = f"Hello chief, you requested for a new token. Your new token is {newtoken}"
            mail.send(msg)
            s_msg = "New token has been sent to your email address"
    return render_template('verifychangepass.html', msg = e_msg, s_msg = s_msg)

@app.route('/changepass', methods=['POST', 'GET'])
def changepass():
    e_msg = ""
    s_msg = ""
    if 'temp_email' not in session:
        return redirect(url_for('login'))
    else:
        email = session['temp_email']   
        #Process form request
        if request.method == 'POST' and 'verify' in request.form:
            details = request.form.get
            passone = details('pass')
            passtwo = details('pass1')
            if passone != passtwo:
                e_msg = "Passwords do not match!"
            else:
                hashedpass = sha256_crypt.hash(passone)
                cur = mysql.connection.cursor()
                cur.execute("UPDATE users SET passkey = %s WHERE email = %s", (hashedpass, email))
                mysql.connection.commit()
                cur.close()
                session.pop('temp_email', None)
                return redirect(url_for('login'))
    return render_template('changepass.html', msg = e_msg, s_msg = s_msg)

@app.route('/signup', methods=['POST','GET'])
def signup():
    msg = ""
    if request.method == 'POST' and 'register' in request.form:
        details = request.form.get
        fname = details('fname')
        lname = details('lname')
        email = details('email')
        mobile = details('mobile')
        passone = details('passone')
        passtwo = details('passtwo')
        street = details('street')
        state = details('state')
        city = details('city')
        u_zip = details('zip')
        if fname == "" or lname == "" or email == "" or mobile == "" or street == "" or state == "" or city == "" or u_zip == "" or passone == "" or passtwo == "":
            msg = "All fields are required"
        elif passone != passtwo:
            msg = "Passwords do not match"
        elif emailexists(email):
            msg = "Email already exists"
        else:
            hashedpass = sha256_crypt.hash(passone)
            token = genToken()
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO users (firstname, lastname, email, mobile, street, state, city, zip, passkey, token) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (fname, lname, email, mobile, street, state, city, u_zip, hashedpass, token))
            mysql.connection.commit()
            cur.close()
            msg = Message('Verify Email address', sender = 'info@crowndidactic.com', recipients = [email])
            msg.body = f"Hello {fname} You're one step away from shopping your favorite products. In order to complete your registration you'll need to verify your email address. Your token is {token}"
            mail.send(msg)
            session['temp_email'] = email
            return redirect(url_for('verifyemail'))
    return render_template('signup.html', msg = msg)

@app.route('/cart')
def cart():
    products = ""
    colors = ""
    sizes = ""
    qty = ""
    nav_show = "d-block"
    u_show = "d-none"
    totalcartitems = countcartitems()
    if 'key' in session:
        nav_show = 'd-none'
        u_show = 'd-block'
    else:
        return redirect(url_for('login'))
    items = getcartitems()
    size = len(items)
    ship = getshipping()
    for item in items:
        products += f"{item[10]},"
        colors += f"{item[0]},"
        qty += f"{item[2]},"
        sizes += f"{item[1]},"
    return render_template('cart.html', colors = colors[:-1], qty = qty[:-1], sizes = sizes[:-1], products = products[:-1], ship = ship, nav_show = nav_show, size = size, u_show = u_show, items = items, stringToList = stringToList, totalcartitems = totalcartitems)

@app.route('/profile')
def profile():
    totalcartitems = countcartitems()
    nav_show = "d-block"
    u_show = 'd-none'
    if 'key' in session:
        nav_show = 'd-none'
        u_show = 'd-block'
    else:
        return redirect(url_for('login'))

    #Get user details
    u_details = getuser()
    fname = u_details[1]
    lname = u_details[2]
    email = u_details[3]
    mobile = u_details[4]
    street = u_details[5]
    state = u_details[6]
    city = u_details[7]
    uzip = u_details[8]

    #get wishlist items
    wishitems = getwishitems()
    wishsize = len(wishitems)

    #get past orders
    orderitems = getorderitems()
    ordersize = len(orderitems)
    return render_template('profile.html', orderitems = orderitems, ordersize = ordersize, stringToList = stringToList, wishsize = wishsize, wishitems = wishitems, fname = fname, lname = lname, mobile = mobile, email = email, street = street, state = state, city = city, uzip = uzip, nav_show = nav_show, u_show = u_show, totalcartitems = totalcartitems)

@app.route('/product', methods=['POST','GET'])
def product():
    totalcartitems = countcartitems()
    pid = request.args.get('pid')
    item = getProduct(pid)
    sizes_list = stringToList(item[4])
    colors_list = stringToList(item[5])
    cartstatus = ""
    wishstatus = ""
    nav_show = "d-block"
    u_show = "d-none"

    if 'key' in session:
        nav_show = 'd-none'
        u_show = 'd-block'

    if checkCart(pid) == True:
        cartstatus = "disabled"
        wishstatus = "disabled"

    if checkWish(pid) == True:
        wishstatus = "disabled"
    
    return render_template('productpage.html', nav_show = nav_show, u_show = u_show, item = item, sizes = sizes_list, colors = colors_list, cartstatus = cartstatus, wishstatus = wishstatus, totalcartitems = totalcartitems)

@app.route('/home')
def home():
    sales = countorders()
    users = countusers()
    products = countproducts()
    orders = getorders()
    size = len(orders)
    profit = countprofit()
    if 'admin' not in session:
        return redirect(url_for("adminlogin"))
    return render_template('/Dashboard/home.html', size = size, sales = sales, users = users, products = products, orders = orders, profit = profit)

@app.route('/addproduct', methods=['POST','GET'])
def addproduct():
    errmsg = ""
    sumsg = ""
    categories = getcategories()
    profit = countprofit()
    if 'admin' not in session:
        return redirect(url_for("adminlogin"))
    if request.method == 'POST' and 'upload' in request.form:
        details = request.form.get
        cat = details('category')
        name = details('name')
        price = details('price')
        qty = details('qty')
        sizes = details('sizes')
        colors = details('colors')
        desc = details('desc')
        image = request.files['imgurl']
        if name == "" or price == "" or qty == "" or sizes == "" or colors == "" or desc == "":
            errmsg = "All fields are required"
        elif image.filename == "":
            errmsg = "No image selected"
        elif image and allowed_file(image.filename):
            newimgname = f"{getDate()}{genRandomStr()}.png"
            image.filename = newimgname
            filename = secure_filename(image.filename)  
            image.save(os.path.join('static/products', filename))
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO products (name, price, quantity, sizes, colors, description, imgurl, category) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (name, price, qty, sizes, colors, desc, filename, cat))
            mysql.connection.commit()
            cur.close()
            sumsg = "Product added successfully"
    return render_template('/Dashboard/addproduct.html', categories = categories, sumsg = sumsg, errmsg = errmsg, profit = profit)

@app.route('/manageproduct')
def manageproduct():
    products = getproducts()
    size = len(products)
    profit = countprofit()
    if 'admin' not in session:
        return redirect(url_for("adminlogin"))
    return render_template('/Dashboard/manageproduct.html', products = products, size = size, profit = profit)

@app.route('/manageusers')
def manageusers():
    users = getusers()
    size = len(users)
    profit = countprofit()
    if 'admin' not in session:
        return redirect(url_for("adminlogin"))
    return render_template('Dashboard/manageusers.html', size = size, users = users, len = len, profit = profit)

@app.route('/productdetails', methods=['POST', 'GET'])
def adproductdetails():
    pid = request.args.get('pid')
    profit = countprofit()
    item = getProduct(pid)
    if 'admin' not in session:
        return redirect(url_for("adminlogin"))
    return render_template("/Dashboard/productdetails.html", item = item, profit = profit)

@app.route('/sendemail')
def sendemail():
    profit = countprofit()
    if 'admin' not in session:
        return redirect(url_for("adminlogin"))
    return render_template('Dashboard/sendemail.html', profit = profit)

@app.route('/adminlogin', methods=['POST', 'GET'])
def adminlogin():
    errmsg = ""
    if request.method == 'POST':
        uname = request.form.get('uname')
        passkey = request.form.get('pass')
        if uname == "" or passkey == "":
            errmsg = "All fields are required"
        elif uname == "Admin" and passkey == "1234":
            session['admin'] = "admin"
            return redirect(url_for("home"))
    return render_template('Dashboard/login.html', errmsg = errmsg)

@app.route('/adminlogout')
def adminlogout():
    session.pop('admin', None)
    return redirect(url_for("adminlogin"))

@app.route('/addcart', methods=['POST'])
def shopaddcart():
    msg = ""
    pid = request.form['pid']
    color = request.form['color']
    size = request.form['size']
    qty = request.form['qty']
    if 'key' in session:
        uid = session['key']
        if checkCart(pid) == True:
            msg = "Item already in the cart"
        elif checkWish(pid) == False:
            addToCart(pid, qty, color, size)
            msg = "Item added to cart successfully!"
        else:
            cur = mysql.connection.cursor()
            cur.execute('DELETE FROM wishlist WHERE U_ID = %s AND P_ID = %s', (uid, pid))
            mysql.connection.commit()
            cur.close()
            addToCart(pid, qty, color, size)
            msg = "Item added to cart successfully!"
    else:
        msg = "You're not logged in"
    return msg

@app.route('/remcart', methods=['POST'])
def remcart():
    cid = request.form['cid']
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM cart WHERE C_ID = %s', [cid])
    mysql.connection.commit()
    cur.close()
    return "true"

@app.route('/updatecart', methods=['POST'])
def updatecart():
    cid = request.form['cid']
    col = request.form['col']
    value = request.form['value']
    query = f"UPDATE cart SET {col} = %s WHERE C_ID = %s"
    cur = mysql.connection.cursor()
    cur.execute(query, (value, cid))
    mysql.connection.commit()
    cur.close()
    return "true"

@app.route('/addwish', methods=['POST', 'GET'])
def addwish():
    pid = request.form['pid']
    if 'key' in session:
        uid = session['key']
        if checkWish(pid) == True:
            msg = "Item already in wishlist"
        else:
            addToWish(pid)
            msg = "Item added to wishlist successfully!"
    else:
        msg = "You're not logged in"
    return msg

@app.route('/remwish', methods=['POST'])
def remwish():
    wid = request.form['wid']
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM wishlist WHERE W_ID = %s', [wid])
    mysql.connection.commit()
    cur.close()
    return "true"

@app.route('/updateuser', methods=['POST'])
def updateuser():
    if 'key' in session:
        uid = session['key']
        fname = request.form['fname']
        lname = request.form['lname']
        mobile = request.form['mobile']
        cur = mysql.connection.cursor()
        cur.execute('UPDATE users SET firstname = %s, lastname = %s, mobile = %s WHERE U_ID = %s', (fname, lname, mobile, uid))
        mysql.connection.commit()
        cur.close()
        return "true"
    else:
        return "You're not logged in"

@app.route('/updatebilling', methods=['POST'])
def updatebilling():
    if 'key' in session:
        uid = session['key']
        street = request.form['street']
        state = request.form['state']
        city = request.form['city']
        uzip = request.form['zip']
        cur = mysql.connection.cursor()
        cur.execute('UPDATE users SET street = %s, state = %s, city = %s, zip = %s WHERE U_ID = %s', (street, state, city, uzip, uid))
        mysql.connection.commit()
        cur.close()
        return "true"
    else:
        return "You're not logged in"

@app.route('/updemail', methods=['POST'])
def updemail():
    msg = ""
    if 'key' in session:
        email = getuser()[3]
        token = updateToken(email)
        newemail = request.form['newemail']
        if newemail == email:
            msg = "Please use a different email"
        elif emailexists(newemail):
            msg = "Email already exists"
        else:
            msg = Message('Update email', sender = 'info@crowndidactic.com', recipients = [newemail])
            msg.body = f"Hello chief, A request to update your email was made. This is your verification token {token}. if you do not recognize this activity please ignore this email."
            mail.send(msg)
            session['temp_email'] = email
            session['new_email'] = newemail
            session.pop('key', None)
            msg = 'Successful'
    else:
        msg = "You're not logged in"
    return msg

@app.route('/addorder', methods=['POST'])
def addorder():
    if 'key' in session:
        uid = session['key']
        pids = request.form['pids']
        color = request.form['color']
        size = request.form['size']
        qty = request.form['qty']
        total = request.form['total']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO orders (P_IDS, color, size, qty, U_ID, total) VALUES (%s, %s, %s, %s, %s, %s)', (pids, color, size, qty, uid, total))
        mysql.connection.commit()
        cur.close()
        clearcart()
        return "true"
    else:
        return "You're not logged in"

def verifypass(password):
    if 'key' in session:
        uid = session['key']
        cur = mysql.connection.cursor()
        cur.execute('SELECT passkey FROM users WHERE U_ID = %s', [uid])
        record = cur.fetchone()
        if record:
            passvalid = sha256_crypt.verify(password, record[0])
            if passvalid == True:
                return True
    return False

@app.route('/updatepass', methods=['POST'])
def updatepass():
    if 'key' in session:
        pword = request.form['pass']
        if verifypass(pword) == True:
            email = getuser()[3]
            token = updateToken(email)
            msg = Message('Update Password', sender = 'info@crowndidactic.com', recipients = [email])
            msg.body = f"Hello chief, a request to change your password was made. your one time token is {token}. Please if you do not recognize this activity please ignore this email."
            mail.send(msg)
            session.pop('key', None)
            session['temp_email'] = email
            return "true"
        else:
            return "Invalid password"
    else:
        return "You're not logged in"

@app.route('/logout')
def logout():
    session.pop('key', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)