import os

from PIL import Image
import numpy as np

import keras
from keras import Input, Model
from keras.layers import Dense, GlobalAveragePooling2D, Flatten, Dropout, BatchNormalization
from keras.applications import ResNet50

import tensorflow as tf

inputs = Input((224, 224, 3))
base_model = ResNet50(include_top=False, weights=None, input_tensor=inputs)

x = base_model.output

x = Dropout(0.2)(x)

x = Flatten()(x)

x = Dense(1024, activation='relu')(x)

outputs = Dense(5, activation='softmax')(x)

TCN = Model(inputs, outputs)

TCN.load_weights(os.path.join(os.path.dirname(__file__), '..', 'model', '1.h5'))


def f(f):
    with graph.as_default():
        a = Image.open(f).convert('RGB').resize([224, 224])
        a = np.array(a)[None]
        a = keras.applications.resnet50.preprocess_input(a)
        pred = TCN.predict(a)
        return pred, pred.argmax()


##fileNames = os.listdir('./my_test/')
##for f_name in fileNames:
##    pred, max_arg = f('./my_test/'+f_name)
##    conf = pred.max()
##    if conf < 0.85:
##        print('置信度低, 返回人工')
##    else:
##        print(max_arg, conf)
##

global graph
graph = tf.get_default_graph()
