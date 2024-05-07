import unittest
import datetime

from app.controllers.quizzes_controller import QuizzesController

# Creating a custom exception to handle database errors. Developers can include more information
class DataBaseError(Exception):
    pass

class QuizzesTest(unittest.TestCase):

    def setUp(self):
        # Run tests on non-production data
        self.ctrl = QuizzesController('quizzes_test.py')
        
    def tearDown(self) -> None:
        self.ctrl.clear_data()
        
    def test_expose_failure_01(self):
        """
        The following test case is designed to expose a failure in add_quiz method.
        The method is expected to raise an exception when the title is not a string.
        But instead it fails at Line 63 in quizzes_controller.py as an integer input is trying to
        be concatenated with a string which is not possible.
        """

        with self.assertRaises(AttributeError):
            self.ctrl.add_quiz(-1, "Welcome to the quiz 1", datetime.datetime(2024, 5, 6), datetime.datetime(2024, 5, 17))
        
        """
        Using try and except block to catch the exception raised by the add_quiz method when
        the title is not a string can handle this failure. Recommendation is to gracefully return another error.
        In that case the test case will pass without the system crashing.
        """
        

    def test_expose_failure_02(self):
        """
        The following test case is designed to expose a failure in add_question method.
        The method is expected to raise an exception when the quiz title is not a string.
        But instead it fails at Line 81 of quizzes_controller.py where it is saving the data to the JSON file.
        The error roots at Line 78 of quizzes_controller.py where date time object is used in an fstring which is not possible.
        The exact problem is trying to save non-json data to a json file at Line 21 in data_loader.py.
        This method halts while writing the data to the JSON file corrupting the file which is talked 
        about in the next test case.
        """

        new_quiz_id = self.ctrl.add_quiz("Software Engineering - Quiz 1", "Welcome to the quiz 1", datetime.datetime(2024, 5, 6), datetime.datetime(2024, 5, 17))
        randomDate = datetime.datetime(2024, 5, 17)
        with self.assertRaises(AttributeError):
            self.ctrl.add_question(new_quiz_id, randomDate, "Why is SDLC important?")
        
        """
        Using try and except block to catch the exception raised by the add_question method when
        the quiz title is not a string can handle this failure. Recommendation is to gracefully return another exception.
        In that case the test case will passwithout the system crashing.
        """  

    def test_expose_failure_03(self):
        """
        This test case is designed to expose a failure in get_quiz_by_id and related getter methods.
        These methods are expected to raise an exception when the data is corrupted in the JSON file.
        But instead they try to load the corrupted data and fail at Line 27 in data_loader.py. This causes 
        all the getter methods to fail as they are dependent on the data loaded from the JSON file.
        """

        #Corrupting the data in the JSON file and loading it!
        with open('data/quizzes_test.py', 'w') as file:
            file.write('{"availaT00:00:00","id90": "0523456e293e3d46ceaa60e5a9b27653","last_updatT19:32:22.272055","see quiz 1",are Engineering - Quiz 1"}]')
        self.ctrl._load_data()
        
        #Trying to get the quiz by id, the code crashes. But the test case should pass without the
        #system crashing. It can return a custom exception called DataBaseError.
        with self.assertRaises(DataBaseError):
            self.ctrl.get_quiz_by_id("0523456e293e3d46ceaa60e5a9b27653")
            
        """
        Using try and except block to catch the exception raised by the load_data method when
        the data is corrupted can handle this failure. Recommendation is to gracefully return another exception.
        In that case the test case will pass without the system crashing.
        """

if __name__ == '__main__':
    unittest.main()