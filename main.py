import database
from my_main_app import MainApp

if __name__ == '__main__':
    database.create_base()
    app = MainApp()
    app.mainloop()
    exit(0)