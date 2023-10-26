from flask import Flask, render_template, request
import sqlite3
import logging

app = Flask(__name__)


@app.route('/')

def login_form():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = str(request.form['username'])
    password = str(request.form['password'])
    value = request.form['value']
    conn = sqlite3.connect('project/credentials.db')
    cursor = conn.cursor() 
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS credentials (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)''')
    #
    logger = logging.getLogger('project/my_website')
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler('project/my_website')
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(message)s')

    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    def loglogin(username):
        logger.debug(f'Enter the website: {username}')
    #
    def save_credentials(username, password):
        

        cursor.execute("SELECT * FROM credentials WHERE username=?", (username,))
        result = cursor.fetchone()
        if result:
           return render_template('wrongname.html')
        


        cursor.execute("INSERT INTO credentials (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return render_template('newaccount.html')

    def loginn(username, password):

         cursor.execute("SELECT * FROM credentials WHERE username=? AND password=?", (username, password))
         result = cursor.fetchone()
         if result:
            loglogin(username)
            return f'Ви успішно увійшли!'
         else:
            return render_template('wrongdata.html')
    if value == "Реєстрація":
        result = save_credentials(username, password)
    elif value == "Вхід":
        result = loginn(username, password)
    elif value == "Спробувати ще раз" or "Увійти":
        return render_template('login.html')
    elif value == "3":
        return f'Ви ввели імя: {username} і пароль: {password}'
    return result
    conn.close()
    

if __name__ == '__main__':
    app.run(debug=True)

