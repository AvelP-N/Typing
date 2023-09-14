import time
import keyboard
from win32api import MessageBox


class Typing:
    def __init__(self):
        self.count_error = 0
        self.time_start = time.time()

    def printing_error(self):
        self.count_error += 1

    def time_spent(self):
        time_seconds = round(time.time() - self.time_start)
        hours = str(time_seconds // 3600)
        minutes = str(time_seconds % 3600 // 60)
        seconds = str(time_seconds % 3600 % 60)
        return f'{hours.zfill(2)}:{minutes.zfill(2)}:{seconds.zfill(2)}'

    def run(self):
        keyboard.add_hotkey('CTRL+Z', self.printing_error)
        keyboard.remap_key('ENTER', 'RIGHT')
        keyboard.wait('ESC')

    def result(self):
        information = f"""
        The end result\n
        Time spent  {self.time_spent()}
        Count error - {self.count_error}
        """
        MessageBox(0, information, 'Information', 0)
        print(information)


if __name__ == '__main__':
    print_training = Typing()
    print_training.run()
    print_training.result()
