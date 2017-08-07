import collections
from django.core.paginator import Page
import inflection


class SerializerTypeDataDecorator(object):
    def __init__(self, wrapped_serializer_instance, resource_name):
        self._wrapped_instance = wrapped_serializer_instance
        self._resource_name = resource_name.value

    @property
    def data(self):
        try:
            print("ALLLA", self.decorate_data(self._wrapped_instance.data))
            return self.decorate_data(self._wrapped_instance.data)
        except AttributeError as e:
            # change AttributeError to Exception here to bubble through __getattr__
            raise Exception(e)

    @property
    def resource_name_plural(self):
        return inflection.pluralize(self._resource_name)

    def decorate_data(self, old_data):
        return collections.OrderedDict({
            self.resource_name_plural: data_to_list(old_data)
        })


def data_to_list(data):
    return data if isinstance(data, list) else [data]


class PaginationDecorator(object):
    def __init__(self, wrapped_serializer_instance):
        self.object = wrapped_serializer_instance

    @property
    def data(self):
        try:
            return self.decorate_data(self.object.data)
        except AttributeError as e:
            # change AttributeError to Exception here to bubble through __getattr__
            raise Exception(e)

    def decorate_data(self, old_data):
        if self.object is None:
            return old_data
        meta = collections.OrderedDict([
            ('page', 1),
            ('has_next', False),
            ('has_previous', False)
        ])
        if isinstance(self.object, Page):
            meta['page'] = self.object.number
            meta['has_next'] = self.object.has_next()
            meta['has_previous'] = self.object.has_previous()
        ret = collections.OrderedDict(meta=meta)
        ret.update(old_data)
        return ret
