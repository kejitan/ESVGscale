# README.md

* The application was deployed on AWS at 34.194.42.220:8050 till till about 24th March 2020 and was taken out after complimentaryt AWS Educate credit was exhausted. 

* P paper has been written and submitted to Computer Vision DevCom 2020 conference and is available in the repository with name TIQS-Final1.pdf

* A recording of a user session is made availavle at
https://drive.google.com/file/d/1em0lD1sEK7S2Z_OqTfgiKjEbo39gGG7r/view?usp=sharing

* This is a multi user application. Input/outputs from multiple users do not interfer.

* If the application is installed on a local computer with GPU, the response is faster, about 5 seconds. Response for text query based search is fast (less than 2 seconds) as it does not need Tensorflow/GPU.

* Install the application on AWS as described in AWSdeployment.md document.
or
* Install the application on local computer as described in Installation.md document.

* For completion, scaling of the system is described in Installation1.md document.

* The repository contains sample100.zip archive containing sample images for 'Display Similar Images' part of the application. You can install them on your computer that runs web browser, or you may use your own images.

* Testing and logging are described in Testing.md document


* IMAGE QUERY BASED IMAGE RETRIEVAL

1. Now we are ready to run the Image based query application. Run
$ conda activate PSP15
$ -- cd ~/InstallDir/ESVGscale
$ python VG_ADE_600.py or
python VG_ADE_600_score.py for a script with implementation of a novel similarity score between the sample image and candidate images, from a terminal in the ESVGscale directory.

2. It will inform that the application will interact on localhost:8050 port. Please visit this link in a web browser. Click refresh button in the web browser. You will see four boxes. Top Input box and FETCH IMAGES button are for Query based image search.

3. For Image based search, we need to supply the application with a sample image. This can be done by selecting a sample jpg file (from your local computer) or dragging it on the Drag and Drop of Select Files component. Once the image is loaded, press DISPLAY SIMILAR IMAGES button. 

4. We see up to 4 images that have similarity to the sample image supplied earlier. 

5. Please press Refresh button on the browser to clear images on the screen. 

6. VG_ADE_600.py uses 108077 + 22000 images from Visual Genome and ADE20K datasets respectively, and have been annotated into 150 classes and stored in teh ElasticSearch index. The sample image is also segmented and annotated into 150 classes (PSPindexClass.csv file). For similarity we match top 7 classes from the sample images with those in the ElasticSearcj index. A randon set of 4 matching images is presented to the user.  

7. VG_ADE_600_score.py uses 22000 images from ADE20K image dataset and has been annotated into classname as well as pixel sizes for each class. The script implements a novel similarity score computation.  If the number of pixels in a class for sample image and candidate image are similar, the class contributes high similarity score to the overall similarity score ofthe image. On the other hand if the number of pixels in teh sample image and candidate image (for class under consideration) is very different then it ccontributes low to the overall score even though the class is present in both the sample image and candiate image. The 108077 images need to be annotated for Classname and ClassVal (pixel size) and added to the Elastic Serach database before thye can be searched using this new similarity measure. Please ferer to the attached paper for mode details. 


* TEXT QUERY BASED IMAGE RETRIEVAL

1. We enter comma separated list of objects we wish to see in the images that the system retrieves, in the top Input box, e.g. man,tiger 
The system will search the Visual Genome dataset using ElasticSearch and present up to 4 qualifying images. 

2. After entering the comma separated list, press FETCH IMAGES button and wait for the images to appear. 

3. After this you can present the system with another query. 

4. Please press Refresh button on the browser to clear images on the screen. 

# Acknowledgements

The author acknowledges use of Divam Gupta’s keras-semantic-segmentation library, Stanford University’s Visual Genome dataset, MIT CSAIL’s ADE20K dataset, pspnet50 model pretrained on ADE20K dataset. The application used Elastic Search, Kibana, Plotly Dash, AWS Educational Credits for hosting the application for a few days. Google Search and Stack Overflow among others were very helpful in resolving myriads of problems encountered while implementing the system. I would like to thank my mentor Krishna Kumar Tiwari for his guidance in this Capstone project.  

# References
* https://visualgenome.org/api/v0/api_home.html -- Data download directory
* https://groups.csail.mit.edu/vision/datasets/ADE20K/ -- Data download directory
* https://github.com/divamgupta/image-segmentation-keras Github repository
* https://divamgupta.com/image-segmentation/2019/06/06/deep-learning-semantic-segmentation-keras.html Blog


# License
* This work uses Visual Genome Dataset, ADE20K Dataset, Divam Gupta's Keras Segmentation library under their licenses. Author's contributions are licensed under a Creative Commons Attribution 4.0 International License. 
