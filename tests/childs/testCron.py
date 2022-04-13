from datetime import datetime as dt

with open("rueba.txt", "wt") as file:
    file.write(str(dt.now()))