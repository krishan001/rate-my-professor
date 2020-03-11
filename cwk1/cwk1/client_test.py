import json
import requests
import sys
import re

def register_user():
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

    print("\n")
    username = input("Enter a username : ")
    print("\n")
    email = input("Enter your email : ")
    print("\n")
    pswd = input("Enter a password : ")
    print("\n")
    conPswd = input("Confirm password : ")
    print("\n")

    if ( re.search(regex,email) and pswd == conPswd and (len(pswd)>5) and username.isalnum() and (len(username)>2)):
        PARAMS = {'usrname' : username, 'email' : email, 'pass' : pswd}
        req = requests.post('http://127.0.0.1:8000/api/register/', data = PARAMS )
        req = req.json()
        string = req['phrase']
        print(string)
    else:
        print("\nSorry!! Invalid values detected. Ensure :\n1) Your username is minimum length 3 and is alpha numeric.\n2) Passwords match and are also minimum length 6.\n3) Your email is valid.\n")

def login_user(key, url):
    print("\n")
    username = input("Enter your username : ")
    print("\n")
    pswd = input("Enter your password : ")
    print("\n")

    PARAMS = {'usrname' : username, 'pass' : pswd}
    # r = requests.post('http://127.0.0.1:8000/api/login/', data = PARAMS )
    req = requests.post(url, data = PARAMS )
    req = req.json()
    phrase = req['phrase']
    key = req['token']
    usrname = req['usrname']
    print(phrase)
    returnlist = {'key' : key, 'usrname' : usrname}
    return returnlist

def logout_user(key):
    if key == "":
        phrase = notLoggedIn()
        key = ""
        return key
    else:
        headers = {'Authorization': key}
        req = requests.get('http://127.0.0.1:8000/api/logout/', headers = headers)
        req = req.json()
        phrase = req['phrase']
        key = req['token']
        usrname = req['usrname']
        print(phrase)
        returnlist = {'key' : key, 'usrname' : usrname}
        return returnlist


def lists(key):
    headers = {'Authorization': key}
    req = requests.get('http://127.0.0.1:8000/api/list', headers = headers)
    if req.status_code == 200:
        req = req.json()
        li = []
        print("\n" + "Module ID" + "     " + "Module name" + "     " + "Semester" + "     " + "Year" + "     " + "Teacher ID" +"\n")
        for i in req['phrase']:
            li.append(i)
        x = len(li)
        for i in range(x):
            phrase = "\n" + str(li[i]['ID']) + "     " + str(li[i]['name']) + "     " + str(li[i]['sem']) + "     " + str(li[i]['year']) + "     " + str(li[i]['tc']) +"\n"
            print(phrase)
    else:
        req = req.json()
        print(notLoggedIn())


def rate(key, command):
    headers = {'Authorization': key}
    data = {"teach_ID" : command.split(" ")[1], "mod_ID" : command.split(" ")[2], "year" : command.split(" ")[3], "semester" : command.split(" ")[4], "rate" : command.split(" ")[5]}
    req = requests.post('http://127.0.0.1:8000/api/rate/', headers = headers, data = data)
    if req.status_code == 200:
        req = req.json()
        print(req["phrase"])
    elif req.status_code == 403:
        print(notLoggedIn())
    else:
        req = req.json()
        print(req["phrase"])

def view(key):
    headers = {'Authorization': key}
    req = requests.get('http://127.0.0.1:8000/api/view/', headers = headers)
    if req.status_code == 200:
        req = req.json()
        li = []
        for i in req['phrase']:
            li.append(i)
        for i in range(len(li)):
            string = "\n" + "The rating of Professor "+ li[i]['name'] +" is " + str(li[i]['Rating']) + "\n"
            print(string)
    else:
        req = req.json()
        print(notLoggedIn())

def average(key, command):
    print("\n")
    headers = {'Authorization': key}
    data = {"teach_ID" : command.split(" ")[1], "mod_ID" : command.split(" ")[2]}
    req = requests.get('http://127.0.0.1:8000/api/average/', headers = headers, data = data)
    if req.status_code == 200:
        req = req.json()
        phrase = "\nThe rating of Professor " + req["phrase"]['name'] + " in module " + req["phrase"]['module_n'] + " " + req["phrase"]['modid'] + " is " +  str(req["phrase"]['Rating']) + "\n"
        print(phrase)
    elif req.status_code == 403:
        print(notLoggedIn())
    else:
        req = req.json()
        print(req["phrase"])

def notLoggedIn():
    return ("\nYou are not logged in!!!. \nLog in first!!!!!!\n")

def main():
    key = ""
    usrname = ""
    while True:
        print("=======================================================================================================")
        print("Please enter a command:\n")
        print("1) register\n")
        print("2) login (Enter it as \"login url\")\n")
        print("3) list \n")
        print("4) rate (Enter it as \"rate professor_id module_code year semester rating \", where rating is between 1-5)\n")
        print("5) view \n")
        print("6) average (Enter it as \"average professor_id module_code\")\n")
        print("7) logout\n")
        print("8) quit\n")
        
        if len(key) == 0:
            command = input("\n(not logged in)\nEnter a command : ")
        else:
            command = input("\n("+ usrname +")\nEnter a command : ")

        
        user_command_split = command.split(" ")
        if user_command_split[0].lower() == "register":
            register_user()

        elif user_command_split[0].lower() == "login":
            try:
                url = user_command_split[1]
                l = login_user(key, url)
                key = l['key']
                usrname = l['usrname']
                
            except IndexError:
                print("Please enter a url to login to")

        elif user_command_split[0].lower() == "list":
            lists(key)

        elif user_command_split[0].lower() == "logout":
            l = logout_user(key)
            key = l['key']
            usrname = l['usrname']

        elif user_command_split[0][0:4].lower() == "rate" and len(user_command_split) == 6:
            rate(key,command)

        elif user_command_split[0].lower() == "view":
            view(key)

        elif user_command_split[0].lower() == "average" and len(user_command_split) == 3 :
            average(key,command)

        elif user_command_split[0].lower() == "quit":
            break

        else:
            print("\nInvalid option\n")
        


if __name__ == '__main__':
    main()
