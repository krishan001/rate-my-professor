import json
import requests
import sys
import re

# Create your tests here.
def register():
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

    print("\n")
    a = input("Enter a username : ")
    print("\n")
    b = input("Enter your email : ")
    print("\n")
    c = input("Enter a password : ")
    print("\n")
    d = input("Confirm password : ")
    print("\n")

    value1 = re.search(regex,b)
    value2 = c == d and (len(c)>5)
    value3 = a.isalnum() and (len(a)>2)

    if ( value1 and value2 and value3):
        PARAMS = {'uname' : a, 'email' : b, 'passrr' : c}
        r = requests.post('http://127.0.0.1:8000/api/register/', data = PARAMS )
        r = r.json()
        string = r['phrase']
        print(string)
    else:
        print("\n**********************************************************************\n\nSorry!! Invalid values detected. Ensure :\n1) Your username is minimum length 3 and is alpha numeric.\n2) Passwords match and are also minimum length 6.\n3) Your email is valid.\n\n**********************************************************************\n")

def login(key):
    print("\n")
    a = input("Enter your username : ")
    print("\n")
    b = input("Enter your password : ")
    print("\n")

    PARAMS = {'uname' : a, 'passrr' : b}
    r = requests.post('http://127.0.0.1:8000/api/login/', data = PARAMS )
    r = r.json()
    string = r['phrase']
    key = r['token']
    uname = r['uname']
    print(string)
    returnlist = {'key' : key, 'uname' : uname}
    return returnlist

def logout(key):
    print("\n")
    if key == "":
        string = notLoggedIn()
        key = ""
        return key
    else:
        headers = {'Authorization': key}
        r = requests.get('http://127.0.0.1:8000/api/logout/', headers = headers)
        r = r.json()
        string = r['phrase']
        key = r['token']
        uname = r['uname']
        print(string)
        returnlist = {'key' : key, 'uname' : uname}
        return returnlist


def lists(key):
    print("\n")
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
            string = "\n" + str(li[i]['ID']) + "     " + str(li[i]['name']) + "     " + str(li[i]['sem']) + "     " + str(li[i]['year']) + "     " + str(li[i]['tc']) +"\n"
            print(string)
    else:
        r = r.json()
        print(notLoggedIn())


def rate(key, inp):
    print("\n")
    headers = {'Authorization': key}
    data = {"teach_ID" : inp.split(" ")[1], "mod_ID" : inp.split(" ")[2], "year" : inp.split(" ")[3], "semester" : inp.split(" ")[4], "rate" : inp.split(" ")[5]}
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
    print("\n")
    headers = {'Authorization': key}
    r = requests.get('http://127.0.0.1:8000/api/view/', headers = headers)
    if r.status_code == 200:
        r = r.json()
        li = []
        for i in r['phrase']:
            li.append(i)
        x = len(li)
        for i in range(x):
            string = "\n" + "The rating of Professor "+ li[i]['name'] +" is " + str(li[i]['Rating']) + "\n"
            print(string)
    else:
        r = r.json()
        print(notLoggedIn())

def average(key, inp):
    print("\n")
    headers = {'Authorization': key}
    data = {"teach_ID" : inp.split(" ")[1], "mod_ID" : inp.split(" ")[2]}
    r = requests.get('http://127.0.0.1:8000/api/average/', headers = headers, data = data)
    if r.status_code == 200:
        r = r.json()
        string = "\nThe rating of Professor " + r["phrase"]['name'] + " in module " + r["phrase"]['module_n'] + " " + r["phrase"]['modid'] + " is " +  str(r["phrase"]['Rating']) + "\n"
        print(string)
    elif r.status_code == 403:
        print(notLoggedIn())
    else:
        r = r.json()
        print(r["phrase"])

def notLoggedIn():
    return ("\n**********************************************************************\nYou are not logged in!!!. \nLog in first!!!!!!\n**********************************************************************\n")

def main(args=None):
    key = ""
    usrname = ""
    while True:
        print("\n***********************************************************************************\n")
        print("\nWelcome to coursework1 of sc17kdp\n")
        print("Here are your options:\n")
        print("1) register (Enter it as \"register\")\n")
        print("2) login (Enter it as \"login\")\n")
        print("3) list (Enter it as \"list\")\n")
        print("4) rate (Enter it as \"rate professor_id module_code year semester rating \", where rating is between 1-5)\n")
        print("5) view (Enter it as \"view\")\n")
        print("6) average (Enter it as \"average professor_id module_code\")\n")
        print("7) logout\n")
        print("8) quit\n")
        print("\n\n***********************************************************************************\n\n")
        if len(key) == 0:
            inp = input("\n\n(not logged in)\nEnter an option : \n\n")
        else:
            inp = input("\n\n("+ usrname +")\nEnter an option : \n\n")
        if inp.lower() == "register":
            register()
        elif inp.lower() == "login":
            l = login(key)
            key = l['key']
            usrname = l['uname']
        elif inp.lower() == "list":
            lists(key)
        elif inp.lower() == "logout":
            l = logout(key)
            key = l['key']
            usrname = l['uname']
        elif inp[0:4].lower() == "rate" and len(inp.split(" ")) == 6 and (inp.split(" ")[3] == "2017" or inp.split(" ")[3] == "2018" or inp.split(" ")[3] == "2019")and (inp.split(" ")[4] == "1" or inp.split(" ")[4] == "2") and (int(inp.split(" ")[5]) >= 1 and int(inp.split(" ")[5])<= 5):
                rate(key,inp)
        elif inp.lower() == "view":
            view(key)
        elif inp[0:7].lower() == "average" and len(inp.split(" ")) == 3 :
                average(key,inp)
        elif inp.lower() == "quit":
            break
        else:
            print("\n***********************************************************************************\nInvalid option\n***********************************************************************************\n")

if __name__ == '__main__':
    main()
