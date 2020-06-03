from days_off import Vacations

# This class will be the representation of a user. It will sanitize the data
# to add and input users in the database.
class User(Vacations):
    status = 'active'

    def __init__(self, firstn, lastn, birthd, entry, firstyear=True, totaldays=22, override=True):
        super(User, self).__init__(bool(firstyear), int(totaldays), bool(override))
        self.first_name = str(firstn)
        self.last_name = str(lastn)
        self.birth_date = str(birthd)
        self.entry_date = str(entry)

    def __repr__(self):
        return {'first name': self.first_name,
                'last name': self.last_name,
                'birth_date': self.birth_date,
                'date of entry': self.entry_date,
                'status': self.status,
                'Vacation details': super(User, self).__repr__()
                }


if __name__ == "__main__":
    from datetime import datetime
    u1 = User('Jane', 'Doe', '1990-05-08', '2020-02-01', "Tue", 22, True)
    print(u1.__repr__())
    u1.request_day_off(num_days=3.5, req_date=datetime(2020, 5, 8), override=True)
