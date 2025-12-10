import sqlite3
import secrets
import string
from cryptography.fernet import Fernet

# Генерация ключа для шифрования (его нужно сохранить)
def generate_key():
    return Fernet.generate_key()

# Инициализация шифрования
key = generate_key()
cipher = Fernet(key)

# Генерация пароля
def generate_password(length: int) -> str:
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))

# Шифрование пароля
def encrypt_password(password: str) -> str:
    return cipher.encrypt(password.encode()).decode()

# Дешифровка пароля
def decrypt_password(encrypted_password: str) -> str:
    return cipher.decrypt(encrypted_password.encode()).decode()

# Создание или подключение к базе данных SQLite
def create_database():
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    # Создание таблицы для хранения паролей
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS passwords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        en_password TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

# Добавление пароля в БД
def add_password(username: str, password: str):
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    encrypted_password = encrypt_password(password)
    cursor.execute('INSERT INTO passwords (username, encrypted_password) VALUES (?, ?)', (username, encrypted_password))
    conn.commit()
    conn.close()

# Получение пароля из БД
def get_password(username: str) -> str:
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    cursor.execute('SELECT encrypted_password FROM passwords WHERE username = ?', (username,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return decrypt_password(row[0])
    return None

# Основной блок
if __name__ == "__main__":
    print("Классно, верно?")
    # Создание базы данных
    create_database()

    # Генерация и добавление пароля
    username = input("Введите имя пользователя: ")
    password = generate_password(16)  # Генерируем пароль длиной 16 символов
    print(f"Сгенерированный пароль: {password}")
    add_password_to_db(username, password)

    # Получение пароля из базы данных
    retrieved_password = get_password_from_db(username)
    print(f"Пароль для {username}: {retrieved_password}")
