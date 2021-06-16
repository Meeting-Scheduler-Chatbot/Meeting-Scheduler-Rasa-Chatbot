# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
import pymongo
from pprint import pprint
import requests
import datetime
from datetime import timedelta
import numpy as np
import timeit

from typing import Dict, Text, Any, List, Union, Optional

from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
from rasa_sdk import Action
from rasa_sdk.events import SlotSet
from rasa.core.channels.channel import InputChannel, OutputChannel, UserMessage
from rasa.core.channels.hangouts import HangoutsInput
import spacy

import en_core_web_md
nlp = en_core_web_md.load()

# ​nlp = spacy.load("en")
doc = nlp("30 minutes")

print(doc.ents[0].text, type(doc.ents[0].text))


TIME_DELTA = 0
noon = "12-13"
workingTimes = "8-23"

API = "http://localhost:8080/api"
TOKEN = ""

def get_token_from_email(email):
    # req at tokeni esitle.
    sec_key = "amazing_pass"

    res = requests.post(
        'http://localhost:8080/auth/login',
        data={
            "email": email,
            "password": sec_key
        },
    )
    return res.json()["token"]


def findSlotMapReference(duration, stride, day):
    chunkList = []
    startEndWorkingTimes = workingTimes.split("-")
    startEndNoonTimes = noon.split("-")

    startWorkingTime = datetime.time(int(startEndWorkingTimes[0]))
    endWorkingTime = datetime.time(int(startEndWorkingTimes[1]))
    startNoonTime = datetime.time(int(startEndNoonTimes[0]))
    endNoonTime = datetime.time(int(startEndNoonTimes[1]))

    # print("®"*50, day, startWorkingTime, day.time(), sep="\n")

    if startWorkingTime > day.time():
        start = datetime.datetime.combine(day.date(), startWorkingTime)
    else:
        start = day

    s = start
    e = start + datetime.timedelta(seconds=60 * duration)
    while e.time() <= endWorkingTime:
        if s.time() >= endNoonTime or e.time() <= startNoonTime:
            chunkList.append((s, e))
        s = s + datetime.timedelta(seconds=60 * stride)
        e = e + datetime.timedelta(seconds=60 * stride)
    #print(chunkList)
    return chunkList

def getAllFutureEvents(peopleList, token):
    res = requests.post('http://localhost:8080/api/googleSecure/schedule',
                        data={
                            "memberList": peopleList
                        },
                        headers={
                                'Authorization': "Bearer " + token,
                        },
                    )

    # print(res)
    # print(res.json())
    # print(res.json()["data"])
    return res.json()["data"]


