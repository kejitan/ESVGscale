#!/usr/bin/env python
import os

from PIL import Image 
import glob, os
from tqdm import tqdm
import six
import pandas as pd
import keras_segmentation
from keras_segmentation.data_utils.data_loader import get_image_array, get_segmentation_array

import numpy as np

import re
import json
from pandas.io.json import json_normalize
import time

from keras_segmentation.models.model_utils import transfer_weights
from keras_segmentation.pretrained import pspnet_50_ADE_20K
from keras_segmentation.models.pspnet import pspnet_50
from keras_segmentation.predict import predict
from Kseg2annANN import seg2ann

def find_classes(inp, out_fname):

    pr = predict(model=pspnet_50_ADE_20K(), inp=inp, out_fname=out_fname)

    CDict = seg2ann(seg_file=out_fname)

    k = 0
    classnum_list = []
    classval_list = []
    for key in sorted(CDict.keys(), reverse=True) :
        k = k +1
        if k > 10 :
            break
        if key != 0 :
            classnum_list.append(CDict[key][0])
            classval_list.append(CDict[key][1])
            print(CDict[key])

    print(classnum_list)
    print(classval_list)
    return classnum_list, classval_list




