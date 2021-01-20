from __future__ import print_function
import pickle as pkl
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from collections import defaultdict
import geocoder
import re
import time



class User:

    def __init__(self,username=None,password=None):

        try:
            self.IndividualContactList = pkl.load(open(r"C:\college\Github_improvement\Covid Alert\IndividualContactList.pkl","rb"))
        except:
            self.IndividualContactList = None
        try:
            self.FriendSuggesterList = pkl.load(open(r"C:\college\Github_improvement\Covid Alert\FriendSuggesterList.pkl","rb"))
        except:
            self.FriendSuggesterList = None
        try:
            self.MutualContactList = pkl.load(open(r"C:\college\Github_improvement\Covid Alert\MutualContactList.pkl","rb"))
        except:
            self.MutualContactList = None
        try:
            self.CentralPhoneDir = pkl.load(open(r"C:\college\Github_improvement\Covid Alert\CentralPhoneDir.pkl","rb"))
        except:
            self.CentralPhoneDir = None
        try:
            self.FriendList = pkl.load(open(r"C:\college\Github_improvement\Covid Alert\FriendList.pkl","rb"))
        except:
            self.FriendList = None

        if username!=None and password!=None:
            self.username = username
            self.password = password
            try:
                self.RegisteredUsersDB = pkl.load(open(r"C:\college\Github_improvement\Covid Alert\RegisteredUsersDB.pkl","rb"))
            except:
                self.RegisteredUsersDB = None
            self.check()
        else:
            print("The username or password is empty!")

    def check(self):
        if self.RegisteredUsersDB!=None:
            if self.username in self.RegisteredUsersDB and self.RegisteredUsersDB[self.username]==self.password:
                print("Successfully Logged in!")
            else:
                choice = input("Incorrect username or password!! Do you want to register?(y/n): ")
                if choice.lower()=="y" or choice.lower()=="yes":
                    self.register()
                else:
                    print("Thanks for using our platform!")
                    return 
        else:
            choice = input("No userDatabase Found!! Do you want to register?(y/n): ")
            if choice.lower()=="y" or choice.lower()=="yes":
                self.register()
            else:
                print("Thanks for using our platform!")
                return 

    def FindLocation(self):
        g = geocoder.ip('me')
        lat,lon = g.latlng[0], g.latlng[1]
        return lat,lon

    def register(self):    
        FirstName = input("Enter your first name: ")
        LastName = input("Enter your last name: ")
        username = input("Enter your username: ")
        if self.RegisteredUsersDB!=None:
            while username in self.RegisteredUsersDB['Users']:
                print("The username is already registered! enter a different username!")
                username = input("Enter your username: ")
        lat,lon = self.FindLocation()
        password = input("Enter your password: ")
        passwordCheck = input("Enter your password again: ")
        while(password != passwordCheck):
            print("the passwords dont match!")
            password = input("Enter your password: ")
            passwordCheck = input("Enter your password again: ")
        covid = False
        PhoneNo = input("Enter your Phone Number: ")
        while(re.match(r"^[1-9]{1}\d{9}$",PhoneNo)==None):
            print("Incorrect Phone Number entered!!")
            PhoneNo = input("Enter your Phone Number: ")

        email = input("Enter your email id: ")
        while(re.match(r"^[a-z0-9]+([\.]\w)*[@]{1}[a-z]+[\.]{1}[a-z]{2,3}$",email)==None):
            print("Enter a valid Email ID!")
            email = input("Enter your email id: ")

        dob = input("Enter your Date of birth(dd/mm/yyyy): ")
        while( re.match(r"^(([0]{1}[1-9]{1}[\/]{1})|([1-2]{1}\d{1}[\/]{1})|([3]{1}[0-1]{1}[\/]{1}))(([0]{1}[1-9]{1}[\/]{1})|([1]{1}[0-2]{1}[\/]{1}))([1-9]{1}\d{3})$",dob)==None):
            print("invalid Email Id! please enter valid ID!")
            dob = input("Enter your Date of birth(dd/mm/yyyy): ")
        ToBeSavedData = {"FirstName": FirstName,"LastName": LastName,"Location":[lat,lon],"Covid":covid,"PhoneNo":PhoneNo,"Email":email,"DOB":dob}
        if self.RegisteredUsersDB!=None:
            self.RegisteredUsersDB["Users"][username] = ToBeSavedData
        else:
            self.RegisteredUsersDB = {}
            final={}
            final[username] = ToBeSavedData
            self.RegisteredUsersDB["Users"] = final
        pkl.dump(self.RegisteredUsersDB,open(r"C:\college\Github_improvement\Covid Alert\RegisteredUsersDB.pkl","wb"))
        self.RegisteredUsersDB = pkl.load(open(r"C:\college\Github_improvement\Covid Alert\RegisteredUsersDB.pkl","rb"))
        if self.CentralPhoneDir!=None:
            self.CentralPhoneDir[PhoneNo] = username
        else:
            self.CentralPhoneDir = {}
            self.CentralPhoneDir[PhoneNo] = username
        self.GetContacts(PhoneNo)

