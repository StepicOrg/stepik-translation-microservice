## Model Schema

This schema is designed to allow for power and flexibility in the API given its purpose may either change or expand in the near future.

### TranslationService

This is primary interface model in the system, describing API methods, which each translation service will implement. 

**Fields**
* API_KEY (string)
* BASE_URL (string)
* price per 1000 symbols (integer)
* api version (float)
* limit_free_count_symbols (integer)
* symbols_translated (integer)

**Relations**
- Belongs to: ApiController

**Methods**
- get_step(pk, lang, type) - get translated steps[pk] in `lang` from `type` service
- get_lesson(pk, lang, type) - get translated steps from lesson[pk]
- get_translated_ratio(lang, type_object, type_object_id) - percent of translated texts in `lang` in specific object. `type_object` is ['lesson', 'course'] 
- get_available_languages() - provide all languages which are used by specific service
- update_translated_text(pk, lang, type, new_text) - `POST` method, which updates steps[pk] in `lang` from `type` service with 
`new_text`
- create_translated_text(pk, lang, typ) -  `POST` method, which creates translation for steps[pk] in `lang` from `type` service

### YandexTranslator, GoogleTranslator, AzureTranslator

Theese models just implement `TranslationService` interface.

### ApiController
This is primary model, which will be facade for whole microservice and store all api endoints for users

**Fields**
* API_KEY (string)
* BASE_URL (string)
* api version (float)
* translation_services (TranslationService model)

**Methods** 
- add_translated_service
- deletetranslated__service

Actually it only has some setters/getters and views, where methods from `TranslationService` are called with specific service type.

### Translation
This is primary model, which defines the smallest translated piece. It can be inherited by other models.

**Fields**
* id (integer) id in translated database not in Stepik API DB
* lang (string)
* updated_at (date)
* created_at (date)
* text (string)

### TranslatedLesson

This model consists of translated steps.
