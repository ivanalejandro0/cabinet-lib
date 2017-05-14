#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import singledispatch
import json


class Item:
    def __init__(self, name, content, tags=None):
        if tags is None:
            tags = []

        self.name = name
        self.content = content
        self.tags = tags
        # self.type = "account|note|etc"  # for templating

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__

        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return "name: {0}; content: {1}; tags: {2}".format(
            self.name, self.content, self.tags)

    def __repr__(self):
        return str(self.__dict__)

    @classmethod
    def from_dict(cls, dct):
        """Use this to create an instance of this class from a dict.
        @rtype: cls
        """
        r = cls(dct['name'], dct['content'], dct['tags'])
        return r

    def serialize(self):
        """Return a representation of the current state of this instance.
        @rtype: dict
        """
        return vars(self)


@singledispatch
def to_serializable(obj):
    """Used by default."""
    return str(obj)


@to_serializable.register(Item)
def item_serializer(obj):
    """Used if *obj* is an instance of MyClass."""
    return obj.serialize()


def parse_class(dct):
    return Item.from_dict(dct)


def item_to_str(item):
    string = json.dumps(item, default=to_serializable)
    return string


def str_to_item(string):
    item = json.loads(string, object_hook=parse_class)
    return item
