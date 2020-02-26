


def register_user(username, password, email):
    # enter username
    # enter email
    # enter password
    pass

def login_user(username, password, url):
    # enter username
    # enter password
    pass

def logout_user():
    pass

def list_items():
    pass


def view():
    # view the ratings of all the professors
    pass

def average(professor_id,module_code):
    # get the average of a certain professor in a certain module
    pass

def rate(professor_id,module_code, year, semester, rating):
    # rate the teaching of a certain professor in a certain module instance
    pass

def client():
    # infinite loop
    while 1==1:
        user_command = input("Please enter a command : ")
        user_command_split = user_command.split()
        for i in range (0, len(user_command_split)):
            user_command_split[i] = user_command_split[i].replace(' ','')

###########################################################################################

        if user_command_split[0] == "register":
            username = input("Please enter your username : ")
            email = input("Please enter your email : ")
            password = input("Please enter your password : ")
            the_url = user_command_split[1]
            register_user(username, password, email)

###########################################################################################

        if user_command_split[0] == "login":
            try:
                the_url = user_command_split[1]
                username = input("Please enter your username : ")
                password = input("Please enter your password : ")
                login_user(username, password, the_url)
            except IndexError:
                print("Please enter a url to login to")

###########################################################################################

        if user_command_split[0] == "logout":
            logout_user()

###########################################################################################

        if user_command_split[0] == "list":
            list_items()

###########################################################################################

        if user_command_split[0] == "view":
            view()

###########################################################################################

        if user_command_split[0] == "average":
            try:
                professor_id = user_command_split[1]
                module_code = user_command_split[2]
                average(professor_id,module_code)
            except IndexError:
                print("Please add a professor id and module code as arguments")

###########################################################################################

        if user_command_split[0] == "rate":
            try:
                professor_id = user_command_split[1]
                module_code = user_command_split[2]
                year = user_command_split[3]
                semester = user_command_split[4]
                rating = user_command_split[5]
                rate(professor_id,module_code, year, semester, rating)
                
            except IndexError:
                print("Please add professor id, module code, year, semester and rating as arguments")
                

###########################################################################################

client()