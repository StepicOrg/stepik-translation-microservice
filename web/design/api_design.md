**/api/translate**

public:

* *GET* `lessons/?page=<>&service_name=<>` - get all lessons
* *GET* `lessons/<stepik_id>/?lang=<>&service_name=<>` - get specific lesson
* *GET* `steps/?page=<>&lang=<>&service_name=<>` - get all translated steps
* *GET* `steps/<stepik_id>/?lang=<>&service_name=<>` - get specific step

private:

* *UPDATE* `steps/<stepik_id>/?lang=<>&text=<>&service_name=<>` - update translated step's text
* *POST* `steps/<stepik_id>/?lang=<>&service_name=<>` - create translated step's text


**/api/translation-ratio**
* *GET* `lesson/<stepik_id>/?lang=<>&service_name=<>` - get `translation_ratio` of specific lesson
* *GET* `course/<stepik_id>/?lang=<>&service_name=<>` - get `translation_ratio` of specific course

**/api/available-languages**
* *GET* `courses/<stepik_id>/?service_name=<>` - get `available-languages` for course
* *GET* `lessons/<stepik_id>/?service_name=<>` - get `available-languages` for lesson
* *GET* `steps/<stepik_id>/?service_name=<>` - get `available-languages` for step


Optional params for requests: `lang` and `service_name`
Future support: `ids`
