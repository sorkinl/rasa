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
    for ele in str1:

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
        print('In ActionHandleProvidedInfo!')
        name = tracker.get_slot('name')
        time = tracker.get_slot('time')

        last_message = tracker.latest_message["text"]

        # if name and location are provided, show
        # the user further options

        # if name and time:
        #     dispatcher.utter_message(
        #         text="From out custom action ActionHandleProvidedInfo - Thanks for tell me about your trip " + name + "."
        #         "I'll think about going to " + time + " next time."
        #     )
        # dispatcher.utter_message(buttons=buttons)

        # if valid information isn't provided,
        # ask the user for the information
        # again.
        if name:
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
            # return [FollowupAction("action_confirm_name")]
            # Trigger Action_Confirm_Name with the value from buttons or text

        return []


# class ActionDefaultAskAffirmation(Action):
#     def name(self):
#         return "action_default_ask_affirmation"

#     async def run(self, dispatcher, tracker, domain):

#         print("Action running")
#         # select the top three intents from the tracker
#         # ignore the first one -- nlu fallback
#         predicted_intents = tracker.latest_message["intent_ranking"][1:4]
#     # A prompt asking the user to select an option
#         message = "Sorry! What do you want to do?"
#     # a mapping between intents and user friendly wordings
#         intent_mappings = {
#             "inform_time": "Time pls",
#             "inform_name": "Name pls",
#             "affirm": "Yes",
#             "goodbye": "End conversation",
#             "out_of_scope": "None of these",
#             "faq": "Frequently asked questions",
#             "bot_challenge": "Am I a bot?",
#             "ask_features": "Features",
#             "request_appointment": "appointment request",
#             "greet": "hi",
#             "deny": "no",
#             "mood_great": "Mood",
#             "mood_unhappy": " No happy",
#             "gratitude": "thanks bro",
#             "confirm_name": "Yep that's my name",
#             "inform_reason": "That's the reason"


#         }
#         # tracker.latest_message['intent'].get('name'))
#         # https://rasa.com/docs/rasa/forms/#writing-stories--rules-for-unhappy-form-paths
#         #SlotSet("name", "Leo")
#         print(tracker.latest_action_name, "action name")
#         print(tracker.latest_message['intent'], "intent")
#         print(tracker.latest_message['entities'], "entities")
#         print(tracker.latest_message['text'], "text")
#         print(tracker.slots, "slots")
#     # show the top three intents as buttons to the user
#         buttons = [
#             {
#                 "title": intent_mappings[intent['name']],
#                 "payload": "/{}".format(intent['name'])
#             }
#             for intent in predicted_intents
#         ]
#     # add a "none of these button", if the user doesn't
#         # agree when any suggestion
#         buttons.append({
#             "title": "Different Name",
#             "payload": "/greet"
#         })
#         if(tracker.slots["name"] == None):
#             print("Utter confirm name")
#             dispatcher.utter_message(response="utter_сonfirm_name")
#         else:
#             dispatcher.utter_message(text=message, buttons=buttons)
#         # dispatcher.utter_message(response="utter_greet")

#         return [ActiveLoop(None)]

# Message.set("intent", { "name": "inform_location"}, add_to_output=True)


class ActionConfirmName(Action):
    def name(self):
        return "action_confirm_name"

    async def run(self, dispatcher, tracker, domain):
        print("Confirm name")
        message = tracker.latest_message["text"]

        return [SlotSet("name", message)]


# a mapping between intents and user friendly wordings
    # intent_mappings = {
    # "inform_location": "Inform location - Where did you go exactly?  Give me a name like Paris or China.",
    # "inform_reason_trip": "Inform reason",
    # "inform_time": "Inform time",
    # "inform_name": "Inform name",
    # "mood_great": "Great mood",
    # "ask_features": "Ask features",
    # "affirm": "Agree",
    # "deny": "Disagree",
    # "goodbye": "End conversation"
    # }

# show the top three intents as buttons to the user
    # buttons = [
    # {
    # "title": intent_mappings[intent['name']],
    # "payload": "/{}".format(intent['name'])
    # }
    # for intent in predicted_intents
    # ]

# add a "none of these button", if the user doesn't
    # agree when any suggestion
    # buttons.append({
    # "title": "None of These",
    # "payload": "/out_of_scope"
    # })
