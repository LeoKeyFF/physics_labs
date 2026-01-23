import sqlite3

database_path = "database.db"

def create_base(user_name = 'Вася'):
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS RESULTS (
    TaskID INTEGER PRIMARY KEY,
    UserName varchar(255),
    Exercise1 BOOLEAN,
    Exercise2 BOOLEAN
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ACCOUNTS (
    Login varchar(255),
    Password varchar(255),
    Status varchar(255)
    )
    ''')


    connection.commit()
    connection.close()

def add_result(task, exercise1, exercise2):
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    print(task, exercise1, exercise2)

    cursor.execute(
        f"UPDATE RESULTS SET Exercise1 = {exercise1}, Exercise2 = {exercise2} WHERE TaskID = {task}"
    )

    connection.commit()
    connection.close()



def acc_check_for_same_user_name(user_login):
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    logins = cursor.execute(f"SELECT Login FROM ACCOUNTS").fetchall()

    connection.commit()
    connection.close()

    if len(logins) > 0:
        for login in logins:
            if login[0] == user_login:
                return False

    print(logins)

    return True

def acc_sign_up(login, password, status):
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    cursor.execute(
        f"INSERT INTO ACCOUNTS (Login, Password, Status) VALUES ('{login}', '{password}', '{status}')"
    )

    tasks = 3
    for task in range(0, tasks):
        cursor.execute(
            f"INSERT INTO RESULTS (UserName) VALUES ('{login}')"
        )

    connection.commit()
    connection.close()

def sign_in(login, password):
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    password_true = cursor.execute(f"SELECT Password FROM ACCOUNTS WHERE Login = '{login}'").fetchall()
    status = cursor.execute(f"SELECT Status FROM ACCOUNTS WHERE Login = '{login}'").fetchall()

    if len(password_true) > 0:
        password_true = password_true[0][0]
    else:
        return None
    print(password_true)

    if password_true == password:
        if len(status) > 0:
            status = status[0][0]
        return status
    else:
        return False

