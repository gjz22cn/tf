# -*- coding: utf-8 -*-
import sys
import os
import socket
import time
import datetime
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
        self.IN3 = 12
        self.IN4 = 16
        self.ENA2 = 25
        self.in_1 = 20
        self.in_2 = 21
        self.pwm1 = None
        self.pwm2 = None
        self.P_IN_LEFT = 5
        self.P_IN_MID  = 13
        self.P_IN_RIGHT = 6
        self.root_dir = '/mnt/udisk/trash'
        self.trash = ['baozhuangsuliaodai', 'feizhi', 'peel', 'suliaobei', 'xiaomubang', 'xiguan', 'zhibei']
        self.recyclable = ['carboard', 'metal', 'plastic', 'paper', 'glass']
        self.dianji_state = 'brake' 
        self.path_init()
        self.init_gpio()

        self.camera = picamera.PiCamera()
        self.camera.resolution = (1080,1080)
        self.camera.framerate = 30

        self.server = ('127.0.0.1', 9999)
        self.sock = self.socket_init()
        self.last_time = time.time()
        self.res_srv = ('10.10.10.10', 6666)
        self.res_sock = self.socket_init()
        self.cnt = 0;
        #time.sleep(300)
        self.do_classify()
        #self.dianji1_right()
        #self.dianji1_left()

    def path_init(self):
        if not os.path.exists(self.root_dir):
            return

        for item in self.trash:
            sub_dir = os.path.join(self.root_dir, item)
            if not os.path.exists(sub_dir):
                os.mkdir(sub_dir)

    def store_img(self, source, category):
        if category == 'none':
            return

        if not os.path.exists(self.root_dir):
            return
        
        dst_dir = os.path.join(self.root_dir, category)
        if not os.path.exists(dst_dir):
            os.mkdir(dst_dir)
                
        now_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        cmd = 'cp ' + source + ' ' + dst_dir + '/' + category + '_' + now_time + '.jpg'
        try:
            print (cmd)
            os.system(cmd)
        except:
            print ("Error: unable to store image.")


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
            #self.cnt += 1
            #print ("do_classify cnr=%d"%(self.cnt))
            #self.do_classify()
                
            # turn led off
            #self.set_gpio(self.led, False)
            print ("door open. %d\n"%(self.cnt))
        else:
            self.cnt += 1
            print ("do_classify cnr=%d"%(self.cnt))
            #self.do_classify()
            #self.set_gpio(self.led, False)
            self.do_classify()
            self.dianji_suspended(2)
            print ("door close. %d\n"%(self.cnt))


    def door_callback(self, pin):
        # turn led on
        #self.set_gpio(self.led, True)
        self.dianji_go_full_speed(2)

        self.last_time = time.time()
        try:
            _thread.start_new_thread(self.door_check, (pin,))
        except:
            print ("Error: unable to start door check thread")

    def p_callback(self, pin):
        if (pin == self.P_IN_LEFT) and (GPIO.input(5) == 0):
            if self.dianji_state != 'right':
                self.dianji_action(1, 'brake')
                time.sleep(0.2)
                self.dianji_action(1, 'right')
        
        if (pin == self.P_IN_RIGHT) and (GPIO.input(6) == 0):
            if self.dianji_state != 'left':
                self.dianji_action(1, 'brake')
                time.sleep(0.2)
                self.dianji_action(1, 'left')

        if (pin == self.P_IN_MID) and (GPIO.input(13) == 0):
            if self.dianji_state != 'brake':
                self.dianji_action(1, 'brake')
                self.do_classify()


    def init_gpio(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)
        GPIO.setup(self.ENA1, GPIO.OUT, initial=GPIO.LOW)
        self.pwm1=GPIO.PWM(self.ENA1, 200)
        self.pwm1.start(40)

        #GPIO.setup(self.IN3, GPIO.OUT)
        #GPIO.setup(self.IN4, GPIO.OUT)
        #GPIO.setup(self.ENA2, GPIO.OUT, initial=GPIO.LOW)
        #self.pwm2=GPIO.PWM(self.ENA2, 200)
        #self.pwm2.start(40)

        GPIO.setup(self.P_IN_LEFT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.P_IN_MID, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.P_IN_RIGHT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        #GPIO.setup(self.in_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        #GPIO.setup(self.in_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        #GPIO.add_event_detect(self.in_1, GPIO.RISING, callback=self.door_callback, bouncetime=500)
        GPIO.add_event_detect(self.P_IN_LEFT, GPIO.FALLING, callback=self.p_callback, bouncetime=150)
        GPIO.add_event_detect(self.P_IN_MID, GPIO.FALLING, callback=self.p_callback, bouncetime=150)
        GPIO.add_event_detect(self.P_IN_RIGHT, GPIO.FALLING, callback=self.p_callback, bouncetime=150)
        #GPIO.add_event_detect(self.in_1, GPIO.BOTH, callback=self.door_callback, bouncetime=200)
        #GPIO.add_event_detect(self.in_1, GPIO.FALLING, callback=self.door_callback, bouncetime=200)
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

    def dianji_suspended(self, idx):
        if idx == 1:
            GPIO.output(self.IN1, GPIO.HIGH)
            GPIO.output(self.IN2, GPIO.HIGH)
        #else:
        #    GPIO.output(self.IN3, GPIO.HIGH)
        #    GPIO.output(self.IN4, GPIO.HIGH)

    def dianji_brake(self, idx):
        print ('brake')
        if idx == 1:
            GPIO.output(self.IN1, GPIO.LOW)
            GPIO.output(self.IN2, GPIO.LOW)
        #else:
        #    GPIO.output(self.IN3, GPIO.LOW)
        #    GPIO.output(self.IN4, GPIO.LOW)

    def dianji_left(self, idx):
        print ('left')
        time.sleep(0.2)
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        #self.dianji_go_full_speed(1)
        #time.sleep(2)
        #self.dianji_brake(1)
        #self.on_gpio(self.IN1, 2)

    def dianji_right(self, idx):
        print ('right')
        time.sleep(0.2)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        #self.dianji_back_full_speed(1)
        #time.sleep(t_sleep)
        #self.dianji_brake(2)
        #self.on_gpio(self.IN2, 2)

    def dianji_go_full_speed(self, idx):
        if idx == 1:
            GPIO.output(self.IN1, GPIO.HIGH)
            GPIO.output(self.IN2, GPIO.LOW)
            GPIO.output(self.ENA1, GPIO.HIGH)
        #else:
        #    GPIO.output(self.IN3, GPIO.HIGH)
        #    GPIO.output(self.IN4, GPIO.LOW)
        #    GPIO.output(self.ENA2, GPIO.HIGH)

    def dianji_back_full_speed(self, idx):
        if idx == 1:
            GPIO.output(self.IN1, GPIO.LOW)
            GPIO.output(self.IN2, GPIO.HIGH)
            GPIO.output(self.ENA1, GPIO.HIGH)
        #else:
        #    GPIO.output(self.IN3, GPIO.LOW)
        #    GPIO.output(self.IN4, GPIO.HIGH)
        #    GPIO.output(self.ENA2, GPIO.HIGH)

    def dianji_action(self, idx, action):
        self.dianji_state = action
        if action == 'left':
            self.dianji_left(idx)
        elif action == 'right':
            self.dianji_right(idx)
        elif action == 'brake':
            self.dianji_brake(idx)



    def do_classify(self):
        time.sleep(5)
        filename = '/tmp/picture.jpg'
        self.pic_cap(0, filename)
        img=cv2.imread(filename,1)
        dst=cv2.resize(img,(299,299))
        cv2.imwrite(filename, dst)
        
        try:
            _thread.start_new_thread(self.query_srv, (filename,))
        except:
            print ("Error: unable to start thread")
            self.do_classify()


    def do_action(self, res):
        print ('res='+res)
        if res != 'ERROR':
            self.start_report_result(res+'-picture.jpg')
            self.store_img('/tmp/picture.jpg', res)
            #if res == 'glass' or res == 'metal':
            if res == 'none':
                return
            elif res in self.trash:
                self.dianji_action(1, 'left')
            else:
                self.dianji_action(1, 'right')
        else:
            self.do_classify()
    
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
            self.do_classify()
            return 'ERROR'

        result = res_array[0].split(' ')
        if len(result) < 1:
            self.do_classify()
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
