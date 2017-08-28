# Stepik Translation Microservice
This microservice provides API functionality to create translations of [stepik.org](stepik.org) step materials, like steps-source and texts.
API endpoints are listed on TODO.

You can find comparison of translation service API on this page: TODO. <br>
**TL;DR**: Azure with Yandex have slightly better translation than Google. It was tested on language pair: ru -> en.

## Starting Development

**Setup your Docker environment**

This project uses docker infrastructure. Make sure that you installed:

1. `docker`
2. `docker-compose` version 1.13.0 or higher
3. `docker-machine` only for macOS or Windows

After installing all programs I describe process of setuping service on Ubuntu 16.04. If you are using macOS or Windows, please follow [instructions](https://docs.docker.com/machine/get-started/). On Ubuntu you should run only two commands:
```
# Enable docker to start on boot
$ sudo systemctl enable docker

# Start docker right now
$ sudo systemctl start docker
```

**Setup your .env file**

Create file .env in the web/translation_microservice folder with params below. 
```
DEBUG=False # set True only on localhost
SECRET_KEY=... # generate https://www.miniwebtool.com/django-secret-key-generator/
POSTGRES_DB=translation  # you can choose any
POSTGRES_USER=pasha  # you can choose any
POSTGRES_PASSWORD=abacaba # you can choose any
POSTGRES_ADDRESS=postgres
YANDEX_API_KEY=... # go to https://tech.yandex.com/translate/
STEPIK_CLIENT_ID=... # can get both values here https://stepik.org/oauth2/applications/ 
STEPIK_CLIENT_SECRET=... 
```

**Run the project**
- Run `docker-compose build` and then `docker-compose up` to build and start the project's containers.  If you would like to run them in the background (without logs visible), run `docker-compose up -d`
- To remove all containers, run `docker-compose down`.

**Additional commands**

Unfortunately after starting `docker-compose` we have to run following commands. Open separate terminal window, write
`$ docker-compose run --rm web python manage.py shell` and type:
```
>>> from api_controller.models import ApiController
>>> from translation.models import TranslationService
>>> ApiController.objects.create()
>>> yandex = TranslationService.objects.create(service_name="yandex", api_version=1.5, base_url="https://translate.yandex.net/api/v1.5/tr.json/translate")
```
One more command to run for correct admin pages displaying: `$ docker-compose run --rm web python manage.py collectstatic --no-input`

## Admin access
If you want to help Stepik with materials translation or gain admin access for this microservice, please write email on maxim.averin@stepik.org.

## TODO

* make a link to swagger
* move additional commands info Dockerfile
* post a link with comparison table
