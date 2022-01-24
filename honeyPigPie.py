import sqlite3
import time
import subprocess
from turtle import Turtle,Screen
from turtlePieChart import pie

def printFinal(f = './data/honeyPigPie'+time.strftime("%Y%m%d-%H%M%S")+'.ps'):
    print(f)
    canvas = window.getcanvas()
    canvas.postscript(file=f)
    subprocess.call(['lpr', f])

def dbLand(this_pig):#import sqlite3#https://www.sqlite.org/inmemorydb.html
    conn = sqlite3.connect(this_pig.db)#You can also supply the special name :memory: to create a database in RAM.
    c = conn.cursor()
    c.execute(this_pig.sql)
    this_pig.ds = c.fetchall()
    conn.commit()
    conn.close()


if __name__ == "__main__":
    leo = Turtle(shape="turtle")
    leo.ht()
    leo.speed(10)
    leo.penup()
    tp = (0,-300)
    leo.setposition(tp)
    startrad = 400
    leo.rad = startrad
    leo.db = './data/Bastards.db copy'
    window = Screen()
    window.setup(1200, 1024)
    #window.bgcolor("white smoke")
    window.bgcolor("black")
    window.colormode(255)
    window.setup(startx=None, starty=None)
    #days = [26,27,28,29,30,31,1,2,3,4,5,6,7,8,9,10,11,12,13]
    if not 'loop':
        days = ['09',10,11,12]
        for dt in days:
            leo.sql = 'select "clientIP" pewpew, count(clientIP) cnt\
                 from packet where substr(last_seen,9,2) = "'+str(dt)+'" group by clientIP, \
                substr(last_seen,0,10) order by substr(last_seen,9,2),clientIP;'
            leo.rad = leo.rad-(startrad/len(days))
            #leo.sql = 'select "clientIP" pewpew, count(clientIP) cnt from packet group by clientIP;'
            dbLand(leo)
            pie(leo)
    else:
        #leo.sql = 'select "clientIP" pewpew, count(clientIP) cnt from packet group by clientIP;'
        leo.sql =  "select coalesce(domainName, 'Unknown') Dom, count(domainName) cnt from packet left join packeteer on packet.clientIP = packeteer.clientIP group by domainName having count(domainName)>10 order by domainName;"
        dbLand(leo)
        pie(leo)
    if 1: printFinal()