def schedule (memberList, token, meetingDuration):
    start = timeit.default_timer() 
    UserEvents = getAllFutureEvents(memberList, token)

    stop = timeit.default_timer()
    print("Request Time:", (stop-start))
    
    # {"Gokberk": [ [s,e] [s,e]  sorted by s }

    start = timeit.default_timer() 
    #SlotMapReference = findSlotMapReference(meetingDuration, 1, datetime.datetime.fromisoformat((datetime.datetime.strptime(begin, '%Y-%m-%d %H:%M')-timedelta(hours=TIME_DELTA)).isoformat()))
    
    SlotMapReference = findSlotMapReference(meetingDuration, 1, datetime.datetime.now())
    days_to_check = 5
    for day in range(1, days_to_check):
        SlotMapReference += findSlotMapReference(meetingDuration, 1, (datetime.datetime.now() + datetime.timedelta(days=day)) - datetime.timedelta(hours = datetime.datetime.now().hour))
    
    stop = timeit.default_timer()
    # print(SlotMapReference)
    print("Chunk Create Time:", stop-start)
    # possibleSlotReference = [[start, end], [start,end],...]
    # print(SlotMapReference)
    
    start = timeit.default_timer() 
    n =  len(UserEvents) # number of user
    k =  len(SlotMapReference) # chunck size
    # print(n)
    # print(k)
    allFreeSlotMap= np.ones((n,k), dtype = np.int8)
    # = [[0,0,0,0...],[0,0,0,0,0,0,0]....]
    
    index = -1 # used to reference allFreeSlotMap for the user's index
    # print("€€€€€€€€€€€€€€€€€€€€€€€€€€€", UserEvents)
    for user, userMap in UserEvents.items():
        index +=1 
        for event in userMap:
            s = event[0]
            e = event[1]
            # print("-"*50)
            # print("event: ",user , event)
            # print("s: ", s)
            # print("e: ", e)
            # print("-"*50)
            s = datetime.datetime.fromisoformat((datetime.datetime.strptime(s[:-9], '%Y-%m-%dT%H:%M')-timedelta(hours=TIME_DELTA)).isoformat())
            e = datetime.datetime.fromisoformat((datetime.datetime.strptime(e[:-9], '%Y-%m-%dT%H:%M')-timedelta(hours=TIME_DELTA)).isoformat())
            for slotIndex, slotReference in enumerate(SlotMapReference):
                sR =  slotReference[0]
                eR =  slotReference[1]
                if  (s >= sR and s <= eR) or (e >= sR and e <= eR) or (sR >= s and sR <= e) or (eR >= s and eR <= e):
                    allFreeSlotMap[index,slotIndex] = 0
                    # gives matchings (cakismalar)

    numPersonAvailable = np.sum(allFreeSlotMap,axis=0)
    stop = timeit.default_timer()
    print("Scheduling Algorithm Time:", stop-start)

    #allPossibleAnswers = [ str(y[0])[11:] + " - " + str( y[1])[11:] for x, y in zip(numPersonAvailable, SlotMapReference) if x == n ]
    allPossibleAnswers = [ [y[0].isoformat() , y[1].isoformat()] for x, y in zip(numPersonAvailable, SlotMapReference) if x == n ]
    if allPossibleAnswers:
        print(allPossibleAnswers[0])
        return allPossibleAnswers[0]
    else:
        return "there is no possible time to meet!!!"
    #return [ str(y[0]) + " - " + str( y[1]) for x, y in zip(numPersonAvailable, SlotMapReference) if x == n ]

def db_groups_to_mails(group_name, token):
    group_id = ""
    for each in groups:
        if(each.get("name") == group_name):
            group_id = each.get("_id")
    url = API + "/group/members"
    headers={'Authorization': "Bearer " + token}
    body = {"groupId": group_id}
    r = requests.post(url = url, headers = headers, data = body) 
    data = r.json() 
    group_members = []
    user_ids = []
    for each in data["data"][0]["memberNames"]:
        group_members.append(each["email"])
        user_ids.append(each["_id"])
    return group_members


def db_groups_to_mails_new(group_name, token):
    group_id = ""
    for each in groups:
        if(each.get("name") == group_name):
            group_id = each.get("_id")
    url = API + "/group/members"
    headers={'Authorization': "Bearer " + token}
    body = {"groupId": group_id}
    r = requests.post(url = url, headers = headers, data = body) 
    data = r.json() 
    group_members = []
    user_ids = []
    for each in data["data"][0]["memberNames"]:
        group_members.append(each["email"])
        user_ids.append(each["_id"])
    return group_members, user_ids

groups = []
def db_get_groups(token):
    url = API + "/group/my_groups"
    headers={'Authorization': "Bearer " + token}
    r = requests.get(url = url, headers = headers) 
    data = r.json() 
    group_names = []
    for each in data.get("data"):
        groups.append(each)
        group_names.append(each.get("name"))
    return group_names

def db_get_users(token):
    url = API + "/company/all_members"
    headers={'Authorization': "Bearer " + token}
    r = requests.get(url = url, headers = headers) 
    data = r.json() 
    print("DATAAA", data)
    usermails = []
    for each in data.get("data"):
        usermails.append(each.get("email"))
    print(usermails)
    return usermails

def db_get_users_new(token):
    url = API + "/company/all_members"
    headers={'Authorization': "Bearer " + token}
    r = requests.get(url = url, headers = headers) 
    data = r.json() 
    print("DATAAA", data)
    usermails = []
    user_ids = []
    for each in data.get("data"):
        usermails.append(each.get("email"))
        user_ids.append(each.get("_id"))
    print(usermails)
    return usermails, user_ids

