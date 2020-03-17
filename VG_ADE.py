import os
from waitress import serve

from textwrap import dedent
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_player as player

import random
import plotly
import plotly.graph_objs as go
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate

import numpy as np
import pandas as pd

import pathlib
import PIL

import gc
import json
import requests
from elasticsearch import Elasticsearch, helpers
from elasticsearch.helpers import bulk
from elasticsearch_dsl.query import Bool, MultiMatch, Q
from elasticsearch_dsl.search import Search, MultiSearch
from elasticsearch_dsl import Mapping, Keyword, Nested, Text
from elasticsearch_dsl import Index, analyzer, tokenizer
import glob
import cv2
from matplotlib import pyplot as plt
from findClassANN import find_classes
from PIL import Image
import base64
import io
import string
#import os


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server
app.config.suppress_callback_exceptions = True

res = requests.get('http://localhost:9200')
print (res.content)
es = Elasticsearch([{'host': 'localhost', 'port': '9200'}])
client = Elasticsearch()

def init_layout(refresh_interval):
    app.layout = serve_layout([], 'man,tiger')

def query_imagesi(classnum_list, upfilename): #Disabled --
    print("In query_imagesi")
    hit1 = set()
    image_set = set()
    print("11. classnum_list =", classnum_list)
    
    QI = Q('match_all')
    s1 = Search(index='vgnum')
    classn = 1
    for class_num in classnum_list:
        if classn > 7 :		#can make this 7-- 
            break
        classn = classn + 1
        print("class_num= ",class_num)
        QI = QI & Q('bool', must=[Q("match", classnum=class_num)])

    s1 = s1.query(QI).using(client)
    response = s1.execute()
    for hit in s1.scan() :
        image_set.add(hit.imgfile)
    return display_image_set(image_set, upfilename, '')


    
def query_imageso(object_list):
    print("In query_imageso")
    hit1 = set()
    image_set = set()
    print("11. object_list =", object_list)
    
    QI = Q('match_all')
    s1 = Search(index='idx0')
    for name in object_list:
        print("name= ",name)
        QI = QI & Q("match", names=name)

    s1 = s1.query(QI).using(client)
    response = s1.execute()
    for hit in s1.scan() :
        image_set.add(hit.imgfile)

    return display_image_set(image_set, None, object_list)


def display_image_set(image_set, upfilename, object_list) :

    objects=''
    for ob in object_list:
        if objects == '':
            objects = ob
        else:
            objects = objects + ',' + ob
    im = 0
    images_div = []
    for image in image_set :
        if im > 3 : 
            break
        file, ext = os.path.splitext(image)
        image = file + '.jpg'
        print("66 image =", image)
        images_div.append(display_image(image))
        im = im + 1

    return images_div

def no_images_msg():
    return html.Div([
            html.P("No images found")
    ])

def display_image(image):
    return html.Div(
        html.A(
            html.Img(
                src = app.get_asset_url(image)#,
				#style={'display':'block'}
           ) )
    )

def serve_layout(img_div, objects):
    return html.Div(    
		children=[
		    html.Div(
		        className="container",
		        children=[
		            html.Div(
		                id="left-side-column",
		                className="twelve columns",
		                children=[
		                    html.Img(
		                        id="logo-mobile", src=app.get_asset_url("dash-logo.png")
		                    ),
		                    html.Label('Objects in Image'),
		                    html.Div([
		                        html.Div(dcc.Input(id="Objects-in-image", value=objects,type='text')),                       
		                        html.Button( children="Fetch Images", id="fetch-images",  n_clicks=0),
		                        html.Div(id='outputf'),
		                        html.Div(img_div),

		                    ]),

                            dcc.Upload(
                                id='upload-image',
                                children=html.Div([
                                    'Drag and Drop or ',
                                     html.A('Select Files')
                                ]),
                                style={
                                    'width': '100%',
                                    'height': '50px',
                                    'lineHeight': '50px',
                                    'borderWidth': '1px',
                                    'borderStyle': 'dashed',
                                    'borderRadius': '5px',
                                    'textAlign': 'center',
                                    'margin': '10px'
                                },
 
                                # Do not allow multiple files to be uploaded
                                multiple=False
                                ),
                                html.Div(id='output-image-upload'),
                                html.Div(id='output-similar-images' ),
		                        html.Button( children="Display Similar Images", id="display-similar-images",  n_clicks=0),

		                ],
		            ),
		        ],
		    ),
		]
)


app.layout = serve_layout([], 'man,tiger')

@app.callback(Output('outputf', 'children'),
             [Input('fetch-images', 'n_clicks')],
              [State('Objects-in-image', 'value')])
def fetch_images(n_clicks, value):
    if n_clicks > 0:
        n_clicks = 0
        object_list = value.split(',')
        print("22. object_list=",object_list)
        #app.layout=wait_layout()
        return query_imageso(object_list)
         

@app.callback(Output('output-image-upload', 'children'),
              [Input('upload-image', 'contents')],
              [State('upload-image', 'filename')])
def select_sample_image(contents, file_name):
    if contents is not None:
        children = [ parse_contents(contents, file_name) ]
        return children


def parse_contents(contents, filename):
    print("file_name = ", filename)
    try:
        fname = os.path.basename(filename)
        file, ext = os.path.splitext(fname)

        if ( ext in ['jpg', 'JPG', 'JPEG', 'png'] ):
        # Assume that the user uploaded an image file
            dummy = True;
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    content_type, content_string = contents.split(',')
    image = base64.b64decode(content_string) #.convert('RGB')
    image = Image.open(io.BytesIO(image))
    rgb_im = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
    resized = cv2.resize(rgb_im, (473,473), interpolation = cv2.INTER_AREA)
    if (cv2.imwrite("/home/kejitan/tmp/"+file+".png", resized) == False) :
        print("Could not create /home/kejitan/tmp/"+file+".png")
        return
    print("111"+ "/home/kejitan/tmp/"+file+".png")
    #if (cv2.imwrite("/home/ubuntu/tmp/"+file+".png", resized) == False) :
    #    print("Could not create /home/kejitan/tmp/"+file+".png")
    #    return
    #print("111"+ "/home/ubuntu/tmp/"+file+".png")
    upfile_contents = contents
    return html.Div([
        html.H5(filename),
        html.Img(src=contents),
        html.Hr()  # horizontal line        
    ])



@app.callback(Output('output-similar-images', 'children'),
             [Input('display-similar-images', 'n_clicks')],
             [State('upload-image', 'filename')] )
def display_similar_images( n_clicks, filename ): # image in jpg or mpg format
    if n_clicks > 0:
        print("33 display_similar_images: filename ", filename)
        print("click_received")
        n_clicks = 0
        if (filename == None) :
            return
        value='fetching_images'

        fname = os.path.basename(filename)
        file, ext = os.path.splitext(fname)

        classnum_list = find_classes("/home/kejitan/tmp/"+file+".png", "/home/kejitan/tmp/"+file+"seg.png")
        #classnum_list = find_classes("/home/ubuntu/tmp/"+file+".png", "/home/ubuntu/tmp/"+file+"seg.png")
        print("44 classnum_list" )
        print(classnum_list)
        #app_layout=wait_layout()

        return query_imagesi(classnum_list, "/home/kejitan/tmp/"+file+".png" )
        #query_imagesi(classnum_list, "/home/ubuntu/tmp/"+file+".png" )


if __name__ == "__main__":
    #serve(server, host='34.194.42.220', port=8050)
    serve(server, host='0.0.0.0', port=8050)
#    main()
#    app.run_server(debug=True, port=8053)
