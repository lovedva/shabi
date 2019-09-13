#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
import threading
import time
import pid60Ctr
import pid70Ctr
import pid90Ctr
import sys
import adt7410
import pt1000
import RPi.GPIO

exitFlag = 0
TempOUT1=12 #60度
TempOUT2=23 #70度
TempOUT3=15 #90度
RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setup(TempOUT1, RPi.GPIO.OUT)
RPi.GPIO.setup(TempOUT2, RPi.GPIO.OUT)
RPi.GPIO.setup(TempOUT3, RPi.GPIO.OUT)

 
class myThread (threading.Thread):   #继承父类threading.Thread
    def __init__(self, threadID, name, pidName): #pidName传数字
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.pidName=pidName
        # self.counter = counter
    def run(self):                   #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数 
        # print "Starting " + self.name
        # print_time(self.name, self.counter, 5)
        # print "Exiting " + self.name

        if self.pidName==60:
            RPi.GPIO.setmode(RPi.GPIO.BCM)
            RPi.GPIO.setup(TempOUT1, RPi.GPIO.OUT)
            RPi.GPIO.setup(TempOUT2, RPi.GPIO.OUT)
            RPi.GPIO.setup(TempOUT3, RPi.GPIO.OUT)
            #设置pwm输出占空比
            pwm=RPi.GPIO.PWM(TempOUT1,5)#pwm周期200ms
            pwm.start(1)
            #创建pid控制器对象
            pid60=pid60Ctr.pidCtr()
            #准备写入文件
            file_handle=open('60Templog.txt',mode='w')
            xls.creatxls()
            #循环控制温度
            while True:
                time.sleep(0.5)
                pid60.Pv=float(pt1000.calcTemp(4,5))
                print("Pt1000で測温[4,5]==%s\n温度センサー测温[4,5]==%s度\n-----------------------------"%(pid60.Pv, adt7410.read_adt7410()))
                file_handle.write("%s | "%pid60.Pv)
                pid60.calc()
                # print("pidCr.OUTの計算結果==%s"%pid60.OUT)
                dc=pid60.OUT/pid60.pwmcycle*100
                pwm.ChangeDutyCycle(dc)
                # print("PWM信号のDutyCyle：%s"%dc)
                # file_handle.write("%s ;\n"%dc)
                
            file_handle.close()
        elif self.pidName==70:
             #设置pwm输出占空比
            pwm=RPi.GPIO.PWM(TempOUT2,5)#pwm周期200ms
            pwm.start(1)
            #创建pid控制器对象
            pid70=pid70Ctr.pidCtr()
            #准备写入文件
            file_handle=open('70Templog.txt',mode='w')
            #循环控制温度
            while True:
                time.sleep(0.5)
                pid70.Pv=float(pt1000.calcTemp(2,3))
                print("Pt1000で測温[2,3]==%s\n温度センサー测温[2,3]== None度\n-----------------------------"%pid70.Pv)
                # print("温度センサー测温[4,5]==%s度"%adt7410.read_adt7410())
                file_handle.write("%s | "%pid70.Pv)
                pid70.calc()
                # print("pidCr.OUTの計算結果==%s"%pid70.OUT)
                dc=pid70.OUT/pid70.pwmcycle*100
                pwm.ChangeDutyCycle(dc)
                # print("PWM信号のDutyCyle：%s"%dc)
                # file_handle.write("%s ;\n"%dc)
                
            file_handle.close()
        elif self.pidName==90:
             #设置pwm输出占空比
            pwm=RPi.GPIO.PWM(TempOUT3,5)#pwm周期200ms
            pwm.start(1)
            #创建pid控制器对象
            pid90=pid90Ctr.pidCtr()
            #准备写入文件
            file_handle=open('90Templog.txt',mode='w')
            #循环控制温度
            while True:
                time.sleep(0.5)
                pid90.Pv=float(pt1000.calcTemp(0,1))
                print("Pt1000で測温[0,1]==%s\n温度センサー测温[0,1]== None度\n-----------------------------"%pid90.Pv)
                # print("温度センサー测温[4,5]==%s度"%adt7410.read_adt7410())
                file_handle.write("%s | "%pid90.Pv)
                pid90.calc()
                # print("pidCr.OUTの計算結果==%s"%pid90.OUT)
                dc=pid90.OUT/pid90.pwmcycle*100
                pwm.ChangeDutyCycle(dc)
                # print("PWM信号のDutyCyle：%s"%dc)
                # file_handle.write("%s ;\n"%dc)
            file_handle.close()
 
def print_time(threadName, delay, counter):
    while counter:
        if exitFlag:
            (threading.Thread).exit()
        time.sleep(delay)
        print "%s: %s" % (threadName, time.ctime(time.time()))
        counter -= 1
 
if __name__ == "__main__":
    try:
        TempOUT1=12 #60度
        TempOUT2=23 #70度
        TempOUT3=15 #90度
        RPi.GPIO.setmode(RPi.GPIO.BCM)
        RPi.GPIO.setup(TempOUT1, RPi.GPIO.OUT)
        RPi.GPIO.setup(TempOUT2, RPi.GPIO.OUT)
        RPi.GPIO.setup(TempOUT3, RPi.GPIO.OUT)
        # 创建新线程
        thread1 = myThread(1, "pid60", 60)
        thread2 = myThread(2, "pid70", 70)
        thread3 = myThread(3, "pid90", 90)
         
        # 开启线程
        thread1.start()
        thread2.start()
        thread3.start()
    finally:
        #RPi.GPIO.cleanup()
        pass