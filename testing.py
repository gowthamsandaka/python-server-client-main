"""
This program used for the testing purpose of the
User_service class of the server-client appliation
"""
import unittest
import sys
import shutil
import os
import pandas as pd
from User_service import Client_User

class Client_testing(unittest.TestCase):
    """
    This class is used to define the testing
    the functions defined in the User_service class
    """
    def test_get_register(self):
        """
        This funtion is used to test the register function and get the response
        """
        testing_user = Client_User()
        testing_user.is_Loginuser = True
        expected_result = ['\nUser Registered.\n']
        obtained_result = []
        testing_data = [['register_user', 'john_henrik123']]

        for user_credentials in testing_data:
            obtained_result.append(testing_user.register(user_credentials[0], user_credentials[1]))
        
        quit_data = pd.DataFrame(columns=['username', 'password'])
        quit_data.to_csv('SessionServices/Users.csv', index=False)
        self.assertListEqual(obtained_result, expected_result)

    def test_get_login(self):
        """
        This funtion is used to test the login function and get the response
        """
        testing_user = Client_User()
        testing_user.register('login_user', 'peter_hardson')
        expected_result = ['\nLogin user successfully.\n']
        obtained_result = []
        testing_data = [['login_user', 'peter_hardson']]

        for user_credentials in testing_data:
            obtained_result.append(testing_user.login(user_credentials[0], user_credentials[1]))

        testing_user.is_login = True
        self.assertListEqual(obtained_result, expected_result)

    def test_get_list(self):
        """
        This funtion is used to test the list function and get the response
        """
        testing_user = Client_User()
        obtained_output = testing_user.list
        self.assertTrue(obtained_output)

    def test_get_create_folder(self):
        """
        This funtion is used to test the create_folder function and get the response
        """
        testing_user = Client_User()
        expected_result = ['\nCreated the login_user1 successfully.\n']
        obtained_result = []
        testing_user.register('login_user1', '123')
        testing_user.login('login_user1', '123')
        testing_data = [['login_user1']]

        for user_credentials in testing_data:
            obtained_result.append(testing_user.create_folder(user_credentials[0]))

        self.assertListEqual(obtained_result, expected_result)

    def test_get_change_folder(self):
        """
        This funtion is used to test the change_folder function and get the response
        """
        testing_user = Client_User()
        expected_result = ['\nchanged directory to sub_folder successfully.\n']
        obtained_result = []
        testing_user.register('login_user2', '123')
        testing_user.login('login_user2', '123')
        testing_user.create_folder('sub_folder')
        testing_data = [['sub_folder']]

        for user_credentials in testing_data:
            obtained_result.append(testing_user.change_folder(user_credentials[0]))

        self.assertListEqual(obtained_result, expected_result)
    
    def test_get_edit_file(self):
        """
        This funtion is used to test the write_file function and get the response
        """
        testing_user = Client_User()
        expected_result = ['\nwritten file1 successfully.\n']
        obtained_result = []
        testing_user.register('login_user3', '123')
        testing_user.login('login_user3', '123')
        testing_user.create_folder('sub_folder1')
        testing_user.change_folder('sub_folder1')
        testing_data = [['file1', 'hello_world']]

        for user_credentials in testing_data:
            obtained_result.append(testing_user.write_file(user_credentials[0], user_credentials[1]))

        self.assertListEqual(obtained_result, expected_result)

    def test_get_quit(self):
        """
        This funtion is used to test the quit function and get the response
        """
        testing_user = Client_User()
        expected_result = ["\nUser Signed out from the server!!\n"]
        obtained_result = []

        obtained_result.append(testing_user.quit())
        quit_data = pd.DataFrame(columns=['username'])
        quit_data.to_csv('SessionServices/login_user.csv', index=False)
        self.assertListEqual(obtained_result, expected_result)
       
def Test_client(test):
   
    load = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(load.loadTestsFromTestCase(test))
    runtest = unittest.TextTestRunner(verbosity=2)
    result = runtest.run(suite)
    if result.skipped:
        return False
    return result.wasSuccessful()

if __name__ == "__main__":
    """
    This funtion returns the results of the testing 
    """
    def test_case():
        print('#'*60 + "\nTesting cases:\n")
        return Test_client(Client_testing)
    if test_case() is not True:
        print("\n\tThis test are not passed")
        sys.exit(1)
    for file_name in os.listdir('Root/'):
        shutil.rmtree("Root/"+file_name)
    sys.exit(0)