#docker build . -t searchengine
#FROM centos:7
FROM centos/python-36-centos7
USER root
RUN yum -y install epel-release
RUN yum -y update
RUN yum groupinstall "Development Tools" -y
#RUN yum install openssl-devel libffi-devel bzip2-devel -y
#RUN yum install wget -y
RUN  yum install gcc openssl-devel bzip2-devel libffi-devel zlib-devel readline-devel python-cliff wget git curl -y


#RUN yum install -y git
#RUN yum install -y curl
#RUN yum install -y zlib
#RUN yum install -y bzip2
#RUN yum install -y readline-devel
#RUN yum install -y sqlite-devel

#RUN yum install -y python-cliff

#RUN yum install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
#RUN yum install -y gcc make zlib1g-dev libreadline-dev libreadline8 sqlite3 libsqlite3-dev libbz2-dev python-tk python3-tk tk-dev
RUN wget https://www.python.org/ftp/python/3.9.0/Python-3.9.0.tgz
RUN tar xvf Python-3.9.0.tgz
RUN cd Python-3.9.0 && ./configure --enable-optimizations &&  make altinstall


#RUN curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash
#RUN ~/.pyenv/bin/pyenv install 3.9.0
#RUN ~/.pyenv/bin/pyenv virtualenv 3.9.0 searchengineclient
#RUN ~/.pyenv/versions/searchengineclient/bin/python3.9 -m pip install --upgrade pip
RUN mkdir /searchengineclien
RUN mkdir /searchengineclien/client_logs
ADD  omero_search_engine_client /searchengineclient
ADD start_gunicorn_serch_engine_client.sh /searchengineclient
ADD run_app.sh /searchengineclient
RUN cd /searchengineclient
RUN mkdir /etc/searchengineclient
RUN mkdir /etc/searchengineclient/client_logs
WORKDIR /searchengineclient
#RUN ~/.pyenv/versions/searchengine/bin/pip install -r  requirments.txt
RUN pip3.9 install -r  requirments.txt
#RUN ~/.pyenv/versions/searchengine/bin/pip install gunicorn
RUN pip3.9 install gunicorn
EXPOSE 5567
#RUN echo $HOME
#RUN mkdir /tmp/logs

#ENTRYPOINT  ["python3.9","manage.py","runserver","-p","5569","-h","0.0.0.0"]
ENTRYPOINT ["bash", 	"run_app.sh"]


 
