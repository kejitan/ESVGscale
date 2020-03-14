import os
import gc
import json
import requests
from elasticsearch import Elasticsearch, helpers
from elasticsearch.helpers import bulk
from elasticsearch_dsl.query import Bool, MultiMatch
from elasticsearch_dsl.search import Search, MultiSearch
from elasticsearch_dsl import Mapping, Keyword, Nested, Text
from elasticsearch_dsl import Index, analyzer, tokenizer
from elasticsearch_dsl import Q
import glob
import time

from  urllib import parse
from os.path import splitext, basename


res = requests.get('http://localhost:9200')
print (res.content)
es = Elasticsearch([{'host': 'localhost', 'port': '9200'}])
client = Elasticsearch()

fimgin = open('./image_data.json', "r")
img_list = json.load(fimgin)

m = Mapping()
m.field('image_id', 'long')

idx1 = Index('idx1')
idx1.mapping(m)

for CDict in img_list :
    image_id = CDict["image_id"] 
    url = CDict["url"]
    imagefile = os.path.basename(url)
    CDict['imagefile'] = imagefile
    print("Imagefile= ", imagefile)
    
    img_str = json.dumps(CDict)
    es.index(index='idx1', body=json.loads(img_str))


def get_imgfile(img_id) :
    s = Search(index='idx1').query('match', image_id=img_id)
    s = s.using(client)
    s.execute()
    for hit in s.scan() :
        imgfile = hit.imagefile
        return imgfile


time.sleep(10)

fimagesin = open('./objects.json', "r")
images_list = json.load(fimagesin)

m1 = Mapping()
m1.field("names", "text")
idxO = Index('idx0')
idxO.mapping(m1)

for CDict in images_list :
    image_id = CDict["image_id"] 
    imgfile = get_imgfile(image_id)
    Objects = CDict["objects"]
    objs_list_str = json.dumps(Objects) 
    objs_list = json.loads(objs_list_str) # will replace curly parenthesesinto square brackets

    CDictES = {} # Dictionary from which Elastic search will be populated
    CDictES['image_id'] = image_id 
    CDictES['imgfile'] = imgfile 
    print("11 imgfile=", imgfile)
  
    synsets_list = [] 
    object_id_list = []
    names_list = []
    w_list = []
    h_list = []
    x_list = []
    y_list = []

    for CObject in objs_list:

        obj_list_str = json.dumps(CObject) 
        obj_list = json.loads(obj_list_str) # will replace curly 
               
        synsets_list.extend(CObject["synsets"])  
        object_id_list.append(CObject["object_id"])
        names_list.extend(CObject["names"]) 

        w_list.append(CObject["w"])
        h_list.append(CObject["h"])
        x_list.append(CObject["x"])
        y_list.append(CObject["y"])
     
    CDictES["synsets"] = synsets_list
    CDictES["object_id"] = object_id_list
    CDictES["names"] = names_list
    CDictES["w_list"] = w_list
    CDictES["h_list"] = h_list
    CDictES["x_list"] = x_list
    CDictES["y_list"] = y_list
       
    objESstr = json.dumps(CDictES) 
    es.index(index="idx0",  body=json.loads(objESstr))


    
