import json
import requests
import sys
import re

def register():
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
        r = requests.post('http://127.0.0.1:8000/api/register/', data = PARAMS )
        r = r.json()
        string = r['phrase']
        print(string)
    else:
        print("\nSorry!! Invalid values detected. Ensure :\n1) Your username is minimum length 3 and is alpha numeric.\n2) Passwords match and are also minimum length 6.\n3) Your email is valid.\n")

def login(key):
    print("\n")
    username = input("Enter your username : ")
    print("\n")
    pswd = input("Enter your password : ")
    print("\n")

    PARAMS = {'usrname' : username, 'pass' : pswd}
    r = requests.post('http://127.0.0.1:8000/api/login/', data = PARAMS )
    r = r.json()
    phrase = r['phrase']
    key = r['token']
    usrname = r['usrname']
    print(phrase)
    returnlist = {'key' : key, 'usrname' : usrname}
    return returnlist

def logout(key):
    if key == "":
        phrase = notLoggedIn()
        key = ""
        return key
    else:
        headers = {'Authorization': key}
        r = requests.get('http://127.0.0.1:8000/api/logout/', headers = headers)
        r = r.json()
        phrase = r['phrase']
        key = r['token']
        usrname = r['usrname']
        print(phrase)
        returnlist = {'key' : key, 'usrname' : usrname}
        return returnlist


def lists(key):
    headers = {'Authorization': key}
    r = requests.get('http://127.0.0.1:8000/api/list', headers = headers)
    if r.status_code == 200:
        r = r.json()
        li = []
        print("\n" + "Module ID" + "     " + "Module name" + "     " + "Semester" + "     " + "Year" + "     " + "Teacher ID" +"\n")
        for i in r['phrase']:
            li.append(i)
        x = len(li)
        for i in range(x):
            phrase = "\n" + str(li[i]['ID']) + "     " + str(li[i]['name']) + "     " + str(li[i]['sem']) + "     " + str(li[i]['year']) + "     " + str(li[i]['tc']) +"\n"
            print(phrase)
    else:
        r = r.json()
        print(notLoggedIn())


def rate(key, command):
    headers = {'Authorization': key}
    data = {"teach_ID" : command.split(" ")[1], "mod_ID" : command.split(" ")[2], "year" : command.split(" ")[3], "semester" : command.split(" ")[4], "rate" : command.split(" ")[5]}
    r = requests.post('http://127.0.0.1:8000/api/rate/', headers = headers, data = data)
    if r.status_code == 200:
        r = r.json()
        print(r["phrase"])
    elif r.status_code == 403:
        print(notLoggedIn())
    else:
        r = r.json()
        print(r["phrase"])

def view(key):
    headers = {'Authorization': key}
    r = requests.get('http://127.0.0.1:8000/api/view/', headers = headers)
    if r.status_code == 200:
        r = r.json()
        li = []
        for i in r['phrase']:
            li.append(i)
        for i in range(len(li)):
            string = "\n" + "The rating of Professor "+ li[i]['name'] +" is " + str(li[i]['Rating']) + "\n"
            print(string)
    else:
        r = r.json()
        print(notLoggedIn())

def average(key, command):
    print("\n")
    headers = {'Authorization': key}
    data = {"teach_ID" : command.split(" ")[1], "mod_ID" : command.split(" ")[2]}
    r = requests.get('http://127.0.0.1:8000/api/average/', headers = headers, data = data)
    if r.status_code == 200:
        r = r.json()
        phrase = "\nThe rating of Professor " + r["phrase"]['name'] + " in module " + r["phrase"]['module_n'] + " " + r["phrase"]['modid'] + " is " +  str(r["phrase"]['Rating']) + "\n"
        print(phrase)
    elif r.status_code == 403:
        print(notLoggedIn())
    else:
        r = r.json()
        print(r["phrase"])

def notLoggedIn():
    return ("\nYou are not logged in!!!. \nLog in first!!!!!!\n")

def main():
    key = ""
    usrname = ""
    while True:
        print("=======================================================================================================")
        print("Please enter a command:\n")
        print("1) register (Enter it as \"register\")\n")
        print("2) login (Enter it as \"login\")\n")
        print("3) list (Enter it as \"list\")\n")
        print("4) rate (Enter it as \"rate professor_id module_code year semester rating \", where rating is between 1-5)\n")
        print("5) view (Enter it as \"view\")\n")
        print("6) average (Enter it as \"average professor_id module_code\")\n")
        print("7) logout\n")
        print("8) quit\n")
        
        if len(key) == 0:
            command = input("\n(not logged in)\nEnter an option : ")
        else:
            command = input("\n("+ usrname +")\nEnter an option : ")

        
        user_command_split = command.split(" ")
        if user_command_split[0].lower() == "register":
            register()
        elif user_command_split[0].lower() == "login":
            # url = user_command_split[1]
            l = login(key)
            key = l['key']
            usrname = l['usrname']

        elif user_command_split[0].lower() == "list":
            lists(key)

        elif user_command_split[0].lower() == "logout":
            l = logout(key)
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