# If modifying these scopes, delete the file token.pickle.

    def GetContacts(self,MyPhoneNumber):
        SCOPES = ['https://www.googleapis.com/auth/contacts.readonly']
        """Shows basic usage of the People API.
        Prints the name of the first 10 connections.
        """
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pkl.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pkl.dump(creds, token)

        service = build('people', 'v1', credentials=creds)

        # Call the People API
        results = service.people().connections().list(
            resourceName='people/me',
            pageSize=1000,
            personFields='names,emailAddresses,phoneNumbers').execute()
        connections = results.get('connections', [])
        phoneDir = {}
        for person in connections:
            
            names = person.get('names', [])
            no = person.get('phoneNumbers', [])
            if names:
                name = names[0].get('displayName')
                for numbers in no:
                    phoneDir[numbers['value']] = name
        if self.IndividualContactList!=None:
            self.IndividualContactList[MyPhoneNumber] = phoneDir
        else:
            self.IndividualContactList = {}
            self.IndividualContactList[MyPhoneNumber] = phoneDir
        pkl.dump(self.IndividualContactList,open(r"C:\college\Github_improvement\Covid Alert\IndividualContactList.pkl","wb"))
        self.IndividualContactList = pkl.load(open(r"C:\college\Github_improvement\Covid Alert\IndividualContactList.pkl","rb"))
        self.AddContactToFriendSuggester(phoneDir,MyPhoneNumber)
    
    def AddContactToFriendSuggester(self, phoneDir,MyPhoneNumber):
        for key,val in phoneDir.items():
            if self.MutualContactList!=None:
                if (key in self.MutualContactList):
                    if (MyPhoneNumber in self.MutualContactList[key]):
                        if self.FriendSuggesterList!=None:
                            self.FriendSuggesterList[key].append(MyPhoneNumber)
                            self.FriendSuggesterList[MyPhoneNumber].append(key)
                        else:
                            self.FriendSuggesterList = defaultdict(list)
                            self.FriendSuggesterList[key].append(MyPhoneNumber)
                            self.FriendSuggesterList[MyPhoneNumber].append(key)
                else:
                    self.MutualContactList[key]={}
                    self.MutualContactList[key][MyPhoneNumber] = 1
            else:
                self.MutualContactList = {}
                self.MutualContactList[key] = {MyPhoneNumber:1}
        pkl.dump(self.FriendSuggesterList,open(r"C:\college\Github_improvement\Covid Alert\FriendSuggesterList.pkl","wb"))
        pkl.dump(self.MutualContactList,open(r"C:\college\Github_improvement\Covid Alert\MutualContactList.pkl","wb"))
        self.FriendSuggesterList = pkl.load(open(r"C:\college\Github_improvement\Covid Alert\FriendSuggesterList.pkl","rb"))
        self.MutualContactList =  pkl.load(open(r"C:\college\Github_improvement\Covid Alert\MutualContactList.pkl","rb"))
        self.NotifyUserAboutSuggestions(MyPhoneNumber)
    
    def NotifyUserAboutSuggestions(self,MyPhoneNumber):

        if self.FriendSuggesterList!=None:
            if MyPhoneNumber in self.FriendSuggesterList and len(self.FriendSuggesterList[MyPhoneNumber])>0:
                for FriendNumber in self.FriendSuggesterList[MyPhoneNumber]:
                    choice = input(self.IndividualContactList[MyPhoneNumber][FriendNumber],", one of your contacts, is now a part of the platform as ",self.CentralPhoneDir[FriendNumber],". Would you like to follow them? (y/n): ")
                    if choice.lower()=="yes" or choice.lower()=="y":
                        username = self.CentralPhoneDir[MyPhoneNumber]
                        FriendUsername = self.CentralPhoneDir[FriendNumber]
                        if self.FriendList!=None:
                            if username in self.FriendList:
                                if FriendUsername not in self.FriendList[username]:
                                    print(FriendUsername," successfully added as your friend!")
                                    self.FriendList[username][FriendUsername] = 1
                                else:
                                    print(FriendUsername," is already your friend!")
                            else:
                                self.FriendList[username] = {}
                                print(FriendUsername," successfully added as your friend!")
                                self.FriendList[username][FriendUsername] = 1
                        else:
                            self.FriendList={}
                            self.FriendList[username] = {}
                            print(FriendUsername," successfully added as your friend!")
                            self.FriendList[username][FriendUsername] = 1     
                    else:
                        pass
                pkl.dump(self.FriendList,open(r"C:\college\Github_improvement\Covid Alert\FriendList.pkl","wb"))
                self.FriendSuggesterList[MyPhoneNumber] = []
            else:
                print("There are no Suggestion for you at present!")
        else:
            print("There are no Suggestion for you at present!")
        return
    
    def NotifyUserAboutCovidAmongFriends(self,username):
        try:
            self.RegisteredUsersDB =  pkl.load(open(r"C:\college\Github_improvement\Covid Alert\RegisteredUsersDB.pkl","rb"))
        except:
            self.RegisteredUsersDB = None
        if self.RegisteredUsersDB!=None:
            AffectedFriends = []
            if self.FriendList[username]:
                for key,val in self.FriendList[username].items():
                    if self.RegisteredUsersDB[key]["Covid"]==True:
                        AffectedFriends.append(key)
            for friend in AffectedFriends:
                print(self.RegisteredUsersDB[friend]["FirstName"]," ",self.RegisteredUsersDB[friend]["LastName"]," one of your friends has been detected COVID positive")
            else:
                print("You dont have any friends. Add friend to check")
        else:
            print("There are no Users at present on this platform!!")
            return 

if __name__ == '__main__':
    User("prathik","pappu")

