
import time

while True:
    try:
        for i in range(1,500):
            time.sleep(5)
            f=open('test.html','w',encoding='UTF-8')
            f.write('<h1>')
            f.write(str(i))
            f.write('</h1>')
            f.close()
            print(i)
    except KeyboardInterrupt:
        f.close()



