**/api/translate**

public:

* *GET* `lessons/?page=<>&lang=<>&translation_service=<>` - get all lessons
* *GET* `lessons/<stepik_id>/?lang=<>&translation_service=<>` - get specific lesson
* *GET* `steps/?page=<>&lang=<>&translation_service=<>` - get all translated steps
* *GET* `steps/<stepik_id>/?lang=<>&translation_service=<>` - get specific step

private:

* *UPDATE* `steps/<stepik_id>/?lang=<>&text=<>&translation_service=<>` - update translated step's text
* *POST* `steps/<stepik_id>/?lang=<>&text=<>&translation_service=<>` - create translated step's text


**/api/translation-ratio**
* *GET* `lesson/<stepik_id>/?lang=<>&translation_service=<>` - get `translation_ratio` of specific lesson
* *GET* `course/<stepik_id>/?lang=<>&translation_service=<>` - get `translation_ratio` of specific course

**/api/available-languages**
* *GET* `courses/<stepik_id>/?translation_service=<>` - get `available-languages` for course
* *GET* `lessons/<stepik_id>/translation_service=<>` - get `available-languages` for lesson
* *GET* `steps/<stepik_id>/?translation_service=<>` - get `available-languages` for step


Optional params for requests: `lang` and `translation_service`
Future support: `ids`
