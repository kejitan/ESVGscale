import os
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID" 
os.environ["CUDA_VISIBLE_DEVICES"] = ""
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
    app.layout = serve_layout([])

def query_imagesi(classnum_list, upfilename): #Disabled --
    print("In query_imagesi")
    hit1 = set()
    image_set = set()
    print("11. classnum_list =", classnum_list)
    
    QI = Q('match_all')
    s1 = Search(index='vgnum')
    classn = 1
    for class_num in classnum_list:
        if classn > 6 :		#can make this 7-- 
            break
        classn = classn + 1
        print("class_num= ",class_num)
        QI = QI & Q('bool', must=[Q("match", classnum=class_num)])

    s1 = s1.query(QI).using(client)
    response = s1.execute()
    #print(response)
    for hit in s1.scan() :
        #print("33 ", hit.imgfile)
        image_set.add(hit.imgfile)
    display_image_set(image_set, upfilename)


    
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

    display_image_set(image_set, None)


def display_image_set(image_set, upfilename) :

    #print("image_set = {0}".format(image_set))
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
    if im == 0 :
        images_div.append(no_images_msg())
        app.layout = serve_layout(images_div)
        print("Please hit refresh...")
        return
    if upfilename != None :
        encoded_image = base64.b64encode(open(upfilename, 'rb').read())  
        images_div.append(
            html.Div([
                html.H5(upfilename),
                html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode())),
                html.Hr(),  # horizontal line        
            ]) )

    print("Please hit refresh...")
    app.layout = serve_layout(images_div)

    return

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



def serve_layout(img_div):
    return html.Div(    
		children=[
		    dcc.Interval(id="interval-updating-images", interval=1000, n_intervals=0),
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
		                        html.Div(dcc.Input(id="Objects-in-image", value="man",type='text')),                       
		                        html.Button( children="Fetch Images", id="fetch-images",  n_clicks=0),
		                        html.Div(id='outputf', children="fimage"),
		                        html.Button( children="Clear Images", id="clear-images", n_clicks=0),
								html.Div(id='display-clear-button', children="dimage"),
		                        html.Div(img_div, id='disp-images' ),

		                    ]),
                            '''
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
 
                                # Allow multiple files to be uploaded
                                multiple=False
                                ),
                                html.Div(id='output-image-upload'),
                                html.Div(id='output-similar-images' ),
		                        html.Button( children="Display Similar Images", id="display-similar-images",  n_clicks=0),
                                #html.Div(id='display-similar-images' ),
                                html.Div(id='output-images' ),
                                '''


		                ],
		            ),
		        ],
		    ),
		]
)


app.layout = serve_layout([])

@app.callback(Output('outputf', 'children'),
             [Input('fetch-images', 'n_clicks')],
              [State('Objects-in-image', 'value')])
def fetch_images(n_clicks, value):
    if n_clicks > 0:
        n_clicks = 0
        #print("value=", value)
        object_list = value.split(',')
        print("22. object_list=",object_list)
        query_imageso(object_list)


@app.callback(Output('display-clear-button', 'children'),
             [Input('clear-images', 'n_clicks')] )
def clear_images(n_clicks):
    if n_clicks > 0:
        n_clicks = 0
        #images_div = []
        app.layout = serve_layout([])
        print("In clear_images")

'''
@app.callback(Output('output-image-upload', 'children'),
              [Input('upload-image', 'contents')],
              [State('upload-image', 'filename')])
def select_sample_image(contents, file_name):
    if contents is not None:
        print("222 " + file_name)
        #upfilename = file_name
        #upfile_contents = contents
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
    cv2.imwrite("/home/ubuntu/tmp/"+file+".png", resized)
    print("111"+ "/home/ubuntu/tmp/"+file+".png")
#    cv2.imwrite("/var/tmp/"+file+".png", resized)
#    print("111"+ "/var/tmp/"+file+".png")
    upfile_contents = contents
    #upfilename = "/var/tmp/"+file+".png"
    return html.Div([
        html.H5(filename),
        html.Img(src=contents),
        html.Hr()  # horizontal line        
    ])

@app.callback(Output('output-similar-images', 'children'),
             [Input('display-similar-images', 'n_clicks')],
             #[Input('upload-image', 'contents')],
             [State('upload-image', 'filename')] )
def display_similar_images( n_clicks, filename ): # image in jpg or mpg format
    if n_clicks > 0:
        print("3333 display_similar_images: filename ", filename)
        print("click_received")
        n_clicks = 0
        if (filename == None) :
            return
        fname = os.path.basename(filename)
        file, ext = os.path.splitext(fname)

        #classnum_list = find_classes("/var/tmp/"+file+".png", "/var/tmp/"+file+"seg.png")
        classnum_list = find_classes("/home/ubuntu/tmp/"+file+".png", "/home/ubuntu/tmp/"+file+"seg.png")
        print("4444 classnum_list" )
        print(classnum_list)
        #encoded_image = base64.b64encode(open("/var/tmp/"+file+".png", 'rb').read())	
        #show_image(encoded_image, filename)
        #query_imagesi(classnum_list, "/var/tmp/"+file+".png" )
        query_imagesi(classnum_list, "/home/ubuntu/tmp/"+file+".png" )

def show_image(contents, filename):
    try:
        if ( ('jpg' in filename) or ('JPG' in filename) or ('png' in filename) or ('PNG' in filename) ):
        # Assume that the user uploaded an image file
            dummy = True;
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.Img(src='data:image/png;base64,{}'.format(contents)),
        html.Hr(),  # horizontal line        
    ])
'''

if __name__ == "__main__":
    #serve(server, host='0.0.0.0', port=8050)
    serve(server, host='18.221.55.65', port=8050)
#    app.run_server(
#        port=8050,
#        host='127.0.0.1',
#        debug=True
#    )
'''
    app.run_server(
        port=8080,
        #port=8050,
        host='103.255.38.15'
        #host='0.0.0.0'
    )
'''
#    main()
#    app.run_server(debug=True, port=8053)
