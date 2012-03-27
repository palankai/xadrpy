# -*- coding: utf-8 -*-
import unittest2
from xadrpy.utils.jsonlib import JSONEncoder
import datetime

class JSONEncoderTestCase(unittest2.TestCase):
    
    def setUp(self):
        self.json_encoder = JSONEncoder()
        pass
        
    def tearDown(self):
        pass
    
    def test_object_serializer(self):
        
        class BaseTestClass(object):
            a = 12
            def __init__(self,b):
                self.b = b
        
        class ExtendedTestClass(BaseTestClass):
            c = 5

        class OverwritedExtendedTestClass(BaseTestClass):
            a = 7
            
        class ExtendedTestClassWithInit(BaseTestClass):
            d = 17
            
            def __init__(self, e):
                self.e = e
                super(ExtendedTestClassWithInit, self).__init__(15)
        
        base_test_object = BaseTestClass(10)
        base_test_object.g = 'hi'

        extended_test_object = ExtendedTestClass(3)
        overwrited_extended_test_object = OverwritedExtendedTestClass(9)
        extended_test_object_with_init = ExtendedTestClassWithInit(8)
        
        self.assertEqual(extended_test_object.a, 12)
        
        self.assertEqual(self.json_encoder._object_serializer(base_test_object), {'a':12, 'b':10, 'g': 'hi'})
        self.assertEqual(self.json_encoder._object_serializer(extended_test_object), {'a':12, 'b':3, 'c':5})
        self.assertEqual(self.json_encoder._object_serializer(overwrited_extended_test_object), {'a':7, 'b':9})
        self.assertEqual(self.json_encoder._object_serializer(extended_test_object_with_init), {'a':12, 'b':15, 'd':17, 'e': 8})
        
        BaseTestClass.g = 'hi'
        base_test_object = BaseTestClass(10)
        self.assertEqual(self.json_encoder._object_serializer(base_test_object), {'a':12, 'b':10, 'g': 'hi'})
    
    def test_encoding_primitives(self):
        self.assertEqual(self.json_encoder.encode(1), '1')
        self.assertEqual(self.json_encoder.encode('1'), '"1"')
        self.assertEqual(self.json_encoder.encode('hi'), '"hi"')
        self.assertEqual(self.json_encoder.encode("hi"), '"hi"')
        self.assertEqual(self.json_encoder.encode(12.4), '12.4')
        self.assertEqual(self.json_encoder.encode(True), 'true')
        self.assertEqual(self.json_encoder.encode(False), 'false')
        self.assertEqual(self.json_encoder.encode(None), 'null')
        self.assertEqual(self.json_encoder.encode(u"é"), '"\u00e9"')

        self.assertEqual(self.json_encoder.encode([1,2,3,3]), '[1, 2, 3, 3]')
        self.assertEqual(self.json_encoder.encode({'a': 12, 'b': '12'}), '{"a": 12, "b": "12"}')
        
        self.assertEqual(self.json_encoder.encode(datetime.date(year=1981, month=2, day=18)), '"1981-02-18"')
        self.assertEqual(self.json_encoder.encode(datetime.datetime(year=1981, month=2, day=18, hour=7, minute=35)), '"1981-02-18 07:35:00"')
        self.assertEqual(self.json_encoder.encode(datetime.datetime(year=1981, month=2, day=18, hour=7, minute=35, second=10)), '"1981-02-18 07:35:10"')
        self.assertEqual(self.json_encoder.encode(datetime.datetime(year=1981, month=2, day=18, hour=7, minute=35, second=10, microsecond=30)), '"1981-02-18 07:35:10"')

        self.assertEqual(self.json_encoder.encode(datetime.time(hour=7, minute=35)), '"07:35:00"')
        self.assertEqual(self.json_encoder.encode(datetime.time(hour=7, minute=35, second=10)), '"07:35:10"')
        self.assertEqual(self.json_encoder.encode(datetime.time(hour=7, minute=35, second=10, microsecond=30)), '"07:35:10"')

        self.assertEqual(self.json_encoder.encode(datetime.timedelta(seconds=13)), '13')
        self.assertEqual(self.json_encoder.encode(datetime.timedelta(minutes=2,seconds=13)), '133')
        self.assertEqual(self.json_encoder.encode(datetime.timedelta(minutes=2,seconds=13, microseconds=3)), '133.000003')
        self.assertEqual(self.json_encoder.encode(datetime.timedelta(minutes=2,seconds=13, microseconds=30)), '133.00003')
        
    
    def test_encoding_objects(self):
        class BaseTestClass(object):
            a = 12
            def __init__(self,b):
                self.b = b
        base_test_object = BaseTestClass(None)
        
        self.assertEqual(self.json_encoder.encode(base_test_object), '{"a": 12, "b": null}')

    def test_encoding_sub_objects(self):
        class BaseTestClass(object):
            a = 12
            def __init__(self,b):
                self.b = b
            
            def set_sub_object(self, subobj):
                self.subobj = subobj
                
        base_test_object = BaseTestClass(None)
        other_object = BaseTestClass('Hello')
        self.assertEqual(self.json_encoder.encode(base_test_object), '{"a": 12, "b": null}')
        
        self.assertEqual(self.json_encoder.encode(other_object), '{"a": 12, "b": "Hello"}')
        base_test_object.set_sub_object(other_object)

        self.assertEqual(self.json_encoder.encode(base_test_object), '{"a": 12, "b": null, "subobj": {"a": 12, "b": "Hello"}}')

    def test_encoding_requirsive_sub_objects(self):
        class BaseTestClass(object):
            a = 12
            def __init__(self,b):
                self.b = b
            
            def set_sub_object(self, subobj):
                self.subobj = subobj
                
        base_test_object = BaseTestClass(None)
        base_test_object.set_sub_object(base_test_object)
        with self.assertRaises(ValueError):
            self.json_encoder.encode(base_test_object)
        
        other_object = BaseTestClass('Hello')
        base_test_object.set_sub_object(other_object)
        other_object.set_sub_object(base_test_object)

        with self.assertRaises(ValueError):
            self.json_encoder.encode(base_test_object)
    