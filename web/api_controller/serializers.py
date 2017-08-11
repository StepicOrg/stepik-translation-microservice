import collections
from django.core.paginator import Page
import inflection


class PaginationDecorator(object):
    def __init__(self, wrapped_serializer_instance):
        self.object = wrapped_serializer_instance

    @property
    def data(self):
        try:
            return self.decorate_data(self.object)
        except AttributeError as e:
            # change AttributeError to Exception here to bubble through __getattr__
            raise Exception(e)

    @property
    def resource_name_plural(self):
        return inflection.pluralize(self.object["type"])

    def decorate_data(self, old_data):
        if self.object is None:
            return old_data
        meta = collections.OrderedDict([
            ('page', 1),
            ('has_next', False),
            ('has_previous', False)
        ])
        if isinstance(self.object["page"], Page):
            meta['page'] = self.object["page"].number
            meta['has_next'] = self.object["page"].has_next()
            meta['has_previous'] = self.object["page"].has_previous()
        ret = collections.OrderedDict(meta=meta)
        old_data = collections.OrderedDict([
            (self.resource_name_plural, self.object["page"].object_list)
        ])
        ret.update(old_data)
        return ret
