
* This is a single user application. If multiple users use this aplication simultaneously, the user input/outputs will interfer.

* We have not configured GPU on our instance therefore 'Display Similar Images' part of the application takes a little longer (about 15 seconds). Please wait for this period after clicking 'Display Similar Images' button before pressing refresh button 

# Installation on AWS

1. Create Amazon EC2 instance with mimimum configuration of 2 vCPUs, 8GB memory, 50 GB SSD- Please see aws.amazon.com for details on how to create EC2 instance.

2. Set up public elastic IP address  (e.g. 52.14.143.209). This is the address from which the users will access the application

3. Setup security group and edit inbound rules to allow traffic on the following ports which you authorise specified to access the application. Ports (22, 8050, 80, 8080, 443). Set filter to 0.0.0.0 to allow traffic from any IP address. (Ports 80, 8080, 443 are not strictly required. They have been enabled, if we install web server and other features such as waitress server in the future). 

4. Upload the following files from your local computer to /home/ubuntu on home directory on EC2 instance using scp. Please replace the file names and EC2 computer name to reflect your instance. 

5. -- In this repository we have given the annADK.tgz and ANN.tgz files. Procedure to create these files is explained in Installation1.md doc. if desired, these can be carried on the local computer and then the files can be copied to EC2 using scp. Procedure to create assets.zip file is also given in that document. assets.zip being > 11 GB file is not included in the repository. assets.zip is made avaibale on Google drive at the following link:
https://drive.google.com/file/d/19iPg0MgP06fhL3gsIz3KE1CL8hyqmrNT/view?usp=sharing

-- download anaconda Anaconda3-2020.02-Linux-x86_64.sh on your local computer

$ scp -i awskeypair.pem assets.zip ubuntu@ec2-52-14-143-209.us-east-2.compute.amazonaws.com:/home/ubuntu/

$ scp -i awskeypair.pem Anaconda3-2020.02-Linux-x86_64.sh ubuntu@ec2-52-14-143-209.us-east-2.compute.amazonaws.com:/home/ubuntu/

where awskeypair.pem is the private key file that you created while creating the instance. "ec2-52-14-143-209.us-east-2.compute.amazonaws.com" -- something similar will be your public dns

5. login to EC2 ssh shell.

$ ssh -i "awskeypair.pem" ubuntu@ec2-52-14-143-209.us-east-2.compute.amazonaws.com

This will open a secure shell (SSH terminal)

6. From the SSH terminal run the foillowing commands

$ mkdir -p /home/ubuntu/tmp # this is to store temporary files generated while running the application.  Set up a cron job to clear this directory periodically

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

10. git clone https://github.com/kejitan/ESVGscale
$ mv assets.zip ESVGscale/
$ cd ESVGscale
$ unzip assets.zip
$ rm assets.zip -- to make 11 GB room on SSD
$ unzip objects.zip
$ unzip images_data.zip
$ tar -xzf annADK.tgz
$ tar -xzf ANN.tgz

-- install conda 
$ cd
$ bash Anaconda3-2020.02-Linux-x86_64.sh
--Allow conda to make changes: conda init

$ source ~/.bashrc

11. create PSP15 environment
$ conda create -n PSP15 python=3.6
$ source ~/.bashrc

12. 
$ wget https://bootstrap.pypa.io/get-pip.py
$ python get-pip.py

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

18. create idx0, idx1 and vgnum indexes - these need to be created on every installation. We cannot create a file, copy and get the performance.
$ python ESMap.py
$ python ESANN.py
$ python ESannADK.py

19. start application from ESVGscale directory
$ python VG_ADK_aws.py

20. Open a browser on local machine and visit link 101.102.103.104:8050 where 52.14.143.209 is your elastic IP address on the Amazon instance on which the application is running

21. Please run the application from your browser as described in README.doc
