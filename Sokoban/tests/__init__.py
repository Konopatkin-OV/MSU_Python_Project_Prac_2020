import unittest

loader = unittest.TestLoader()
tests = loader.discover('Sokoban/tests')
testRunner = unittest.TextTestRunner()
testRunner.run(tests)