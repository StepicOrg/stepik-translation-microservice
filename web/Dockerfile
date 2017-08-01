# our application builds from official python image
FROM python:3.5
# not to use buffer
ENV PYTHONUNBUFFERED 1

RUN mkdir /code # make dir /code
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