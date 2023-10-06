import sqlite3

conn = sqlite3.connect('credential1.db')

cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS credentials  (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)''')

def save_credentials(username, password):

    cursor.execute("INSERT INTO credentials (username, password) VALUES (?, ?)", (username, password))

    conn.commit()

    with open("credentials.txt", "a") as file:

        file.write(f"Username: {username}\nPassword: {password}\n\n")

def check_credentials(username, password):

    cursor.execute("SELECT * FROM credentials WHERE username=? AND password=?", (username, password))

    result = cursor.fetchone()  

    if result:
        print("Доступ дозволено")
    else:
        print("направильний логін або пароль")

username = input("Введіть логін: ")
password = input("Введіть пароль: ")

check_credentials(username, password)

conn.close()
