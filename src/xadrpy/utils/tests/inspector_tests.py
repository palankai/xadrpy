import unittest2
from xadrpy.utils.inspector import is_method

class IsMethodTestCase(unittest2.TestCase):
    
    def test_is_method_on_function(self):
        
        def test_function():
            pass
        
        def test_one_arg_function(arg1):
            pass
        
        def test_two_arg_function(arg1, arg2):
            pass

        def test_multi_arg_function(*args, **kwargs):
            pass

        
        self.assertFalse(is_method(test_function))
        self.assertFalse(is_method(test_one_arg_function))
        self.assertFalse(is_method(test_two_arg_function))
        self.assertFalse(is_method(test_multi_arg_function))

    def test_is_method_on_method(self):
        class TestClass(object):
            
            def test_method(self):
                pass

            def test_one_arg_method(self, arg1):
                pass

            def test_two_arg_method(self, arg1, arg2):
                pass

            def test_multi_arg_method(self, *args, **kwargs):
                pass
            
        test_object = TestClass()

        self.assertTrue(is_method(TestClass.test_method))
        self.assertTrue(is_method(TestClass.test_one_arg_method))
        self.assertTrue(is_method(TestClass.test_two_arg_method))
        self.assertTrue(is_method(TestClass.test_multi_arg_method))

        self.assertTrue(is_method(test_object.test_method))
        self.assertTrue(is_method(test_object.test_one_arg_method))
        self.assertTrue(is_method(test_object.test_two_arg_method))
        self.assertTrue(is_method(test_object.test_multi_arg_method))
