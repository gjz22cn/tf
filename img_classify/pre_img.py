# coding: utf-8
import tensorflow as tf
import os
import numpy as np
import re
# from PIL import Image
import matplotlib.pyplot as plt

print("entry 1")

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
    for root, dirs, files in os.walk('./data/pre_image/'):
        for file in files:
            # load img
            if not file.endswith('.jpg') or file.startswith('.'):
                continue
            image_data = tf.gfile.FastGFile(os.path.join(root, file), 'rb').read()
            predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})
            predictions = np.squeeze(predictions)

            image_path = os.path.join(root, file)
            print(image_path)

            top_k = predictions.argsort()[::-1]
            print(top_k)
            for node_id in top_k:
                human_string = id_to_string(node_id)
                score = predictions[node_id]
                print('%s (score = %.5f)' % (human_string, score))
            print()
