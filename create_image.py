import os

with open("hello3.img", 'w') as f:
    f.seek(1024**3*5-1)
    f.write("\x00")

