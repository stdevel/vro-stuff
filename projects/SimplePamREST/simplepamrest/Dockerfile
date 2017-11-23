#Simple Flask-based PAM web application written in Python for demo purposes
FROM centos:centos7
MAINTAINER Christian Stankowic <info@stankowic-development.net>
EXPOSE 5000

#update _all_ the packages
RUN yum install -y deltarpm
RUN yum update -y

#install Python stuff
RUN yum install -y python-flask sqlite git

#get SimplePamREST
RUN git clone https://github.com/stdevel/vro-stuff.git

#make sure it's accessible from remote
RUN sed -i -e 's/debug=False/debug=False, host="0.0.0.0"/g' vro-stuff/projects/SimplePamREST/SimplePamREST.py

#set entrypoint
WORKDIR vro-stuff/projects/SimplePamREST
ENTRYPOINT python SimplePamREST.py
