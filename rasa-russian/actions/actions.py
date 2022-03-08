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


class ActionDefaultAskAffirmation(Action):
    def name(self):
        return "action_default_ask_affirmation"

    async def run(self, dispatcher, tracker, domain):

        print("Action running")
        # select the top three intents from the tracker
        # ignore the first one -- nlu fallback
        predicted_intents = tracker.latest_message["intent_ranking"][1:4]
    # A prompt asking the user to select an option
        message = "Sorry! What do you want to do?"
    # a mapping between intents and user friendly wordings
        intent_mappings = {
            "inform_time": "Time pls",
            "inform_name": "Name pls",
            "affirm": "Yes",
            "goodbye": "End conversation",
            "out_of_scope": "None of these",
            "faq": "Frequently asked questions",
            "bot_challenge": "Am I a bot?",
            "ask_features": "Features",
            "request_appointment": "appointment request",
            "greet": "hi",
            "deny": "no",
            "mood_great": "Mood",
            "mood_unhappy": " No happy",
            "gratitude": "thanks bro",
            "confirm_name": "Yep that's my name",
            "inform_reason": "That's the reason"


        }
        # tracker.latest_message['intent'].get('name'))
        # https://rasa.com/docs/rasa/forms/#writing-stories--rules-for-unhappy-form-paths
        #SlotSet("name", "Leo")
        print(tracker.latest_action_name, "action name")
        print(tracker.latest_message['intent'], "intent")
        print(tracker.latest_message['entities'], "entities")
        print(tracker.latest_message['text'], "text")
        print(tracker.slots, "slots")
    # show the top three intents as buttons to the user
        buttons = [
            {
                "title": intent_mappings[intent['name']],
                "payload": "/{}".format(intent['name'])
            }
            for intent in predicted_intents
        ]
    # add a "none of these button", if the user doesn't
        # agree when any suggestion
        buttons.append({
            "title": "Different Name",
            "payload": "/greet"
        })
        # if(tracker.slots["name"] == None):
        #     dispatcher.utter_message(response="utter_confirm_name")
        # else:
        #     dispatcher.utter_message(text=message, buttons=buttons)
        dispatcher.utter_message(response="utter_greet")

        return [ActiveLoop(None), SlotSet("name", "Leo")]

#Message.set("intent", { "name": "inform_location"}, add_to_output=True)


class ActionConfirmName(Action):
    def name(self):
        return "action_confirm_name"

    async def run(self, dispatcher, tracker, domain):
        message = tracker.latest_message["text"]

        dispatcher.utter_message(response="request_appointment")
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
