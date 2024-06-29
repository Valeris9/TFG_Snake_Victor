import unittest
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(project_root)

from testfood import TestSnakeFood
from testgame import TestSnakeGame

class MainTest(unittest.TestCase):
    def test_run_tests(self):
        # Crear suite de pruebas
        suite = unittest.TestSuite()

        suite.addTest(unittest.makeSuite(TestSnakeFood))
        suite.addTest(unittest.makeSuite(TestSnakeGame))

        runner = unittest.TextTestRunner()
        result = runner.run(suite)

        self.assertTrue(result.wasSuccessful())

if __name__ == "__main__":
    unittest.main()
