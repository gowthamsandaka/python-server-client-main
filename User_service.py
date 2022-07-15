"""
This program is deals with the each command and its functions
in the client server application
"""
import os
import time
import pandas as pd


class Client_User():
    """
    This class is used to define the user service functions
    """
    def __init__(self):
        """
         __init__ function The Parameters include :
        self.User_name : String representing the username of the user
        self.Login_users : Gives data of the users who are logged in
        self.is_Loginuser : True if the user logged in
        self.Users : Gives data of the users who are registered
        """
        self.User_name = None
        self.is_Loginuser = False
        self.Users = None
        self.Login_users = None
        self.current_directory = None
        self.index = {}

    def commands(self):
        """
        This function returns the commands to
        the user and shows how the commands will function
        """
        commands = ['register :', 'For registation of the User, command: register <username> <password> \n',
                 'login : ', 'for login the User, command:login <username> <password>\n',
                 'quit : ', 'To logging out the User, command:quit\n',
                 'change_folder : ', 'To change the path, command:change_folder <name>\n',
                 'list : ', 'list all the files in the path, command:list\n',
                 'read_file : ', 'read the data from the file, command:read_file <filename>\n',
                 'write_file : ', 'write the data into the file, command:write_file <filename>\n',
                 'create_folder : ', 'create new folder, command:create_folder <foldername>\n'
                   ]
        cmd = ('\n'.join(map(str, commands)))
        return cmd

    def register(self, username, password):
        """
        This function is used to create the user in the server
        -----------------------------------------------
        If the username is already exists it will return that
        the username is already taken
        ------------------------------------------------
        If the username and password are not given it will
        return the Invalid username password
        """
        register_Data = pd.read_csv('SessionServices/Users.csv')
        if username in register_Data['username'].to_list():
            return "\nusername is already taken\n"
        if username == "" or password == "":
            return "\nInvalid username password"
        adddata = pd.DataFrame(columns=['username', 'password'])
        adddata['username'] = [username]
        adddata['password'] = password

        register_Data = register_Data.append(adddata)
        register_Data.to_csv("SessionServices/Users.csv", index=False)
        name_of_directory = str(username)
        path_of_file = "Root/"
        path_of_directory = os.path.join(path_of_file, name_of_directory)
        os.mkdir(path_of_directory)
        return "\nUser Registered.\n"

    def login(self, username, password):
        """
        This function is used to login the user in the server
        ---------------------------------------------------
        If the user already login it will return that the user
        is already taken
        ---------------------------------------------------
        If the user login from the different address then it will
        return that login from the different adress
        """
        login_dict = {}
        login_Data = pd.read_csv('SessionServices/login_user.csv')
        login_dict = pd.read_csv("SessionServices/Users.csv").to_dict('split')
        login_users = []
        login_passwords = []
        k = 0
        for i in range(k, len(login_dict['data'])):
            list_users = (login_dict['data'][i][k])
            login_users.append(list_users)
        for i in range(k, len(login_dict['data'])):
            list_passwords = (login_dict['data'][i][k+1])
            login_passwords.append(list_passwords)
        if self.is_Loginuser:
            return "\nAlready logged in\n"
        if username not in login_users and password not in login_passwords:
            return "\nIncorrect username password\n"
        if username in login_Data['username'].tolist():
            return "\nLogged in from different address\n"

        self.is_Loginuser = True
        self.User_name = username
        self.current_directory = "Root/" + self.User_name
        add_login_data = pd.DataFrame(columns=['username'])
        add_login_data['username'] = [username]
        login_Data = login_Data.append(add_login_data)
        login_Data.to_csv('SessionServices/login_user.csv', index=False)
        return "\nLogin user successfully.\n"

    def quit(self):
        """
        This function is used to quit the user from the server
        """
        logout_Data = pd.read_csv('SessionServices/login_user.csv')
        if self.User_name in logout_Data['username'].tolist():
            rest_to_login = pd.DataFrame(columns=['username'])
            rest_to_login.to_csv('SessionServices/login_user.csv', index=False)
        self.User_name = None
        self.current_directory = ""
        self.is_Loginuser = False
        self.index = {}
        return "\nUser Signed out from the server!!\n"

    def create_folder(self, folder_name):
        """
        This function is used to create the folder
        ------------------------------------------
        If the given folder_name is already given in directory
        then it returns to enter another directory name to avoid
        duplication
        -------------------------------------------
        If given correct folder_name it creates folder based on
        given directory
        """
        if self.is_Loginuser is None:
            return"\nplease login to continue!!\n"
        current_path = os.path.join(self.current_directory)
        total_directory = []
        for new_path in os.listdir(current_path):
            sub_path = os.path.join(current_path, new_path)
            if os.path.isdir(sub_path):
                total_directory.append(new_path)
        if folder_name in total_directory:
            return "\nThis directory is already created please give another directory name.\n"
        os.mkdir(os.path.join(current_path, folder_name))
        return"\nCreated the "+folder_name+" successfully.\n"

    def change_folder(self, folderName):
        """
        This function is used to change the directory of
        the user to the specified folder in the directory
        ----------------------------------------------
        When the user provide the username and password to
        login the directory shifts to the username folder
        in the current directory or else request is denied
        ----------------------------------------------
        NOTE:In this function if you enter command back
        it will back the directory to the current user. 
        """
        if self.is_Loginuser is None:
            return "\nplease login to continue!!\n"
        path = os.path.join(self.current_directory)
        try:
            if folderName == "back":
                self.current_directory = "Root/" + self.User_name
                return "\nchanged directory to " + self.User_name + " successfully.\n"
            if folderName in os.listdir(path):
                self.current_directory = os.path.join(self.current_directory, str(folderName))
                return "\nchanged directory to "+folderName+" successfully.\n"
        except (FileNotFoundError, IOError):
            return("\nInput correct directory name.\n")
        return"\nInput correct directory name.\n"

    def read_file(self, fileName):
        """
        This function is used to read the file
        and return the first hundred characters in it.
        --------------------------------------
        If a file with the filename does not exist in the
        current directory for the user, the request is denied
        ----------------------------------------
        """
        if self.is_Loginuser is None:
            return "\nplease login to continue!!\n"
        path_read_directory = os.path.join(self.current_directory)
        read_files = []
        for file in os.listdir(path_read_directory):
            psub = os.path.join(path_read_directory, file)
            if os.path.isfile(psub):
                read_files.append(file)
        if fileName not in read_files:
            return "\nError file not found\n"
        read_path = os.path.join(path_read_directory, fileName)
        if read_path not in list(self.index.keys()):
            self.index[read_path] = 0
        file1 = open(read_path, "r")
        file_count = file1.read()
        read_index = self.index[read_path]
        index = str(read_index*100)
        data = file_count[read_index*100:(read_index+1)*100]
        self.index[read_path] += 1
        self.index[read_path] %= len(file_count)//100+1
        return "\n" + "file read from " + index + " to " + str(int(index)+100) + " are: " + data

    def write_file(self, filename, data):
        """
        Write the data into the file in the current directory
        ------------------------------------------------------
        If no filename exists then user must create the folder
        """
        if self.is_Loginuser is None:
            return "\nplease login to continue!!\n"
        path_write_directory = os.path.join(self.current_directory, filename)
        write_file = []
        path_sub_file = os.path.join(self.current_directory)
        for file in os.listdir(path_sub_file):
            psub = os.path.join(path_sub_file, file)
            if os.path.isfile(psub):
                write_file.append(file)
        file = open(path_write_directory, "a+")
        file.write(data)
        file.close()
        return"\nwritten "+filename+" successfully.\n"

    def list(self):
        """
        This functio is used to return all files
        and folders in the current directory
        """
        if self.is_Loginuser is None:
            return "\nplease login to continue!!\n"
        path1 = os.path.join(self.current_directory)
        total_data = []
        for name_of_file in os.listdir(path1):
            path2 = os.stat(os.path.join(path1, name_of_file))
            content_size = str(path2.st_size)
            content_time = str(time.ctime(path2.st_ctime))
            total_data.append([name_of_file, content_size, content_time])
        print(f"{path1}")
        list_data = "\nFilename||Size_of_file||Modified_Date"
        for i in total_data:
            data = " || ".join([i[0], i[1], i[2]]) + "\n"
            list_data += "\n" + "".join(map(str, data))
        return list_data
