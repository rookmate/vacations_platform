import sqlite3

# This class will manage the db interactions
class SqliteDb:
    db = None

    def __init__(self, dbname='vacations.db'):
        print(f'Connecting to database {dbname}')

        self.db = sqlite3.connect(dbname)
        c = self.db.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS users (
                              id INTEGER PRIMARY KEY AUTOINCREMENT,
                              first_name TEXT NOT NULL,
                              last_name TEXT NOT NULL,
                              days_used INTEGER DEFAULT 0,
                              total_days INTEGER NOT NULL CHECK(length(total_days) > 0),
                              birth_date TEXT NOT NULL,
                              date_of_entry TEXT NOT NULL,
                              status TEXT DEFAULT 'active' CHECK(status == 'active' OR status == 'inactive'), -- inactive or active
                              UNIQUE(first_name, last_name)
                            )''')

        c.execute('''CREATE TABLE IF NOT EXISTS calendar_events (
                              id INTEGER PRIMARY KEY AUTOINCREMENT,
                              user_id NOT NULL,
                              description,
                              kind NOT NULL, -- vacation or sick
                              begin_date NOT NULL,
                              end_date NOT NULL,
                              FOREIGN KEY (user_id) REFERENCES users (id)
                            )''')

        c.execute("SELECT name FROM sqlite_master WHERE type='table'")
        print(c.fetchall())


    def add_user(self, user=None):
        if user is None:
            print(f'No user provided: {user}')
            return

        c = self.db.cursor()
        # Validate that the user does not exist yet
        try:
            c.execute('''INSERT INTO users
                      VALUES (NULL,?,?,?,?,?,?,?)
                      ''', (user.first_name, user.last_name,
                            user.days_used, user.total_vacation_days,
                            user.birth_date, user.entry_date, user.status,
                            )
                      )
            self.db.commit()
        except Exception as e:
            print(f'User {user.first_name} {user.last_name} already exists. Error: {e}')


    def rm_user(self, user=None):
        if user is None:
            print(f'No user provided: {user}')
            return

        c = self.db.cursor()
        c.execute('''DELETE FROM users
                  WHERE first_name == ? AND last_name == ?
                  ''', (user.first_name, user.last_name,)
                  )
        self.db.commit()


    def update_user(self, user=None, full_row=True):
        # Always replace full row, unless we figure out what column to change
        # eventually
        if user is None:
            print(f'No user provided: {user}')
            return

        c = self.db.cursor()
        try:
            if full_row:
                c.execute('''UPDATE users
                          SET first_name = ?,
                              last_name = ?,
                              days_used = ?,
                              total_days = ?,
                              birth_date = ?,
                              date_of_entry = ?,
                              status = ?
                          WHERE (SELECT id
                                 FROM users
                                 WHERE first_name == ? AND last_name == ?)
                          ''', (user.first_name, user.last_name,
                                user.days_used, user.total_vacation_days,
                                user.birth_date, user.entry_date, user.status,

                                user.first_name, user.last_name,
                                )
                          )
            else:
                print("Not a full row.")
                return
        except Exception as e:
            print(f'Could not update user {user.first_name} {user.last_name}. Error: {e}')
        self.db.commit()


    def add_calendar_event(self, user=None, cal_event=None):
        pass

    def rm_calendar_event(self):
        pass

    def user_events(self, user=None, begin_date=None, end_date=None):
        pass


if __name__ == "__main__":
    from user import User
    db = SqliteDb()
    u1 = User('John', 'Doe', '1990-05-02', '2020-02-01')
    db.add_user(u1)
    print(db.db.cursor().execute("SELECT * FROM users").fetchall())

    u1.total_vacation_days = 27
    u1.status = 'inactive'
    db.update_user(u1)
    print(db.db.cursor().execute("SELECT * FROM users").fetchall())

    db.rm_user(u1)
    print(db.db.cursor().execute("SELECT * FROM users").fetchall())

