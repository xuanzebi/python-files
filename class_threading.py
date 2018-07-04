import threading
import queue

import time


class thread_1(threading.Thread):   # 继承多线程threading类


    def __init__(self,thread_id,name):  #初始化  在实例这个类的时候会调用init
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        #print(threading.current_thread())

    def run(self):
        k = int(0)
        while(k < 1000):
            k += 1
            print(threading.current_thread().name)
            print('当前运行的线程 %s 和当前k的数值为 %s' % (self.name,k))
            #time.sleep(0.5)

    # def spider(self,thread_id):
    #     while True:
    #         if self.queue.empty():   # 判断队列是否为空
    #             break
    #         else:
    #             page = self.queue.get()  #获取队列中元素
    #             print('当前正在工作的线程是,{}'.format(self,thread_id) )


class thread_2(threading.Thread):
    def __init__(self,thread_id,name):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name


    def run(self):
        n = 0
        while(n < 1000):
            n += 1
            self.test()
            print(threading.current_thread().name)
            print('当前运行的线程 %s 和当前n的数值为 %s' % (self.name ,n))
            #time.sleep(1)

    def test(self):
        print("测试成功")
thread_1 = thread_1(1,'thread1')
thread_2 = thread_2(2,'thread2')

thread_1.start()
thread_2.start()
thread_1.join()    # 必须等thread_1 中全部运行完才
thread_2.join()    # 必须等thread_2 中全部运行完才

#如果不加 join 的话 会出现
# thread1
# thread2
# 当前运行的线程 thread1 和当前k的数值为 12
# 当前运行的线程 thread2 和当前n的数值为 7
# 即 线程2 不用等1运行完就可以运行
# # !/usr/bin/python
# # -*- coding: UTF-8 -*-
#
# import threading
# import time
#
# exitFlag = 0
#
#
# class myThread(threading.Thread):  # 继承父类threading.Thread
#                                    # self 代表类的实例，self 在定义类的方法时是必须有的，虽然在调用时不必传入相应的参数。
#     def __init__(self, threadID, name, counter):
#         threading.Thread.__init__(self)
#         self.threadID = threadID
#         self.name = name
#         self.counter = counter
#
#     def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
#         print  "Starting " + self.name
#         print_time(self.name, self.counter, 5)
#         print "Exiting " + self.name
#
#
# def print_time(threadName, delay, counter):
#     while counter:
#         if exitFlag:
#             (threading.Thread).exit()
#         time.sleep(delay)
#         print "%s: %s" % (threadName, time.ctime(time.time()))
#         counter -= 1
#
#
# # 创建新线程
# thread1 = myThread(1, "Thread-1", 1)
# thread2 = myThread(2, "Thread-2", 2)
#
# # 开启线程
# thread1.start()
# thread2.start()
#
# print "Exiting Main Thread"