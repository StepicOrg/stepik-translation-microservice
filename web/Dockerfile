# our application builds from official python image
# also if we wanna minimize size of container, use python:alpine
FROM python:3.5
# not to use buffer
ENV PYTHONUNBUFFERED 1

# make dir /code
RUN mkdir /code
# set it workdir
WORKDIR /code
# add requirements from current dir to /code
ADD ./requirements.txt /code/
# install all requirements
RUN pip install --no-cache-dir -r requirements.txt
# add all files from current folder to /code
ADD . /code/

# application can be reached at port 8000
EXPOSE 8000

# run gunicorn, binding nginx and django
CMD ["/usr/local/bin/gunicorn", "translation_microservice.wsgi", "-w", "2", "-b", ":8000", "--access-logfile", "-", "--capture-output"]