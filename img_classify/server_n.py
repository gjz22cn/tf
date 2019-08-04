# Copyright 2018 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""label_image for tflite."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import numpy as np
import datetime

from PIL import Image

from tensorflow.lite.python.interpreter import Interpreter

import socket
BUFSIZE = 1024
ip_port = ('127.0.0.1', 9999)
model_file='/home/pi/code/tf/img_classify/data/mnet1/mnet1.tflite'
label_file='/home/pi/code/tf/img_classify/data/mnet1/labels.txt'

def load_labels(filename):
  with open(filename, 'r') as f:
    return [line.strip() for line in f.readlines()]


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--input_mean', default=127.5, help='input_mean')
  parser.add_argument(
      '--input_std', default=127.5, help='input standard deviation')
  args = parser.parse_args()

  server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  server.bind(ip_port)

  interpreter = Interpreter(model_path=model_file)
  interpreter.allocate_tensors()

  input_details = interpreter.get_input_details()
  output_details = interpreter.get_output_details()

  # check the type of the input tensor
  floating_model = input_details[0]['dtype'] == np.float32

  # NxHxWxC, H:1, W:2
  height = input_details[0]['shape'][1]
  width = input_details[0]['shape'][2]

  while True:
      data, client_addr = server.recvfrom(BUFSIZE)
      jpg_file = data.decode()
      img = Image.open(jpg_file).resize((width, height))

      # add N dim
      input_data = np.expand_dims(img, axis=0)

      if floating_model:
        input_data = (np.float32(input_data) - args.input_mean) / args.input_std

      interpreter.set_tensor(input_details[0]['index'], input_data)

      t1 = datetime.datetime.now()
      interpreter.invoke()

      output_data = interpreter.get_tensor(output_details[0]['index'])
      results = np.squeeze(output_data)
      t2 = datetime.datetime.now()
      k = t2 - t1
      print (k.total_seconds())

      top_k = results.argsort()[-5:][::-1]
      labels = load_labels(label_file)
      result_str = ''
      for i in top_k:
        if floating_model:
          print('{:08.6f}: {}'.format(float(results[i]), labels[i]))
        else:
          print('{:08.6f}: {}'.format(float(results[i] / 255.0), labels[i]))
        
        if result_str == '':
          result_str = labels[i]
        else:
          result_str = result_str + '\n' + labels[i]

      server.sendto(result_str.encode(), client_addr)
