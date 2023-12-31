from flask import Flask, render_template, request, redirect
import sqlite3
import logging
import time
import threading

app = Flask(__name__)
#Данні профіля
def makeadmin():
    global status
    status = "admin"
def makeuser():
    global status 
    status = "user" 
def set_profiledata(username,mail):
    global profileusername
    global profilemail

    profileusername = username
    profilemail = mail[0]
#

#Початок логування
logger = logging.getLogger('my_website')
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('my_website')
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(message)s')

file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def logenter(username, mail):
    logger.debug(f'Enter the website: "{username}" and email: "{mail}"')
def logregistration(username, mail):
    logger.debug(f'User with name: "{username}" and email: "{mail}" has registered')
#Кінець логування
#Список товарів
products = {
    1: {"name": "Mortal Kombat 11 Ultimate PS5", "description": '"Mortal Kombat 11" - це відеогра з жанру файтингу, випущена в 2019 році. Гра розвиває популярну серію "Mortal Kombat" і пропонує гравцям динамічні поєдинки між різними бійцями, кожен з яких має свої унікальні прийоми та смертоносні фінішери. "Mortal Kombat 11" славиться красивою графікою, кровопролитними битвами і широким списком персонажів, включаючи ветеранів серії та нових героїв. Гра також має захоплюючий сюжетний режим, який розкриває історію Мортал Комбату і його персонажів.', "price": 999, "image": "items/1.webp"},
    2: {"name": "Товар 2", "description": "Властивості товару 2", "price": 20.00, "image": "items/2.webp"},
    3: {"name": "Товар 1", "description": "Властивості товару 1", "price": 10.00, "image": "items/3.webp"},
    4: {"name": "Товар 2", "description": "Властивості товару 2", "price": 20.00, "image": "items/4.webp"},
    5: {"name": "Товар 1", "description": "Властивості товару 1", "price": 10.00, "image": "items/5.webp"},
    6: {"name": "Товар 2", "description": "Властивості товару 2", "price": 20.00, "image": "items/6.webp"},
    7: {"name": "Товар 1", "description": "Властивості товару 1", "price": 10.00, "image": "items/7.webp"},
    8: {"name": "Товар 2", "description": "Властивості товару 2", "price": 20.00, "image": "items/8.webp"},
    9: {"name": "Товар 1", "description": "Властивості товару 1", "price": 10.00, "image": "items/9.webp"},
    10: {"name": "Товар 2", "description": "Властивості товару 2", "price": 20.00, "image": "items/10.webp"},
    11: {"name": "Товар 1", "description": "Властивості товару 1", "price": 10.00, "image": "items/11.webp"},
    12: {"name": "Товар 2", "description": "Властивості товару 2", "price": 20.00, "image": "items/12.webp"},
    13: {"name": "Товар 1", "description": "Властивості товару 1", "price": 10.00, "image": "items/13.webp"},
    14: {"name": "Товар 2", "description": "Властивості товару 2", "price": 20.00, "image": "items/14.webp"},
    15: {"name": "Товар 1", "description": "Властивості товару 1", "price": 10.00, "image": "items/15.jpg"},
    16: {"name": "Товар 2", "description": "Властивості товару 2", "price": 20.00, "image": "items/16.webp"},
}
#Кінець списку

wrong_data_try = 0
def reset_wrongdatatry():
    global wrongdatatry
    while True:
        time.sleep(10)
        wrongdatatry = 0
reset_thread = threading.Thread(target=reset_wrongdatatry)


@app.route('/', methods=['POST', 'GET'])

