#README.md

This repository demostrates how to scale up the images and annotations directory together with Elastic Search indexes. This exercise is continuation of exercise done in repository https://github.com/kejitan/ESpspVG1, however we present it as an independent exercise. Reader may skip steps already done before. 

1. Install ElasticSearch7.4.2 or above

2. sudo apt-get install -y libsm6 libxext6 libxrender-dev
   #sudo apt-get install gunicorn

3. 
```
git clone https://github.com/kejitan/ESVGscale
cd ESVGscale
--Create conda virtual environment PSP by running:
conda create -n PSP python=3.6
conda activate PSP
pip install -r requirements.txt 
pip install waitress
```

4. In the earlier ESpspVG1 repository we have created assets directory containing 108077 images from Visual Genome dataset from Stanford. The exercise in this repository will add 22000 new images from ADE20K dataset from MIT CSAIL, first by creating the images, and annotations in this repository. Next we will create new Elastic Search entries and add to the existing index vgnum. 

5. We will be downloading instance segmentation images, images.tar from http://sceneparsing.csail.mit.edu/ into ESVBscale directory. 

5. Extract from the tar file images.tar. There will be two subdirectories training and validation. Create adkImages folder in ESVGscale directory and copy or move images from training and validation directories to adkImages folder. 

6. The images are in jpg format. Resize the images to 473x473 format by running the following in ESVGscale directory 
```
mkdir -p assetsADK
python makeADKdata.py
```
The image segmentation and annotations step requires that the images be in 473x473 PNG format). 

7. The images in assetsADK directory need to be segmented and annotated. This is done as follows. First Convert the JPG imges into PNG format and copy to pngADK directory. Next segment thhe images in png format and copy the segmented images to segADK directory.Next annotate the segmentated images and copt then to annADK directory
mkdir -p pngADK
mkdir -p segADK
mkdir -p annADK
python jpg2png.py
python png2seg.py  # This step took me about 3 hours with GPU
python seg2ann.py  # This step took me about 10 hours GPU is not used

-- I have a version of seg2ann.py program that shortens the time by using Multiprocessing in Multi core processors. It will need to be tweaked a little bit. 

8. Next we need to create Elastic Search search and add to the existing ES index vgnum. This is done by Running
python ESANNadk.py
This will take a few minutes.

Now we can create a link to the assets directory in the earlier ESpspVG1 directory. Make sure you continue to be in ESVGscale directory
```
ln -s ../ESpspVG1/assets assets
cp assetsADK/* assets  # instead of cp you can use mv to save space. or ypu can delete assetsADK directory after copy to assets directory. To operate the program, we will not need annADK, pngADK, segADK directories either. You can delete them when your experimentation is oover. 

Note that we cannot add new annotations to idx0 and idx1 indexes since they are generated in from annotation files created by manually in Visual Genome format.

We need to copy or move JPG images in assetsADK directory to assets directory.  

9. You can verify that new entris have been added to index 'vgnum' by exploring Kibana Create Index in Management Tool and then browsing in the Discover tool.

* IMAGE QUERY BASED IMAGE RETRIEVAL

10. Now we are ready to run the Image based query application. Run
python VGdashPSP.py 
from a terminal in the ESVGscale directory.

11. It will inform that the application will interact on localhost:8050 port. Please open this port in a web browser. Click refresh button in the web browser. You will see five boxes. Top Input box and FETCHG IMAGES and CLEAR IMAGES buttons are for Query bases image search.

12. Now we need to supply the application with a sample image. This can be done by selecting a sample jpg file or dragging it on the Drag and Drop of Select Files component. Once the image is loaded, press DISPLAY SIMILAR IMAGES button. 

12. After a few seconds, you will see some informational messages in the terminal and a prompt 'Please hit refresh'. At this point the images are ready to be displayed on the web browser. We need to press Refresh button on the web browser. You will see up to 4 images that have similarity to the sample image supplied earlier. 

13. We can repeat the procedure to assess the quality of similarity of the images. This is at present not very good, since the number classes (type of objects in the images) is 150 (small). These classes can be examined in the file PSPindexClass.csv. We have 108077 + 22000 images and each image has up to 11 classes identified in the images. For similarity we match top 6 classes from the sample images. Still there are lots of matches and 4 images are selected randomly. We could require to match 7 objects in the images so as to find better matches. Another change that we could implement in the future versions is that onsider objects for comparison only if they meeet some minimum number of pixels criteria(say 2000). Under the Elactic Search regime it will be very difficult if not impossible to consider top N objects from the images in the dataset. Right now we have not impemented a similarity score because, the objects are labeled in the images irrespective of their size or prominence. Such information is hard to get by in the automatic annotation process using semantic segmentation  as we are using. 


* TEXT QUERY BASED IMAGE RETRIEVAL

-- Nothing new has been added to this functionality from ESpspVG1 repository. The section is and will not work if ESpspsVG1 has not been installed. 

14. We enter comma separated list of objects we wish to see in the images that the system retrieves, in the top Input box, e.g. man,tiger 
The system will search the Visual Genome dataset using ElasticSearch and present up to 4 qualifying images. 

15. After entering the comma separated list, press FETCH IMAGES button and wait for informationl message in the terminal to Hit refresh button. After hitting the Refresh button on the browser, the browser display will be updates. 

16. After this you can present the system with another query. 

* NOTE
This is a scaled up version of the project. Jupyter notebooks have not been provided as the performance of the system is not good with small number of images in the dataset. 



