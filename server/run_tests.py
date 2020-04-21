import unittest
import sys

suite = unittest.TestLoader().discover(start_dir='./tests', pattern='test*.py')
if len(sys.argv) > 1:
    unittest.TextTestRunner(verbosity=int(sys.argv[1])).run(suite)
else:
    unittest.TextTestRunner(verbosity=1).run(suite)
