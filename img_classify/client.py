import socket
import os
import time
import cv2
#import pygame
#import pygame.camera
#from pygame.locals import *

#cap = cv2.VideoCapture(0)

def camera_init():
    pygame.init()
    pygame.camera.init()
    camera = pygame.camera.Camera("/dev/video0", (640,480))
    camera.start()
    return camera

def camera_cap(camera, filename):
    image = camera.get_image()
    pygame.image.save(image, filename)

def camera_unint(camera):
    camera.stop()

#g_camera = camera_init()

def pic_cap(filename):
    cmd = 'fswebcam -r 640x480 --no-banner %s'%(filename)
    os.system(cmd)


BUFSIZE = 1024
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip_port = ('127.0.0.1', 9999)

while True:
    file_name = '/tmp/cap' + time.strftime("_%Y%m%d%H%M%S", time.localtime()) + '.jpg'
    pic_cap(file_name)
    #camera_cap(g_camera, file_name)
    '''
    ret, frame = cap.read()
    if not ret:
        continue

    cv2.imwrite(file_name, frame)
    '''

    client.sendto(file_name.encode('utf-8'), ip_port)
    data, server_addr = client.recvfrom(BUFSIZE)
    res = data.decode()
    print('recvfrom ', server_addr, ': ', res, '\n')

    image = cv2.imread(file_name)
    res_array = res.split('\n')
    for i in range(3):
        cv2.putText(image, res_array[i], (50, 50+50*i), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
    cv2.imshow("Output", image)

    key = cv2.waitKey(0)
    cv2.destroyAllWindows()
    if key & 0x00ff == ord('q'):
        break

#camera_unint(g_camera)
#cap.release()
client.close()
