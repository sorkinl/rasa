from typing import Any, Text, Dict, List

from rasa_sdk.forms import FormValidationAction, ActiveLoop
from rasa_sdk import Action, Tracker
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.events import ConversationResumed
from rasa_sdk.events import ConversationPaused
from rasa_sdk.events import UserUttered
from rasa.shared.nlu.training_data.message import Message


def getCapitalizedElement(arr):
    for x in arr:
        if(x[0].isupper() and len(x[0]) != 1):
            return x
    return None


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

        if name and time:
            dispatcher.utter_message(
                text="From out custom action ActionHandleProvidedInfo - Thanks for tell me about your trip " + name + "."
                "I'll think about going to " + time + " next time."
            )
            # dispatcher.utter_message(buttons=buttons)

        # if valid information isn't provided,
        # ask the user for the information
        # again.
        elif name:
            dispatcher.utter_message(text="Invalid data 1a.")
            dispatcher.utter_message(response="utter_ask_for_time")

        elif time:
            predicted_name = getCapitalizedElement(last_message.split())
            dispatcher.utter_message(text="Invalid data 1b.")
            title = "Is your name: " + predicted_name + \
                " ? If not type your name below." if predicted_name else "I didn't find any name type your name below or I'll call you None"
            buttons = [
                {
                    'title': title,
                    'payload': '/action_handle_provided_info'
                },
            ]
            dispatcher.utter_message(
                text="Click the button below", buttons=buttons)
            # dispatcher.utter_message(response="utter_ask_for_name")
            SlotSet("name", predicted_name)

        return []


class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(self, dispatcher, tracker, domain):
        # output a message saying that the conversation will now be
        # continued by a human.

        # message = "Sorry, couldn't understand that! Let me connect you to a human..."
        # dispatcher.utter_message(text=message)

        # pause tracker
        # undo last user interaction
        # return [ConversationPaused(), UserUtteranceReverted()]
        print('In ActionDefaultFallback!')

        name = tracker.get_slot('name')
        time = tracker.get_slot('time')
        print(name, time)
        if name and time:
            dispatcher.utter_message(
                text="From out custom action ActionDefaultFallback - Thanks for tell me about your trip " + name + "."
                "I'll think about going to " + time + " next time."
            )
            # dispatcher.utter_message(buttons=buttons)

        # if valid information isn't provided,
        # ask the user for the information
        # again.
        elif name:
            # dispatcher.utter_message(text="Invalid data 2a.")
            dispatcher.utter_message(response="utter_ask_for_location")

        elif time:
            dispatcher.utter_message(text="Invalid data 2b.")
            dispatcher.utter_message(response="utter_ask_for_name")

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

        dispatcher.utter_message(response="appointment_form")
        return [ActiveLoop("appointment_form"), SlotSet("name", message)]


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
