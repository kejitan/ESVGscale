# Testing.md

1. We are ready to Test the Query based Image Retrieval application. Run
* $ sudo systemctl start elasticsearch.service 
* $ conda activate PSP15
* $ -- cd ~/InstallDir/ESVGscale
Run
* $ python VG_ADE_600.py -  or
* $ python VG_ADE_600_score.py - from a terminal in the ESVGscale directory. 
* Both these scripts provide identical implementatio of TEXT based query, but they provide different implementation for IMAGE based query.

2. On the browser type "localhost:8050". 

* TEXT QUERY BASED IMAGE RETRIEVAL

1. For Text Query, we enter comma separated list of objects we wish to see in the images that the system retrieves, in the top Input box, e.g. man,tiger 
The system will search the Visual Genome dataset using ElasticSearch and present up to 4 qualifying images. 

2. After entering the comma separated list, press FETCH IMAGES button and wait for the images to appear. 

3. After this you can present the system with another query. 

4. Please press Refresh button on the browser to clear images on the screen. 
 
Sample session is recorded and can be viewed at the following link:


* IMAGE QUERY BASED IMAGE RETRIEVAL

1. We continue to Test with the Image based query application. 

Run
$ python VG_ADE_600.py - for matching images based on 7 common classes or
$ python VG_ADE_600_score.py - for matching images based on a novel similarity measure that takes in to account sratio of pixels in the classes of the sampled image and candidate images from a terminal in the ESVGscale directory.

2. For Image based search, we need to supply the application with a sample image. This can be done by selecting a sample jpg file (from your local computer) or dragging it on the Drag and Drop of Select Files component. Once the image is loaded, press DISPLAY SIMILAR IMAGES button. 

3. After about 10-20 seconds depending on teh server configuration, you will see up to 4 images that have similarity to the sample image supplied earlier. 

4. Please press Refresh button on the browser to clear images on the screen. 

5. VG_ADE_600.py uses 108077 + 22000 images from Visual Genome and ADE20K datasets respectively, and have been annotated into 150 classes and stored in teh ElasticSearch index. The sample image is also segmented and annotated into 150 classes (PSPindexClass.csv file). For similarity we match top 7 classes from the sample images with those in the ElasticSearcj index. A randon set of 4 matching images is presented to the user.  

6. VG_ADE_600_score.py uses 22000 images from ADE20K image dataset and has been annotated into classname as well as pixel sizes for each class. The script implements a novel similarity score computation.  If the number of pixels in a class for sample image and candidate image are similar, the class contributes high similarity score to the overall similarity score ofthe image. On the other hand if the number of pixels in teh sample image and candidate image (for class under consideration) is very different then it ccontributes low to the overall score even though the class is present in both the sample image and candiate image. The 108077 images need to be annotated for Classname and ClassVal (pixel size) and added to the Elastic Serach database before thye can be searched using this new similarity measure. Please ferer to the attached paper for mode details. 

Sample session is recorded and can be viewed at the following link:

https://drive.google.com/file/d/1em0lD1sEK7S2Z_OqTfgiKjEbo39gGG7r/view?usp=sharing


