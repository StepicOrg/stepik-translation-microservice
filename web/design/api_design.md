**/api/translation**

public:

* *GET* `lessons/?page=<>&service_name=<>` - get all lessons
* *GET* `lessons/<stepik_id>/?lang=<>&service_name=<>` - get specific lesson
* *GET* `steps/?page=<>&lang=<>&service_name=<>` - get all translated steps
* *GET* `steps/<stepik_id>/?lang=<>&service_name=<>` - get specific step
* *GET* `attempts/<stepik_id>/?service_name=<>&access_token=<>` - get specific attempt, access_token is required (you can get it [here](https://stepik.org/oauth2/applications/))

private:

* *UPDATE* `steps/<stepik_id>/?lang=<>&text=<>&service_name=<>` - update translated step's text
* *POST* `steps/<stepik_id>/?lang=<>&service_name=<>` - create translated step's text

Private methods should be accessed with `admin_token`

**/api/translation-ratio**
* *GET* `lesson/<stepik_id>/?lang=<>&service_name=<>` - get `translation_ratio` of specific lesson
* *GET* `course/<stepik_id>/?lang=<>&service_name=<>` - get `translation_ratio` of specific course

**/api/available-languages**
* *GET* `courses/<stepik_id>/?service_name=<>` - get `available-languages` for course
* *GET* `lessons/<stepik_id>/?service_name=<>` - get `available-languages` for lesson
* *GET* `steps/<stepik_id>/?service_name=<>` - get `available-languages` for step