def extract_groups(each_value,list_of_groups,seen_before,token,list_of_mails,list_of_ids, dispatcher):
    if each_value not in seen_before:
        seen_before.append(each_value)
        if each_value not in db_get_groups(token):
            dispatcher.utter_message(each_value + " is not in the database")
        else:
            list_of_groups.append(each_value)
            mails, user_ids = db_groups_to_mails_new(each_value, token)

            for each in mails:
                if each not in list_of_mails:
                    list_of_mails.append(each)

            for each in user_ids:
                if each not in list_of_ids:
                    list_of_ids.append(each)

def extract_mails(each_value, seen_before, token, list_of_mails, list_of_ids, dispatcher):
    if each_value not in seen_before:
        seen_before.append(each_value)
        mails, user_ids = db_get_users_new(token)
        if each_value not in mails:
            dispatcher.utter_message(each_value + " is not in the database")
        else:
            list_of_mails.append(each_value)
            ind = mails.index(each_value)
            list_of_ids.append(user_ids[ind])


class ActionInformDoingScheduling(Action):
    def name(self) -> Text:
        return "action_inform_doing_scheduling"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ):

        dispatcher.utter_message("I am scheduling the meeting, give me a second.")



class ActionScheduleEvent(Action):
    def name(self) -> Text:
        return "action_schedule_event"

    @staticmethod
    def schedule_the_event(list_of_ids, list_of_mails, token, duration, event_name) -> List[Text]:
        scheduled = schedule(list_of_ids, token, duration)
        # print("###########################################################################",list_of_mails)
        # print("T"*50)
        # print(self.request)
        # print(tracker.current_state())
        # print(HangoutsInput._extract_sender(req))
        # print(tracker.sender_id)
        # print(tracker.latest_message)
        # print("T"*50)
        # print("scheduled", scheduled)
        res = requests.post(
            'http://localhost:8080/api/googleSecure/insert_event',
            data={
                "start_time": scheduled[0],
                "end_time": scheduled[1],
                "token": token,
                "attendees_emails": list_of_mails.split(", "),
                "event_name" : event_name
            },
            headers={
                    'Authorization': "Bearer " + token,
            },
        )

        if type(scheduled) == List:
            scheduled = " - ".join(scheduled)
        return scheduled

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ):
    
        #TODO: fix the duration conversion ==> duckling or spacy will solve the problem
        print("-"*55,tracker.get_slot("time"))
        scheduled_time = self.schedule_the_event(
            tracker.get_slot("list_of_ids"), 
            tracker.get_slot("user_mail"), 
            tracker.get_slot("token"), 
            int(tracker.get_slot("duration")), 
            tracker.get_slot("meeting_name")
        )

        return [SlotSet("meeting_scheduled_time", scheduled_time)]
        #dispatcher.utter_message(text=upcoming_events_list[0])


class ActionShowUpcomingEvents(Action):
    def name(self) -> Text:
        return "action_show_upcoming_events"

    @staticmethod
    def upcoming_events_db() -> List[Text]:
        """Database of supported cuisines."""
        return ["yarin 3'te toplantin var"]

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ):
        upcoming_events_list = self.upcoming_events_db()
        dispatcher.utter_message(text=upcoming_events_list[0])


# class ActionAddNewPeopleOrGroupsToMeeting(Action):
#     def name(self) -> Text:
#         return "action_add_new_people_or_groups_to_meeting"

#     # @staticmethod
#     # def group_to_mail_db(group_name) -> List[Text]:
#     #     """Database of supported cuisines."""
#     #     return [
#     #         "2@gmail.com",
#     #         "3@gmail.com",
#     #         "4@gmail.com",
#     #         "5@gmail.com",
#     #         "6@gmail.com",
#     #         "7@gmail.com",
#     #         "8@gmail.com",
#     #     ]

#     def run(
#         self,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any],
#     ):
#         user_info = list()
#         team_list = list()
#         list_of_ids = tracker.get_slot("list_of_ids")

