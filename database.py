import sqlite3

database_path = "database.db"

def create_base():
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS RESULTS (
    TaskID INTEGER PRIMARY KEY,
    TaskNumber INT,
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

def add_result(task, exercise1, exercise2, login):
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()


    cursor.execute(
        f"UPDATE RESULTS SET Exercise1 = {exercise1}, Exercise2 = {exercise2} WHERE TaskNumber = {task} AND UserName = '{login}'"
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

    return True

def acc_sign_up(login, password, status):
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    cursor.execute(
        f"INSERT INTO ACCOUNTS (Login, Password, Status) VALUES ('{login}', '{password}', '{status}')"
    )

    if status == "student":
        tasks = 4
        for task in range(0, tasks):
            cursor.execute(
                f"INSERT INTO RESULTS (TaskNumber, UserName) VALUES ('{task + 1}', '{login}')"
            )

    connection.commit()
    connection.close()

def sign_in(login, password):
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    password_true = cursor.execute(f"SELECT Password FROM ACCOUNTS WHERE Login = '{login}'").fetchall()
    status = cursor.execute(f"SELECT Status FROM ACCOUNTS WHERE Login = '{login}'").fetchall()

    connection.close()

    if len(password_true) > 0:
        password_true = password_true[0][0]
    else:
        return None

    if password_true == password:
        if len(status) > 0:
            status = status[0][0]
        return status
    else:
        return False

def get_stat():
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    stat = []
    logins_ = cursor.execute(f"SELECT UserName FROM RESULTS").fetchall()
    logins=[]

    if len(logins_) > 0:
        for l in logins_:
            if l[0] not in logins:
                logins.append(l[0])

    for login in logins:
        for task_number in range(1, 5):
            ex1 = cursor.execute(
                f"SELECT Exercise1 FROM RESULTS WHERE UserName = '{login}' AND TaskNumber = {task_number}"
            ).fetchall()[0][0]
            ex2 = cursor.execute(
                f"SELECT Exercise2 FROM RESULTS WHERE UserName = '{login}' AND TaskNumber = {task_number}"
            ).fetchall()[0][0]
            if ex1 is None:
                ex1 = "Не приступал(а)"
            elif ex1 == 1:
                ex1 = "Правильно"
            else:
                ex1 = "Ошибка"

            if ex2 is None:
                ex2 = "Не приступал(а)"
            elif ex2 == 1:
                ex2 = "Правильно"
            else:
                ex2 = "Ошибка"

            stat.append(
                {
                    "login":login,
                    "task_number":task_number,
                    "ex1": ex1,
                    "ex2":ex2
                }
            )
    connection.close()
    return stat

def clean_base():
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    cursor.execute(
        f"DELETE FROM RESULTS"
    )

    cursor.execute(
        f"DELETE FROM ACCOUNTS"
    )

    connection.commit()
    connection.close()




