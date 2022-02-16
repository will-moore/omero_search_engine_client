#docker build . -t searchengineclient
FROM centos/python-36-centos7
USER root
RUN yum -y install epel-release
RUN yum -y update
#RUN yum groupinstall "Development Tools" -y
#RUN  yum install gcc openssl-devel bzip2-devel libffi-devel zlib-devel readline-devel python-cliff wget git curl -y

RUN wget https://www.python.org/ftp/python/3.9.0/Python-3.9.0.tgz
RUN tar xvf Python-3.9.0.tgz
RUN cd Python-3.9.0 && ./configure --enable-optimizations &&  make altinstall
RUN yum clean all && rm -rf /var/cache/yum

RUN mkdir /searchengineclien
RUN mkdir /searchengineclien/client_logs
ADD  . /searchengineclient
ADD deployment/docker/centos/start_gunicorn_serch_engine_client.sh /searchengineclient
ADD deployment/docker/centos/run_app.sh /searchengineclient
RUN cd /searchengineclient
RUN mkdir /etc/searchengineclient
RUN mkdir /etc/searchengineclient/client_logs
WORKDIR /searchengineclient

RUN pip3.9 install -r  requirements.txt

RUN pip3.9 install gunicorn
EXPOSE 5567


#ENTRYPOINT  ["python3.9","manage.py","runserver","-p","5569","-h","0.0.0.0"]
ENTRYPOINT ["bash", 	"run_app.sh"]


 
