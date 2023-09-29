import time
import keyboard
import sqlite3 as sq
from tabulate import tabulate
from colorama import init, Fore, Back
from win32api import MessageBox, SetConsoleTitle


class DataBase:
    """Connecting to the database"""

    try:
        with sq.connect(r'statistics.db') as connectDB:
            cursor = connectDB.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS info_typing (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                date TEXT,
                                time_spent TEXT,
                                print_speed INTEGER,
                                count_error INTEGER);''')
    except sq.Error as error:
        print(f'{Fore.RED}{str(error).capitalize()}')

    def write_database(self, date, time_spent, print_speed, count_error):
        """Write the final result to the database"""

        try:
            self.cursor.execute(f'''INSERT INTO info_typing (date, time_spent, print_speed, count_error)
                                    VALUES ('{date}', '{time_spent}', {print_speed}, {count_error})''')
            self.connectDB.commit()
        except sq.Error as error:
            print(f'{Fore.RED}{str(error).capitalize()}')

    def read_database(self):
        """Return all results from the database"""
        try:
            data = self.cursor.execute('''SELECT * FROM info_typing''')
            return data
        except sq.Error as error:
            print(f'{Fore.RED}{str(error).capitalize()}')


class Typing(DataBase):
    def __init__(self):
        self.count_error = 0
        self.time_start = time.time()
        self.time_seconds = 0
        self.final_result_time = ''
        self.speed_typing = 0
        self.chars_count = 0

    @staticmethod
    def console_decoration():
        """Console window design"""

        SetConsoleTitle('Typing')
        print(f'{Fore.BLACK}{Back.YELLOW} *** Do not close the console until the end of the application! *** ')

    def printing_error(self):
        """Add an error to the overall result"""

        self.count_error += 1

    def time_spent(self):
        """Calculate the time spent"""

        self.time_seconds = round(time.time() - self.time_start)
        hours = str(self.time_seconds // 3600)
        minutes = str(self.time_seconds % 3600 // 60)
        seconds = str(self.time_seconds % 3600 % 60)
        result_time = f'{hours.zfill(2)}:{minutes.zfill(2)}:{seconds.zfill(2)}'
        self.final_result_time = result_time
        return result_time

    def print_speed(self):
        """Calculate the print speed"""

        calculate_speed = int(self.chars_count / self.time_seconds * 60)
        self.speed_typing = calculate_speed
        return calculate_speed

    @staticmethod
    def info():
        """Information window for program management"""

        control_buttons = '''
        Control buttons:\n\n
        CTRL+Z - Fix the error\n
        ESC - Finish typing
        '''
        MessageBox(0, control_buttons, 'Information', 0)

    def run(self):
        """Assigning keys to control the program"""

        keyboard.add_hotkey('CTRL+Z', self.printing_error)
        keyboard.remap_key('ENTER', 'RIGHT')

        events = keyboard.record(until='ESC')
        self.chars_count = sum(map(lambda i: len(i), keyboard.get_typed_strings(events)))

        keyboard.unhook_all()

    def result(self):
        """Information window for output of the result"""

        information = f'''
        The end result\n
        Time spent  {self.time_spent()}
        Typing speed - {self.print_speed()}
        Count error - {self.count_error}
        '''
        MessageBox(0, information, 'Information', 0)

    def show_data_db(self):
        """Output of all results from the database to the console"""

        headers = ('id', 'date', 'time_spent', 'print_speed', 'count_error')
        print('\n', tabulate(self.read_database(), headers=headers, stralign='center'))


if __name__ == '__main__':
    init(autoreset=True)

    print_training = Typing()
    print_training.console_decoration()
    print_training.info()

    try:
        print_training.run()
    except KeyboardInterrupt:
        print(f'\n{Fore.RED}Press Ctrl+C or Ctrl+Break in console!')
    else:
        print_training.result()
        print_training.write_database(time.strftime('%X %x'), print_training.final_result_time,
                                      print_training.speed_typing, print_training.count_error)
        print_training.show_data_db()
    finally:
        keyboard.unhook_all()
        input(f'\n{Fore.YELLOW}Press "Enter" to exit the program...')
