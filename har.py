"""
    This module implements HAR as per specification version 1.2.
"""
from collections import MutableMapping
from json import dumps, loads
from zlib import compress, decompress


class HAREncodable(MutableMapping):
    __register__ = []
    __required__ = []

    def __init__(self, *args, **kwargs):
        self.__dict__ = {}

        if len(args) > 0:
            kwargs = args[0]

        for key, value in kwargs.iteritems():
            self[key] = value

        for key in self.__required__:
            self[key]

    def __setitem__(self, key, value):
        item_type = self.__required__.get(key, self.__optional__.get(key, None))
        if type(item_type) is type:
            value = item_type(value)
        elif type(item_type) is list:
            value = [HAR[key](v) for v in value]
        elif type(item_type) is dict:
            value = HAR[key](value)

        return self.__dict__.__setitem__(key, value)

    def __getitem__(self, *args, **kwargs):
        return self.__dict__.__getitem__(*args, **kwargs)

    def __delitem__(self, *args, **kwargs):
        return self.__dict__.__delitem__(*args, **kwargs)

    def __len__(self):
        return self.__dict__.__len__()

    def __iter__(self):
        return self.__dict__.__iter__()

    def json(self):
        dump = self
        if self.__class__ is HAR['log']:
            dump = {"log": dump}
        return dumps(dump, default=lambda x: dict(x))

    def compress(self):
        return compress(self.json())

    def decompress(self, compressed_json_string):
        return self.__init__(loads(decompress(compressed_json_string)))


class _HAR(MutableMapping, object):
    """
        HAR implementation as per specification version 1.2 ()
        This class maps the specification contained in __map__ to dynamic subclasses stored in __classes__.
        It then exposes all of this by implementing MutableMapping, the generated subclasses being its keys.
    """
    __map__ = {"log": {"__required__": {"version": str,
                                        "creator": {},
                                        "entries": [], },
                       "__optional__": {"browser": {},
                                        "pages": [],
                                        "comment": str, }},
               "creator": {"__required__": {"name": str,
                                            "version": str, },
                           "__optional__": {"comment": str}, },
               "browser": {"__required__": {"name": str,
                                            "version": str, },
                           "__optional__": {"comment": str}, },
               "pages": {"__required__": {"startedDateTime": str,
                                          "id": str,
                                          "title": str, },
                         "__optional__": {"pageTimings": {},
                                          "comment": str}, },
               "pageTimings": {"__required__": {},
                               "__optional__": {"onContentLoad": int,
                                                "onLoad": int,
                                                "comment": str}, },
               "entries": {"__required__": {"startedDateTime": str,
                                            "time": int,
                                            "request": {},
                                            "response": {},
                                            "cache": {},
                                            "timings": {}, },
                           "__optional__": {"pageref": str,
                                            "serverIPAddress": str,
                                            "connection": str,
                                            "comment": str}, },
               "request": {"__required__": {"method": str,
                                            "url": str,
                                            "httpVersion": str,
                                            "cookies": [],
                                            "headers": [],
                                            "queryString": [],
                                            "headersSize": int,
                                            "bodySize": int, },
                           "__optional__": {"postData": {},
                                            "comment": str}, },
               "response": {"__required__": {"status": int,
                                             "statusText": str,
                                             "httpVersion": str,
                                             "cookies": [],
                                             "headers": [],
                                             "content": {},
                                             "redirectURL": str,
                                             "headersSize": int,
                                             "bodySize": int, },
                            "__optional__": {"comment": str}, },
               "cookies": {"__required__": {"name": str,
                                            "value": str, },
                           "__optional__": {"path": str,
                                            "domain": str,
                                            "expires": str,
                                            "httpOnly": bool,
                                            "secure": bool,
                                            "comment": str}, },
               "headers": {"__required__": {"name": str,
                                            "value": str, },
                           "__optional__": {"comment": str}, },
               "queryString": {"__required__": {"name": str,
                                                "value": str, },
                               "__optional__": {"comment": str}, },
               "postData": {"__required__": {"mimeType": str,
                                             "params": [],
                                             "text": str, },
                            "__optional__": {"comment": str}, },
               "params": {"__required__": {"name": str, },
                          "__optional__": {"value": str,
                                           "fileName": str,
                                           "contentType": str,
                                           "comment": str}, },
               "content": {"__required__": {"size": int,
                                            "mimeType": str, },
                           "__optional__": {"compression": int,
                                            "text": str,
                                            "comment": str}, },
               "cache": {"__required__": {},
                         "__optional__": {"beforeRequest": {},
                                          "afterRequest": {},
                                          "comment": str}, },
               "beforeRequest": {"__required__": {"lastAccess": str,
                                                  "eTag": str,
                                                  "hitCount": int, },
                                 "__optional__": {"expires": str,
                                                  "comment": str, }, },
               "afterRequest": {"__required__": {"lastAccess": str,
                                                 "eTag": str,
                                                 "hitCount": int, },
                                "__optional__": {"expires": str,
                                                 "comment": str, }, },
               "timings": {"__required__": {"send": int,
                                            "wait": int,
                                            "receive": int, },
                           "__optional__": {"blocked": int,
                                            "dns": int,
                                            "connect": int,
                                            "ssl": int,
                                            "comment": str, }, }}

    def __init__(self):
        self.__classes__ = dict([(name,
                                  type(name, (HAREncodable, ), self.__map__[name]))
                                 for name in self.__map__])

    def __getattr__(self, item):
        return self[item]

    def __getitem__(self, *args, **kwargs):
        return self.__classes__.__getitem__(*args, **kwargs)

    def __setitem__(self, *args, **kwargs):
        return self.__classes__.__setitem__(*args, **kwargs)

    def __delitem__(self, *args, **kwargs):
        return self.__classes__.__delitem__(*args, **kwargs)

    def __iter__(self):
        return self.__classes__.__iter__()

    def __len__(self):
        return self.__classes__.__len__()


HAR = _HAR()