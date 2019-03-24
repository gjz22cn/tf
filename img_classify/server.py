# coding: utf-8
import tensorflow as tf
import os
import numpy as np
import re
import gc

import socket
BUFSIZE = 1024
ip_port = ('127.0.0.1', 9999)
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(ip_port)

result_str = ''

lines = tf.gfile.GFile('./data/output/output_labels.txt').readlines()
uid_to_human = {}
for uid, line in enumerate(lines):
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

    while True:
        data, client_addr = server.recvfrom(BUFSIZE)
        jpg_file = data.decode()
        print('server recv:', jpg_file)

        image_data = tf.gfile.FastGFile(jpg_file, 'rb').read()
        predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})
        predictions = np.squeeze(predictions)

        top_k = predictions.argsort()[::-1]
        print(top_k)
        #result_str = jpg_file
        result_str = ''
        for node_id in top_k:
            human_string = id_to_string(node_id)
            score = predictions[node_id]
            r_i = '%s (score = %.5f)' % (human_string, score)
            print(r_i)
            if result_str == '':
                result_str = r_i
            else:
                result_str = result_str + '\n' + r_i

        server.sendto(result_str.encode(), client_addr)
        del image_data
        gc.collect()

    server.close()
