from flask import Flask, render_template, request, redirect
import sqlite3
import logging
import time
import threading

app = Flask(__name__)
#
logger = logging.getLogger('my_website')
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('my_website')
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(message)s')

file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
        
def logenter(username):
    logger.debug(f'Enter the website: {username}')
def logregistration(username, mail):
    logger.debug(f'User with name: "{username}" and email: "{mail}" has registered')
#
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
                logenter(username)
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

if __name__ == '__main__':
    app.run(debug=True)

