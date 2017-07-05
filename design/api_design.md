**GET**:

* `api/translate?type=<>&lang=<>&pk=<>` - translate any type of object with given lang with pk
* `api/translate_ratio?type=<>&lang=<>&pk=<>` - provides translated ratio for any type of object with given lang with pk
* `api/available_languages?type=<>&pk=<>` - provides array of available languages for specific object with pk


**POST**:
- `api/update_translation/?type=<>&lang=<>&lang=<>&pk=<>&new_text` - method, which updates steps[pk] in `lang` from `type` service with `new_text`
- `api/create_translation/?type=<>&lang=<>&lang=<>&pk=<>&new_text` - method, which creates steps[pk] in `lang` from `type` service with `new_text`
