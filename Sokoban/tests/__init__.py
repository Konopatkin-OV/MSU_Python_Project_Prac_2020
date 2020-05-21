import unittest
import os

loader = unittest.TestLoader()
tests = loader.discover(os.path.join('Sokoban', 'tests'))
testRunner = unittest.TextTestRunner()
testRunner.run(tests)
