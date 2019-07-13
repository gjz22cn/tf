# -*- coding: utf-8 -*-
import sys
import os
import socket
import time
import RPi.GPIO as GPIO
import picamera
import _thread
import cv2


class TrashClassify():
    def __init__(self):
        # BCM 
        self.IN1 = 18
        self.IN2 = 23
        self.ENA1 = 24
        self.led = 25
        self.out_5 = 16
        self.in_1 = 20
        self.in_2 = 21
        self.init_gpio()

        self.camera = picamera.PiCamera()
        self.camera.resolution = (1080,1080)
        self.camera.framerate = 30

        self.server = ('127.0.0.1', 9999)
        self.sock = self.socket_init()
        self.last_time = time.time()
        self.cnt = 0
        self.res_srv = ('10.10.10.10', 6666)
        self.res_sock = self.socket_init()


    def door_check(self, pin):
        '''
        time.sleep(1)
        now_time = time.time()
        if (now_time - self.last_time) >= 1:
            if GPIO.input(pin):
                self.cnt += 1
                print ("do_classify cnr=%d"%(self.cnt))
                self.do_classify()
                
                # turn led off
                self.set_gpio(self.led, False)
        '''
        if GPIO.input(pin):
            self.cnt += 1
            print ("do_classify cnr=%d"%(self.cnt))
            self.do_classify()
                
            # turn led off
            self.set_gpio(self.out_4, False)


    def door_callback(self, pin):
        # turn led on
        self.set_gpio(self.led, True)

        self.last_time = time.time()
        try:
            _thread.start_new_thread(self.door_check, (pin,))
        except:
            print ("Error: unable to start door check thread")


    def init_gpio(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)
        GPIO.setup(self.ENA1, GPIO.OUT, initial=GPIO.LOW)
        self.pwm1=GPIO.PWM(self.ENA1, 200)
        self.pwm1.start(40)
        GPIO.setup(self.led, GPIO.OUT)
        GPIO.setup(self.in_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        #GPIO.setup(self.in_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.in_1, GPIO.RISING, callback=self.door_callback, bouncetime=500)
        #GPIO.add_event_detect(self.in_2, GPIO.RISING, callback=self.door_callback, bouncetime=500)


    def on_gpio(self, pin, t_sleep):
        GPIO.output(pin,GPIO.HIGH)
        time.sleep(t_sleep)
        GPIO.output(pin, GPIO.LOW)


    def set_gpio(self, pin, v):
        if v:
            GPIO.output(pin, GPIO.HIGH)
        else:
            GPIO.output(pin, GPIO.LOW)

    def dianji1_suspended(self):
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.HIGH)

    def dianji1_brake(self):
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)

    def dianji1_go(self):
        time.sleep(0.2)
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        time.sleep(2)
        self.dianji1_brake()
        #self.on_gpio(self.IN1, 2)

    def dianji1_back(self):
        time.sleep(0.2)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        time.sleep(t_sleep)
        self.dianji1_brake()
        #self.on_gpio(self.IN2, 2)


    def do_classify(self):
        filename = '/tmp/picture.jpg'
        self.pic_cap(0, filename)
        img=cv2.imread(filename,1)
        dst=cv2.resize(img,(299,299))
        cv2.imwrite(filename, dst)
        
        try:
            _thread.start_new_thread(self.query_srv, (filename,))
        except:
            print ("Error: unable to start thread")


    def do_action(self, res):
        print ('res='+res)
        if res != 'ERROR':
            self.start_report_result(res+'-picture.jpg')
            #if res == 'glass' or res == 'metal':
            if res == 'trash':
                self.dianji1_go()
            else:
                self.dianji1_brake()
    
    def pic_cap(self, idx, filename):
        #cmd = 'fswebcam -d /dev/video%d -r 1080x1080 --no-banner %s'%(idx, filename)
        #cmd = 'raspistill -t 300 -o %s -w 1080 -h 1080'%(filename)
        #os.system(cmd)
        #self.camera.start_preview()
        self.camera.capture(filename)
        #self.camera.stop_preview()

    def socket_init(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return client

    def query_srv(self, filename):
        t1 = time.time()
        self.sock.sendto(filename.encode('utf-8'), self.server)
        data, server_addr = self.sock.recvfrom(1024)
        t2 = time.time()
        print ("query time=%ds"%(t2-t1))
        res = data.decode()
        res_array = res.split('\n')
        if len(res_array) < 1:
            return 'ERROR'

        result = res_array[0].split(' ')
        if len(result) < 1:
            return 'ERROR'

        self.do_action(result[0])

        return result[0]


    def start_report_result(self, result):
        try:
            _thread.start_new_thread(self.report_result, (result,))
        except:
            print ("Error: unable to start report_res thread")

    def report_result(self, result):
        self.res_sock.sendto(result.encode('utf-8'), self.res_srv)

    def do_close(self):
        os.system("echo '123456' | sudo -S shutdown -h 0")

    def main_loop(self):
        while True:
            time.sleep(10)



if __name__ == '__main__':
    trashClassify = TrashClassify()
    trashClassify.main_loop()
