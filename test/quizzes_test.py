import unittest
import datetime

from app.controllers.quizzes_controller import QuizzesController

class QuizzesTest(unittest.TestCase):

    def setUp(self):
        # Run tests on non-production data
        self.ctrl = QuizzesController('quizzes_test.py')
        
    def test_expose_failure_01(self):
        """
        The following test case is designed to expose a failure in add_quiz method.
        The method is expected to raise an exception when the title is not a string.
        But instead it fails at Line 63 in quizzes_controller.py as an integer input is trying to
        be concatenated with a string which is not possible.
        """

        with self.assertRaises(Exception):
            self.ctrl.add_quiz(-1, "Welcome to the quiz 1", datetime.datetime(2024, 5, 6), datetime.datetime(2024, 5, 17))
        
        """
        Using try and except block to catch the exception raised by the add_quiz method when
        the title is not a string can handle this failure. In that case the test case will pass 
        without the system crashing.
        """
        

    def test_expose_failure_02(self):
        """
        The following test case is designed to expose a failure in add_question method.
        The method is expected to raise an exception when the quiz title is not a string.
        But instead it fails at Line 81 where it is saving the data to the JSON file.
        The error roots at Line 78 where date time object is used in an fstring which is not possible.
        This method halts while writing the data to the JSON file corrupting the file which is talked 
        about in the next test case.
        """

        new_quiz_id = self.ctrl.add_quiz("Software Engineering - Quiz 1", "Welcome to the quiz 1", datetime.datetime(2024, 5, 6), datetime.datetime(2024, 5, 17))
        randomDate = datetime.datetime(2024, 5, 17)
        with self.assertRaises(Exception):
            self.ctrl.add_question(new_quiz_id, randomDate, "Why is SDLC important?")
        
        """
        Using try and except block to catch the exception raised by the add_question method when
        the quiz title is not a string can handle this failure. In that case the test case will pass
        without the system crashing.
        """
            
        

    def test_expose_failure_03(self):
        """
        The following test case is designed to expose a failure in loading and saving data.
        Methods save_data and load_data are expected to raise an exception when the data is corrupted.
        But instead they fail by trying to read a corrupted file and not being able to convert the data to json.
        The code fais at Line 55 in _save_data method in quizzes_controller.py.
        The error roots at Line 21 in data_loader.py where it is trying to convert the data to json.
        """
        new_quiz_id = self.ctrl.add_quiz("Software Engineering", "Welcome to the quiz", datetime.datetime(2024, 5, 6), datetime.datetime(2024, 5, 17))
        randomDate = datetime.datetime(2024, 5, 17)

        #This test case was case 2 which is just used for corrupting the file
        with self.assertRaises(Exception):
            self.ctrl.add_question(new_quiz_id, randomDate, "Why is SDLC important?")
        
        #This is the new test case which is designed to expose the failure in get_quiz_by_id method.
        #This extends to all other getter methods in the system.
        with self.assertRaises(Exception):
            new_quiz_id = self.ctrl.add_quiz("Software Engineering Quiz 2", "Welcome to the quiz 2", datetime.datetime(2024, 5, 6), datetime.datetime(2024, 5, 17))

        """
        Using try and except block to catch the exception raised by the load_data and save_data methods when
        the data is corrupted can handle this failure. In that case the test case will pass without the system crashing.
        """

if __name__ == '__main__':
    unittest.main()