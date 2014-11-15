harparse
========

This is yet another python HAR Parser utility. However unlike its contemporaries it uses a recursive strategy in order to provide an abstract yet easy to understand and adapt handle on the HAR format in python.

Installation
============
Installation is straight forward:

    git clone https://github.com/JustusW/harparser.git
    cd harparser
    python setup.py install

or if you don't want the code locally:

    pip install -e git://github.com/JustusW/harparser.git#egg=harparser

or

    pip install harparser

Usage
=====
If you just want to read and write HARs usage is simple:

    from harparser import HAR
    my_har = HAR.log().json(<JSON_STRING>)

This call is equivalent to:

    from harparser import HAR
    from json import loads
    my_har = HAR.log(loads(<JSON_STRING>))

Every HAR class is implementing collections.MutableMapping thus can be cast to dict easily:

    dict(my_har)
    my_har.__dict__

The library harparse provides convenience methods for loading HAR from json strings and compressed json strings.

    from harparser import HAR
    my_har = HAR.log().decompress(<COMPRESSED_JSON_STRING>)

This call is equivalent to:

    from harparser import HAR
    from zlib import decompress
    from json import loads
    my_har = HAR.log(loads(decompress(<COMPRESSED_JSON_STRING>)))

All HAR classes are accessible via their key as defined in the official spec for HAR 1.2. You can access them either as dict like keys or as attributes of HAR. The following methods of access are yielding identical classes:

    HAR.pageTimings is HAR['pageTimings'] and HAR.pageTimings is HAR.get('pageTimings')

Obviously the real magic starts once you overwrite or inherit from the very basic structural integrity checking behaviour and add your own little helpers. As an example I give you this handy log helper, that provides an add method automatically deciding between pages and entries, as well as a reset method and some scaffolding.

    class _HARLog(HAR.log):
        def __init__(self):
            HAR.log.__init__(self, {"version": "1.2",
                                    "creator": {"name": "MITMPROXY HARExtractor",
                                                "version": "0.1",
                                                "comment": ""},
                                    "pages": [],
                                    "entries": []})
        
        def reset(self):
            self.__init__()
        
        def add(self, obj):
            if isinstance(obj, HAR.pages):
                self['pages'].append(obj)
            if isinstance(obj, HAR.entries):
                self['entries'].append(obj)

Advanced Usage
==============
Internally HAR is only an instance of the private class `_HAR`. The `__init__` method instantiates all keys defined in the private attribute `__map__` as classes extending HAREncodable. By default all changes to HAR will be shared globally. If you want to make changes without exposing them like that you have two options.

    from harparse import _HAR
    MyHAR = _HAR()

or

    class _MyOtherHAR(_HAR):
        pass
    MyOtherHAR = _MyOtherHAR()

Simply overwriting the keys of the `_HAR` instance will change the behaviour of all subsequent usages. An example would be this:

    class HARpageTimings(HAR.pageTimings):
        def __setitem__(self, key, value):
            if key != 'comment':
                self['comment'] = "Key '%s' was set to '%s'." % (key, str(value))
            return super(HARpageTimings, self).__setitem__(key, value)
    
    MyHAR.pageTimings = HARpageTimings

You are encouraged to use this behaviour extensively: Be it ORM, input validation, input or output mapping whatever special behaviour you want, harparse is compatible.

Finally
=======
If you find anything that bugs you about my implementation or have suggestions to improve it feel free to contact me or just send me a pull request.
