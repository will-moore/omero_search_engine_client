FROM python:3.9.0
RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get install -y build-essential
RUN apt-get clean
ADD  omero_search_engine_client  /searchengineclient
ADD start_gunicorn_serch_engine_client.sh /searchengineclient
RUN cd /searchengineclient
WORKDIR /searchengineclient
RUN pip  install -r  requirments.txt
RUN pip install gunicorn
EXPOSE 5568
RUN echo $HOME
#ENTRYPOINT  ["python","manage.py","runserver","-p","5558","-h","0.0.0.0"]
ENTRYPOINT ["bash", "start_gunicorn_serch_engine_client.sh"]
