# coding: utf-8
import tensorflow as tf
import os
import numpy as np
import re
# from PIL import Image
import matplotlib.pyplot as plt
import time

import socket
BUFSIZE = 1024
ip_port = ('127.0.0.1', 9999)
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # udp协议
server.bind(ip_port)

result_str = ''

lines = tf.gfile.GFile('./data/output/output_labels.txt').readlines()
uid_to_human = {}
# 一行一行读取数据
for uid, line in enumerate(lines):
    # 去掉换行符
    line = line.strip('\n')
    uid_to_human[uid] = line


def id_to_string(node_id):
    if node_id not in uid_to_human:
        return ''
    return uid_to_human[node_id]


with tf.gfile.FastGFile('./data/output/output_graph.pb', 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    tf.import_graph_def(graph_def, name='')
with tf.Session() as sess:
    softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
    '''
    for root, dirs, files in os.walk('./data/pre_image/'):
        for file in files:
            # 载入图片
            if not file.endswith('.jpg') or file.startswith('.'):
                continue
            image_data = tf.gfile.FastGFile(os.path.join(root, file), 'rb').read()
            predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})  # 图片格式是jpg格式
            predictions = np.squeeze(predictions)  # 把结果转为1维数据

            # 打印图片路径及名称
            image_path = os.path.join(root, file)
            print(image_path)
            # 显示图片
            #             img=Image.open(image_path)
            #             plt.imshow(img)
            #             plt.axis('off')
            #             plt.show()

            # 排序
            top_k = predictions.argsort()[::-1]
            print(top_k)
            for node_id in top_k:
                # 获取分类名称
                human_string = id_to_string(node_id)
                # 获取该分类的置信度
                score = predictions[node_id]
                print('%s (score = %.5f)' % (human_string, score))
            print()
            time.sleep(5)
    '''

    while True:
        data, client_addr = server.recvfrom(BUFSIZE)
        jpg_file = data.decode()
        print('server收到的数据', jpg_file)

        image_data = tf.gfile.FastGFile(jpg_file, 'rb').read()
        predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})  # 图片格式是jpg格式
        predictions = np.squeeze(predictions)  # 把结果转为1维数据

        print(jpg_file)
        result_str = jpg_file

        # 排序
        top_k = predictions.argsort()[::-1]
        print(top_k)
        for node_id in top_k:
            # 获取分类名称
            human_string = id_to_string(node_id)
            # 获取该分类的置信度
            score = predictions[node_id]
            r_i = '%s (score = %.5f)' % (human_string, score)
            print(r_i)
            result_str = result_str + '\n' + r_i

        server.sendto(result_str.encode(), client_addr)

    server.close()
