import mmap
import time

offset = 0

now = time.time()
now += 24*60*60*offset
today = time.localtime(now)
filename = time.strftime("/home/jcgregorio/log/bitworking.org/%Y%m%d.log", today)
map = mmap.mmap(file(filename, "r+").fileno(), 1, access=mmap.ACCESS_READ)
line = map.readline()
while line != "":
    print line
    line = map.readline()


