
# Installation.md

* Installation on a local computer

* This is a single user application. If multiple users use this application simultaneously, the user input/outputs will interfer.

* If the local computer has not been configured with GPU,'Display Similar Images' part of the application takes a little longer (about 25 seconds). Please wait for this period after clicking 'Display Similar Images' button before pressing refresh button. If the application is installed on a local computer with GPU, the response is faster, about 10 seconds. Response for text query based search is fast (a couple of seconds) as it does not need Tensorflow/GPU.


$ mkdir -p /home/username/tmp # this is to store temporary files generated while running the application.  Set up a cron job to clear this directory periodically

$ sudo apt-get update
$ sudo apt-get upgrade
$ sudo apt-get install build-essential cmake unzip pkg-config
$ sudo apt-get install libjpeg-dev libpng-dev libtiff-dev
$ sudo apt-get install libjasper-dev
--If you receive an error about libjasper-dev  being missing then follow the following instructions:
$ sudo add-apt-repository "deb http://security.ubuntu.com/ubuntu xenial-security main"
$ sudo apt update
$ sudo apt install libjasper1 libjasper-dev
$ sudo apt-get install libgtk-3-dev
$ sudo apt-get install -y libsm6 libxext6 libxrender-dev
 
$ sudo apt install git

10. 
$ git clone https://github.com/kejitan/ESVGscale
$ mv assets.zip ESVGscale/
$ cd ESVGscale
$ unzip assets.zip
$ rm assets.zip -- to make 11 GB room on SSD
$ unzip objects.zip
$ unzip images_data.zip
$ unzip annADK.zip
$ tar -xzf ANN.tgz

-- In this repository we have given the annADK.tgz and ANN.tgz files. Procedure to create these files is explained in Installation1.md doc. assets.zip being > 11 GB file is not included in the repository. assets.zip is made available on Google drive at the following link:
https://drive.google.com/file/d/19iPg0MgP06fhL3gsIz3KE1CL8hyqmrNT/view?usp=sharing 

-- Install Anaconda
$ bash Anaconda3-2020.02-Linux-x86_64.sh
--Allow conda to make changes: conda init

$ source ~/.bashrc

11. create PSP15 environment
$ conda create -n PSP15 python=3.6
$ source ~/.bashrc

12. 
$ wget https://bootstrap.pypa.io/get-pip.py
$ python get-pip.py

$ cd ESVGscale

13. pip install -r requirements.txt

14. Install Elastic Search 7.4.2

-- ref https://outlandish.com/blog/creating-an-aws-instance-running-elasticsearch-3/
$ wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.4.2.deb
$ sudo dpkg -i elasticsearch-7.4.2-amd64.deb

15. Add elastic search to startup at boot
-- To configure Elasticsearch to start automatically when the system boots up, run the following commands:

$ sudo /bin/systemctl daemon-reload
$ sudo /bin/systemctl enable elasticsearch.service

-- Elasticsearch can be started and stopped as follows:
$ sudo systemctl start elasticsearch.service
$ sudo systemctl stop elasticsearch.service

$ curl -O https://artifacts.elastic.co/downloads/kibana/kibana-7.4.2-linux-x86_64.tar.gz
$ curl https://artifacts.elastic.co/downloads/kibana/kibana-7.4.2-linux-x86_64.tar.gz.sha512 | shasum -a 512 -c - 
$ tar -xzf kibana-7.4.2-linux-x86_64.tar.gz
$ mv kibana-7.4.2-linux-x86_64 kibana742 
$ kibana742/bin/kibana &

18. create idx0, idx1 and vgnum indexes
$ python ESMap.py
$ python ESANN.py
$ python ESannADK.py

# setting up of tmp directory path in home/username
-- create a tmp directory say /home/username/tmp 
-- Open VG_ADK_600.py and change instances of /home/kejitan/tmp to /home/username/tmp
-- This directory is used to write temporary files in the 'Display Similar Images' query processing
19. start application from ESVGscale directory
$ python VG_ADK_600.py

20. Open a browser and visit localhost:8050

21. Please run the application from your browser as described in README.md doc.
