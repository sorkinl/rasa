import random
from typing import Any, Text, Dict, List

from rasa_sdk.forms import FormValidationAction, ActiveLoop
from rasa_sdk import Action, Tracker
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk.events import ConversationResumed
from rasa_sdk.events import ConversationPaused
from rasa_sdk.events import UserUttered
from rasa.shared.nlu.training_data.message import Message


def getCapitalizedElement(arr):
    nameArr = []
    for x in arr:
        if(x[0].isupper() and len(x) > 1):
            nameArr.append(x)
    return nameArr


def getTimeElement(arr):
    timeArr = []
    for x in arr:
        if(x[0].isdigit() and len(x) > 1):
            timeArr.append(x + "утра")
            timeArr.append(x + "вечера")
    return timeArr


def listToString(arr):
    # initialize an empty string
    str1 = ""

    # traverse in the string
    for ele in arr:

        str1 += ele + ", "

    # return string
    return str1.strip(', ')


def makeButton(name):
    return {"title": name,
            "payload": name
            }


def randomTimes():
    i = 0
    arr = []
    while i < 5:
        arr.append(str(random.randint(1, 12)) + ":00 PM")
        i += 1

    return arr


class ActionHandleProvidedInfo(Action):
    def name(self) -> Text:
        return "action_handle_provided_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        name = tracker.get_slot('PER')
        time = tracker.get_slot('time')

        last_message = tracker.latest_message["text"]

        # if name and location are provided, show
        # the user further options

        if name and time:
            print("Nothing needed")

        # if valid information isn't provided,
        # ask the user for the information
        # again.
        elif name:
            predicted_times = getTimeElement(last_message.split())
            dispatcher.utter_message(text="Invalid data 1a.")
            print(predicted_times)
            print(listToString(predicted_times))
            title = "Is your name one of these: " + listToString(predicted_times) + \
                " ? If not type your name below." if len(
                    predicted_times) != 0 else "I didn't find any time can you choose one of the following when prof is available?"
            print(title)
            times = predicted_times if len(
                predicted_times) != 0 else randomTimes()
            buttons = map(makeButton, times)
            dispatcher.utter_message(
                text=title, buttons=buttons)

        else:
            predicted_names = getCapitalizedElement(last_message.split())
            dispatcher.utter_message(text="Invalid data 1b.")
            print(predicted_names)
            print(listToString(predicted_names))
            title = "Is your name one of these: " + listToString(predicted_names) + \
                " ? If not type your name below." if len(
                    predicted_names) != 0 else "I didn't find any name type your name below or I'll call you Leo"
            print(title)
            buttons = map(makeButton, predicted_names)
            dispatcher.utter_message(
                text=title, buttons=buttons)

        return []


class ActionConfirmName(Action):
    def name(self):
        return "action_confirm_name"

    async def run(self, dispatcher, tracker, domain):
        print("Confirm name")
        message = tracker.latest_message["text"]

        return [SlotSet("PER", message)]


class ActionGiveDiagnosis(Action):
    def name(self):
        return "action_give_diagnosis"

    async def run(self, dispatcher, tracker, domain):
        print("Give diagnosis")
        fever = tracker.get_slot("fever")
        sick = tracker.get_slot("sick")
        headache = tracker.get_slot("headache")
        throat = tracker.get_slot("throat")
        nose = tracker.get_slot("nose")
        if(fever == "True"):
            dispatcher.utter_message(text="У вас грипп")
        else:
            if(sick == "True"):
                dispatcher.utter_message(text="У вас аллергия")
            else:
                dispatcher.utter_message(text="У вас простуда")
        return []