def login_form():
    if request.method == "POST":
        username = str(request.form['username'])
        password = str(request.form['password'])

        value = request.form['value']
        conn = sqlite3.connect('credentials.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS credentials (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, mail TEXT, status TEXT)''')

        def login(username, password):
            global wrong_data_try
            cursor.execute("SELECT * FROM credentials WHERE username=? AND password=?", (username, password))
            result = cursor.fetchone()
            if result:
                cursor.execute("SELECT mail FROM credentials WHERE username = ?;", (username,))
                result = cursor.fetchone()
                logenter(username, result)
                set_profiledata(username, result)
                makeuser()

                return 'main'
            else:
                wrong_data_try += 1
                if wrong_data_try < 2:
                    return '/wrongdata'
                else:
                    return '/wrongdatalimit'
        if value == "Вхід":
            resalt = login(username, password)
        return redirect(resalt)
    else:
        return render_template('login.html')


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == "POST":
        username = str(request.form['username'])
        mail = str(request.form['mail'])
        password = str(request.form['password'])
        value = request.form['value']
        makeuser()
        global status
        conn = sqlite3.connect('credentials.db')
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS credentials (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, mail TEXT, status TEXT)''')
        def save_credentials(username, password, mail, status):


            cursor.execute("SELECT * FROM credentials WHERE username=?", (username,))
            result = cursor.fetchone()
            if result:
                return redirect('/wrongname')



            cursor.execute("INSERT INTO credentials (username, password, mail, status) VALUES (?, ?, ?, ?)", (username, password, mail, status))
            conn.commit()
            logregistration(username, mail)
            return redirect('/newaccount')
        if value == "Зареєструватися":
            resalt1 = save_credentials(username, password, mail, status)
        return resalt1
    else:
        return render_template('registration.html')


@app.route('/newaccount')
def newaccount():
    return render_template('newaccount.html')


@app.route('/wrongdata')
def wrongdata():
    return render_template('wrongdata.html')


@app.route('/wrongname')
def wrongname():
    return render_template('wrongname.html')


@app.route('/main')
def main():
    return render_template('main.html')


@app.route('/wrongdatalimit')
def wrongdatalimit():
    return render_template('wrongdatalimit.html')


@app.route('/product/<int:product_id>', methods=['POST', 'GET'])
def product_detail(product_id):
    if request.method == "POST":
        value = request.form['value']
        if value == "Купити":
            conn = sqlite3.connect('C:/Users/User/Documents/team/Team-victory/products.db')
            cursor = conn.cursor()


            def get_product_by_id(product_id):
                cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
                return cursor.fetchone()

            product = get_product_by_id(product_id)
            name = product[1]
            price = product[3]
            conn.close()

            conn = sqlite3.connect('C:/Users/User/Documents/team/Team-victory/project/basket_database.db')
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS cart
                              (id INTEGER PRIMARY KEY AUTOINCREMENT,
                              name TEXT NOT NULL,
                              price REAL NOT NULL,
                              quantity INTEGER NOT NULL)''')
            
            cursor.execute('SELECT COUNT(*) FROM cart WHERE name = ?', (name,))
            count = cursor.fetchone()[0]
            if count > 0:
                cursor.execute('SELECT quantity FROM cart WHERE name = ?', (name,))
                current_quantity = cursor.fetchone()[0]
                new_quantity = current_quantity + 1
                cursor.execute('UPDATE cart SET quantity = ? WHERE name = ?', (new_quantity, name))
  
                
                conn.commit()
                conn.close()
            else:
                cursor.execute('INSERT INTO cart (name, price, quantity) VALUES (?, ?, ?)', (name, price, 1))
                conn.commit()
                conn.close()
            return redirect('/basket')
    else :
        conn = sqlite3.connect('C:/Users/User/Documents/team/Team-victory/products.db')
        cursor = conn.cursor()
        def get_product_by_id(product_id):
            cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
            return cursor.fetchone()
        product = get_product_by_id(product_id)
        if product is None:
            return "Товар не знайдено"
        conn.close()

        return render_template('product_detail.html', product=product)


@app.route('/product/new_product',methods=['POST', 'GET'] )
def new_product():
    if request.method == "POST":
        #
        conn = sqlite3.connect('C:/Users/User/Documents/team/Team-victory/products.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                description TEXT,
                price REAL,
                image TEXT
            )
        ''')
        conn.commit()

        def add_product(name, description, price, image):

            cursor.execute('''
                INSERT INTO products (name, description, price, image)
                VALUES (?, ?, ?, ?)
            ''', (name, description, price, image))
            conn.commit()

        def get_product_by_id(product_id):
            cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
            return cursor.fetchone()
        #
        name = str(request.form['name'])
        description = str(request.form['description'])
        price = str(request.form['price'])
        image = str(request.form['image'])
        value = str(request.form['value'])
        if value == "створити":
            add_product(name, description, price, image)
            product = get_product_by_id(1)
            conn.close()
            return redirect("/main")
    else:
      return  render_template('new_product.html')


@app.route('/profile')
def profile():
    global profileusername
    global profilemail
    global status
    stat = status
    username = profileusername
    mail = profilemail
    return render_template('profile.html', username= username, mail = mail, status = stat)


@app.route('/basket')
def show_cart():
    conn = sqlite3.connect('C:/Users/User/Documents/team/Team-victory/project/basket_database.db')
    cursor = conn.cursor()


    cursor.execute('SELECT * FROM cart')
    cart_items = cursor.fetchall()


    conn.close()
    price = 0
    for item in cart_items:
        price += item[3]* item[2]

    return render_template('goods.html', cart_items=cart_items, price = price)


@app.route('/product')
def product():
    conn = sqlite3.connect('C:/Users/User/Documents/team/Team-victory/products.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall() 
    return render_template('productslist.html', products=products)




if __name__ == '__main__':
    app.run(debug=True)

