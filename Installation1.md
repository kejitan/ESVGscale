#Installation1.md

This repository demostrates how to scale up the images and annotations directory together with Elastic Search indexes. This exercise is continuation of exercise done in repository https://github.com/kejitan/ESpspVG1, however we present it as an independent exercise. Reader may skip steps already done before. 

1. Install ElasticSearch7.4.2 or above

2.$ sudo apt-get install -y libsm6 libxext6 libxrender-dev
 
3. 
```
$git clone https://github.com/kejitan/ESVGscale
$cd ESVGscale
--Create conda virtual environment PSP by running:
$conda create -n PSP15 python=3.6
$conda activate PSP15
$pip install -r requirements.txt 
```

4. In the earlier ESpspVG1 repository we have created assets directory containing 108077 images from Visual Genome dataset from Stanford. (These steps are reproduced at the end of this doc).  The exercise in this repository will add 22000 new images from ADE20K dataset from MIT CSAIL, first by creating the images, and annotations in this repository. Next we will create new Elastic Search entries and add to the existing index vgnum. 

5. We will be downloading instance segmentation images, images.tar from http://sceneparsing.csail.mit.edu/ into ESVGscale directory. 

5. Extract from the tar file images.tar. There will be two subdirectories training and validation. Create adkImages folder in ESVGscale directory and copy or move images from training and validation directories to adkImages folder. 

6. The images are in jpg format. Resize the images to 473x473 format by running the following in ESVGscale directory 
```
$ mkdir -p assetsADK
$ python makeADKdata.py
```
The image segmentation and annotations step requires that the images be in 473x473 PNG format). 

7. The images in assetsADK directory need to be segmented and annotated. This is done as follows. First Convert the JPG imges into PNG format and copy to pngADK directory. Next segment thhe images in png format and copy the segmented images to segADK directory.Next annotate the segmentated images and copt then to annADK directory
$ mkdir -p pngADK
$ mkdir -p segADK
$ mkdir -p annADK
$ python jpg2png.py
$ python png2seg.py  # This step took me about 3 hours with GPU
$ python seg2ann.py  # This step took me about 10 hours GPU is not used

-- I have a version of seg2ann.py programseg2annProcess .py that shortens the time by using Multiprocessing in Multi core processors. It will need to be tweaked a little bit depending on the configuration of the local computer. 

8. Next we need to create Elastic Search index entries and add to the existing ES index vgnum. This is done by running:
$ python ESANNadk.py
This will take a few minutes.

Now we can create a link to the assets directory in the earlier ESpspVG1 directory. Make sure you continue to be in ESVGscale directory
```
ln -s ../ESpspVG1/assets assets
cp assetsADK/* assets  # instead of cp you can use mv to save space. or you can delete assetsADK directory after copy to assets directory. To operate the program, we will not need annADK, pngADK, segADK directories either. You can delete them when your experimentation is over. 

Note that we cannot add new annotations to idx0 and idx1 indexes since they are generated in from annotation files created by manually in Visual Genome format.

We need to copy or move JPG images in assetsADK directory to assets directory.  
$ cp assetsADK/* assets/

9. You can verify that new entris have been added to index 'vgnum' by exploring Kibana Create Index in Management Tool and then browsing in the Discover tool.


