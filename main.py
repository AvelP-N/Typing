import time
import keyboard
from win32api import MessageBox
import sqlite3 as sq


class DataBase:
    try:
        with sq.connect(r'C:\Users\PNasonov\PycharmProjects\typing\Typing\statistics.db') as connectDB:
            cursor = connectDB.cursor()
    except sq.OperationalError as error:
        print(str(error).capitalize())

    def show_data_db(self):
        self.cursor.execute('''SELECT * FROM info_typing''').fetchall()
        print(self.cursor.fetchall())


class Typing(DataBase):
    def __init__(self):
        self.count_error = 0
        self.time_start = time.time()
        self.time_seconds = 0
        self.chars_count = 0

    def printing_error(self):
        self.count_error += 1

    def time_spent(self):
        self.time_seconds = round(time.time() - self.time_start)
        hours = str(self.time_seconds // 3600)
        minutes = str(self.time_seconds % 3600 // 60)
        seconds = str(self.time_seconds % 3600 % 60)
        return f'{hours.zfill(2)}:{minutes.zfill(2)}:{seconds.zfill(2)}'

    def print_speed(self):
        calculate_speed = self.chars_count / self.time_seconds * 60
        return int(calculate_speed)

    @staticmethod
    def info():
        control_buttons = '''
        Control buttons:\n
        CTRL+Z - Fix the error
        '''
        MessageBox(0, control_buttons, 'Information', 0)

    def run(self):
        keyboard.add_hotkey('CTRL+Z', self.printing_error)
        keyboard.remap_key('ENTER', 'RIGHT')

        events = keyboard.record(until='ESC')
        self.chars_count = sum(map(lambda i: len(i), keyboard.get_typed_strings(events)))

        keyboard.unhook_all()

    def result(self):
        information = f'''
        The end result\n
        Time spent  {self.time_spent()}
        Typing speed - {self.print_speed()}
        Count error - {self.count_error}
        '''
        MessageBox(0, information, 'Information', 0)


if __name__ == '__main__':
    print_training = Typing()
    print_training.info()
    print_training.run()
    print_training.result()
    print_training.show_data_db()
