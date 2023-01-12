from n11deneme import  n11run
from vatan import vatanrun
from hepsiburada import hbrun
from trendyol import trendrun
import threading

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"}

# print("n11")
# n11run(headers,10)
# print("vatan")
# vatanrun(headers,10)
# print("hb")
# hbrun(headers,10)
# print("trend")
# trendrun(headers,10)

if __name__ == "__main__":
    t1 = threading.Thread(target=n11run, args=(headers,35))
    t2 = threading.Thread(target=vatanrun, args=(headers,19))
    t3 = threading.Thread(target=hbrun, args=(headers,35))
    t4 = threading.Thread(target=trendrun, args=(headers,26))

    t1.start()
    t2.start()
    t3.start()
    t4.start()

