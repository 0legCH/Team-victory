from flask import Flask, render_template, request, redirect
import sqlite3
import logging
import time
import threading

app = Flask(__name__)
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
        cursor.execute('''CREATE TABLE IF NOT EXISTS credentials (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, mail TEXT)''')
 
        def login(username, password):
            global wrong_data_try
            cursor.execute("SELECT * FROM credentials WHERE username=? AND password=?", (username, password))
            result = cursor.fetchone()
            if result:
                cursor.execute("SELECT mail FROM credentials WHERE username = ?;", (username,))
                result = cursor.fetchone()
                logenter(username, result)
                
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
        conn = sqlite3.connect('credentials.db')
        cursor = conn.cursor() 
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS credentials (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, mail TEXT)''')
        def save_credentials(username, password, mail):
        

            cursor.execute("SELECT * FROM credentials WHERE username=?", (username,))
            result = cursor.fetchone()
            if result:
                return redirect('/wrongname')
            


            cursor.execute("INSERT INTO credentials (username, password, mail) VALUES (?, ?, ?)", (username, password, mail))
            conn.commit()
            logregistration(username, mail)
            return redirect('/newaccount')
        if value == "Зареєструватися":
            resalt1 = save_credentials(username, password, mail)
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


@app.route('/product/<int:product_id>')
def product_detail(product_id):
    conn = sqlite3.connect('products.db') #ТУТ МАЄ БУТИ ВАШ ПОВНИЙ ШЛЯХ ДО ФАЙЛУ БАЗИ
    cursor = conn.cursor()
    def get_product_by_id(product_id):
        cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
        return cursor.fetchone()
    product = get_product_by_id(product_id)
    if product is None:
        return "Товар не знайдено"

    return render_template('product_detail.html', product=product)

@app.route('/product/new_product',methods=['POST', 'GET'] )
def new_product():
    if request.method == "POST":
        #
        conn = sqlite3.connect('products.db')
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
            return(f"ID: {product[0]}, Name: {product[1]}, Description: {product[2]}, Price: {product[3]}, Image: {product[4]}")
    else:
      return  render_template('new_product.html')


if __name__ == '__main__':
    app.run(debug=True)

