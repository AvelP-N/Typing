import time

hours = str(3660 // 3600)
minutes = str(3665 % 3600 // 60)
seconds = str(3765 % 3600 % 60)
print(f'{hours.zfill(2)}:{minutes.zfill(2)}:{seconds.zfill(2)}')