#         if tracker.get_slot("group_name") is not None:
#             team_list = tracker.get_slot("group_name")
#         # print(tracker.latest_message["entities"])
#         for i in tracker.latest_message["entities"]:
#             if i["entity"] == "user_info" and i["value"] not in user_info:
#                 user_info.append(i["value"])
#         if tracker.get_slot("user_mail") is not None:
#             user_mails = tracker.get_slot("user_mail")
#             for each_value in user_info:
#                 if "group_" in each_value and "@" not in each_value:
#                     team_list.append(each_value)
#                     for each in db_groups_to_mails(each_value,TOKEN):
#                         user_mails.append(each)
#                 elif "@" in each_value and "group_" not in each_value:
#                     user_mails.append(each_value)
#                 else:
#                     print("ActionAddNewPeopleOrGroupsToMeeting: ", each_value)

#         dispatcher.utter_message(text="User(s) added")
#         return [SlotSet("user_mail", user_mails), SlotSet("group_name", team_list)]
#         # re ile mail/group cekilebilir


# class ActionAddNewPeopleOrGroupsToMeeting(Action):
#     def name(self) -> Text:
#         return "action_add_new_people_or_groups_to_meeting"
#     def run(
#         self,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any],
#     ):
#         user_info = list()
#         team_list = list()
#         seen_before = list()
#         list_of_ids = tracker.get_slot("list_of_ids")
        
#         if tracker.get_slot("group_name") is not None:
#             team_list = tracker.get_slot("group_name")
        
#         print(tracker.latest_message["entities"])

#         for i in tracker.latest_message["entities"]:
#             if i["entity"] == "user_info" and i["value"] not in user_info:
#                 user_info.append(i["value"])

#         if tracker.get_slot("user_mail") is not None:
#             user_mails = tracker.get_slot("user_mail")
#             seen_before = team_list + user_mails

#             for each_value in user_info:

#                 if (("group_" in each_value) and ("@" not in each_value) and (each_value not in team_list)):
#                 extract_groups(each_value, team_list, seen_before, token, user_mails, list_of_ids)

#                 elif (("@" in each_value) and ("group_" not in each_value) and (each_value not in user_mails)):
#                     extract_mails(each_value, seen_before, token, user_mails, list_of_ids)
                    
#                 elif ((each_value in team_list) or (each_value in user_mails)):
#                     continue
                    
#                 else:
#                     print("ActionAddNewPeopleOrGroupsToMeeting: ", each_value)

#         dispatcher.utter_message(text="User(s) added")
#         return [SlotSet("user_mail", user_mails), SlotSet("group_name", team_list)]
#         # re ile mail/group cekilebilir







# class ActionRemovePeopleOrGroupsFromMeeting(Action):
#     def name(self) -> Text:
#         return "action_remove_people_or_groups_from_meeting"

#     # @staticmethod
#     # def group_to_mail_db(group_name) -> List[Text]:
#     #     """Database of supported cuisines."""
#     #     return [
#     #         "IT@gmail.com",
#     #         "IK@gmail.com",
#     #         "Appa@gmail.com",
#     #         "OLAAAY@gmail.com",
#     #         "CAVIT@gmail.com",
#     #         "Steph@gmail.com",
#     #         "Elma@gmail.com",
#     #     ]

#     def run(
#         self,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any],
#     ):
#         TOKEN = get_token_from_email(tracker.sender_id)
#         user_info = list()
#         team_list = list()
#         # print(tracker.activeloop)
#         if tracker.get_slot("group_name") is not None:
#             team_list = tracker.get_slot("group_name")
#         # print(tracker.latest_message["entities"])
#         print(tracker.get_latest_entity_values("user_info"))
#         # get_token_from_email(tracker.get_latest_entity_values("user_info"))
#         for i in tracker.latest_message["entities"]:
#             if i["entity"] == "user_info" and i["value"] not in user_info:
#                 user_info.append(i["value"])
#         if tracker.get_slot("user_mail") is not None:
#             user_mails = tracker.get_slot("user_mail")
#             for each_value in user_info:
#                 if (
#                     "group_" in each_value
#                     and "@" not in each_value
#                     and each_value in team_list
#                 ):
#                     team_list.remove(each_value)
#                     for each in db_groups_to_mails(each_value,TOKEN):
#                         user_mails.remove(each)
#                 elif (
#                     "@" in each_value
#                     and "group_" not in each_value
#                     and each_value in user_mails
#                 ):
#                     user_mails.remove(each_value)
#                 else:
#                     print("ActionRemovePeopleOrGroupsFromMeeting:", each_value)
#         if user_mails == []:
#             dispatcher.utter_message(
#                 text="Nobody left in the meeting, please add people"
#             )
#         else:
#             dispatcher.utter_message(text="User(s) removed")
#         return [SlotSet("user_mail", user_mails), SlotSet("group_name", team_list), SlotSet("token", TOKEN)]


