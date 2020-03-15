# README.md

* The application is deployed on AWs and can be accessed at
  34.194.42.220:8050
This should be accessible till about 23rd March 2020

* This is a single user application. If multiple users use this application simultaneously, the user input/outputs will interfer.

* We have not configured GPU on our instance on AWS, therefore 'Display Similar Images' part of the application takes a little longer (about 25 seconds). Please wait for this period after clicking 'Display Similar Images' button before pressing refresh button. If the application is installed on a local computer with GPU, the response is faster, about 10 seconds. Response for text query based search is fast (a couple of seconds) as it does not need Tensorflow/GPU.

* Install the application on AWS as described in AWSdeployment.md document.

* Install the application on local computer as described in Installation.md document.

* For completion, scaling of the system is described in Installation1.md document.


* IMAGE QUERY BASED IMAGE RETRIEVAL

1. Now we are ready to run the Image based query application. Run
$ conda activate PSP15
$ -- cd ~/InstallDir/ESVGscale
$ python VG_ADE_600.py 
from a terminal in the ESVGscale directory.

2. It will inform that the application will interact on localhost:8050 port. Please visit this link in a web browser. Click refresh button in the web browser. You will see five boxes. Top Input box and FETCH IMAGES and CLEAR IMAGES buttons are for Query based image search.

3. For imaged based search, we need to supply the application with a sample image. This can be done by selecting a sample jpg file (from your local computer) or dragging it on the Drag and Drop of Select Files component. Once the image is loaded, press DISPLAY SIMILAR IMAGES button. 

4. After a few seconds, you will see some informational messages in the terminal and a prompt 'Please hit refresh'. At this point the images are ready to be displayed on the web browser. We need to press Refresh button on the web browser. You will see up to 4 images that have similarity to the sample image supplied earlier. 

5. We can repeat the procedure to assess the quality of similarity of the images. This is at present not very good, since the number categories (type of objects in the images) is 150 (small). These classes can be examined in the file PSPindexClass.csv file. We have 108077 + 22000 images and each image has up to 11 classes identified in the images. For similarity we match top 6 classes from the sample images. Still there are lots of matches and 4 images are selected randomly. We could require to match 7 objects in the images so as to find better matches. But that may give no matches in some instances. Another change that we could implement in the future versions is  to consider objects for comparison only if they meet some minimum number of pixels criteria(say 2000). Under the Elastic Search regime it will be very difficult if not impossible to consider top N objects from the images in the dataset. Right now we have not impemented a similarity score because, the objects are labeled in the images irrespective of their size or prominence. Such information is hard to get by in the automatic annotation process using semantic segmentation as we are using. 


* TEXT QUERY BASED IMAGE RETRIEVAL

1. We enter comma separated list of objects we wish to see in the images that the system retrieves, in the top Input box, e.g. man,tiger 
The system will search the Visual Genome dataset using ElasticSearch and present up to 4 qualifying images. 

2. After entering the comma separated list, press FETCH IMAGES button and wait for informationl message in the terminal to Hit refresh button. After hitting the Refresh button on the browser, the browser display will be updates. 

3. After this you can present the system with another query. 
 



