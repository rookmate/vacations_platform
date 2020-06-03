from datetime import datetime, timedelta

# This class is meant to perform operations on vacation days as well as set the
# limits reagarding vacation days in PT.
class Vacations:
    __start_date = datetime.now()
    __max_legal_days = 30   # By law the max is 30 days
    __legal_interlude = timedelta(days=180) # Has override option but is negotiable
    __first_year_total_vacation_days = 20   # By law, but is negotiable
    total_vacation_days = 22    # Minimum by law
    used_vacation_days = 0
    is_first_year = True

    def __init__(self, first_year=True, total_days=22, override=False):
        if first_year:
            if total_days > self.__first_year_total_vacation_days and not override:
                # TODO: Add request to override on the frontend
                print(f'Hardcoding vacation days to {self.__first_year_total_vacation_days}.')
                self.total_vacation_days = self.__first_year_total_vacation_days
                self.is_first_year = first_year
                return
        else:
            if total_days > self.__max_legal_days:
                print(f'Hardcoding vacation days to max value {self.__max_legal_days}.')
                self.total_vacation_days = self.__max_legal_days
                return

        self.total_vacation_days = total_days
        self.is_first_year = first_year


    def __repr__(self):
        return {'total days': self.total_vacation_days,
                'days used': self.used_vacation_days,
                'is first year': self.is_first_year
                }

    # The front end will only allow half-days and full-days
    def request_day_off(self, num_days, req_date, override=False):
        if req_date < self.__start_date:
            print(f'Cannot schedule days off before entry date: {self.__start_date.strftime("%Y-%m-%d %H:%M")}')
            return

        if (req_date - self.__start_date) < self.__legal_interlude:
            if not override:
                # TODO: Add request to override on the frontend
                print(f'Cannot schedule before {self.__start_date.strftime("%Y-%m-%d %H:%M")} without authorization')
                return

        if num_days > self.total_vacation_days - self.used_vacation_days:
            print(f'Cannot schedule more than {self.total_vacation_days - self.used_vacation_days} days')
            return

        # TODO: Write to DB
        print(f'Scheduled {num_days} days from {req_date} to {req_date+timedelta(num_days)}')
        self.used_vacation_days += num_days

    def remove_days_off(self, from_date, to_date):
        # TODO: Remove from DB the days requested
        print('Removed days off')


if __name__ == "__main__":
    old = datetime(2020, 8, 5)
    print(old)
    regular = Vacations()
    print(regular.__repr__())
    regular.request_day_off(num_days=3.5, req_date=old, override=True)
    regular.remove_days_off("Chuck", "Testa")
    print(regular.__repr__())