class ValidateScheduleMeetingForm(FormValidationAction):
    """Example of a form validation action."""

    def name(self) -> Text:
        return "validate_schedule_meeting_form"

    # async def required_slots(
    #     self,
    #     slots_mapped_in_domain: List[Text],
    #     dispatcher: "CollectingDispatcher",
    #     tracker: "Tracker",
    #     domain: "DomainDict",
    # ) -> Optional[List[Text]]:
    #     required_slots = slots_mapped_in_domain + ["user_info"]
    #     return required_slots

    # @staticmethod
    # def groups_db() -> List[Text]:
    #     """Database of supported cuisines."""

    #     return [
    #         "group_IT",
    #         "group_IK",
    #         "group_Appa",
    #         "group_OLAAAY",
    #         "group_CAVIT",
    #         "group_Steph",
    #         "group_Elma",
    #     ]

    # @staticmethod
    # def group_to_mail_db(group_name) -> List[Text]:
    #     """Database of supported cuisines."""
    #     return [
    #         "IT@gmail.com",
    #         "IK@gmail.com",
    #         "Appa@gmail.com",
    #         "OLAAAY@gmail.com",
    #         "CAVIT@gmail.com",
    #         "Steph@gmail.com",
    #         "Elma@gmail.com",
    #     ]

    # def validate_group_name(  # List aliyor ama text yaziyor xd (ps. calisiyo)
    #     self,
    #     value: Text,
    #     dispatcher: CollectingDispatcher,
    #     tracker: Tracker,
    #     domain: Dict[Text, Any],
    # ) -> Dict[Text, Any]:
    #     """Validate cuisine value."""
    #     token = get_token_from_email(tracker.sender_id)

    #     if isinstance(value, str):
    #         value = [value]

    #     values = list()

    #     print("validate_group_name:", value)
    #     for v in value:
    #         if v in db_get_groups(token):
    #             values.append(db_groups_to_mails(v, token))
    #         else:
    #             dispatcher.utter_message(template="utter_wrong_group_name")
    #             return {"group_name": None}
    #     return {"group_name": values, "token": token}

    def validate_duration( 
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:

        print(value)
        print(tracker.latest_message)
        for entity in tracker.latest_message["entities"]:
            if entity["entity"] == 'duration': 
                return {
                    "duration": entity["additional_info"]["normalized"]["value"] / 60
                }   
        return {"duration": None}

         
        

    def validate_time( 
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:

        print(value)
        print(tracker.latest_message)

         
        return {
            "time": value,
        }


    def validate_user_info(  # List aliyor ama text yaziyor xd (ps. calisiyo)
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:

        token = get_token_from_email(tracker.sender_id)

        if isinstance(value, str):
            value = [value]
        # print(value)

        list_of_mails = list()
        list_of_groups = list()
        seen_before = list()
        list_of_ids = list()

        for each_value in value:
            if (("group_" in each_value) and ("@" not in each_value) and (each_value not in list_of_groups)):
                extract_groups(each_value, list_of_groups, seen_before, token, list_of_mails, list_of_ids, dispatcher)

            elif (("@" in each_value) and ("group_" not in each_value) and (each_value not in list_of_mails)):
                extract_mails(each_value, seen_before, token, list_of_mails, list_of_ids, dispatcher)
                
            elif ((each_value in list_of_groups) or (each_value in list_of_mails)):
                continue

            else:
                print("validate_user_info:", each_value)

        if len(list_of_mails) == 0 or len(list_of_ids) == 0:
            value = None

        print("USERIDS", list_of_ids)
        print("user_mail", list_of_mails)
        print("group_name", list_of_groups)

        str_list_of_mails = ", ".join(list_of_mails)
        str_list_of_groups = ", ".join(list_of_groups)
        
        return {
            "user_info": value,
            "user_mail": str_list_of_mails,
            "group_name": str_list_of_groups,
            "list_of_ids": list_of_ids,
            "token": token,
        }
