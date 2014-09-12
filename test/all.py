import winbrewtest
import inspect
import glob
import os

def test_case(case):
    test = case() 
    functions = inspect.getmembers(test)
    for name, fn in functions:
        if name.startswith('test_'):
            fn()

def test_module(name):
    module = __import__(name)
    for name, item in module.__dict__.iteritems():
        if inspect.isclass(item) and issubclass(item, winbrewtest.TestCase):
            test_case(item)

def test_all():
    files = glob.glob("*.py")
    for file in files:
        if file not in ('all.py', 'winbrewtest.py'):
            file = os.path.splitext(file)[0]
            test_module(file)
    

if __name__ == '__main__':
    test_all()
    
