from typing import Any, Text, Dict, List

from rasa_sdk.forms import FormValidationAction, ActiveLoop
from rasa_sdk import Action, Tracker
#from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.events import ConversationResumed
#from rasa_sdk.events import ConversationPaused
from rasa_sdk.events import UserUttered
from rasa.shared.nlu.training_data.message import Message



#from rasa_sdk import Action, Tracker
#from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, ConversationPaused


class ActionHandleProvidedInfo(Action):
    def name(self):
        return "action_handle_provided_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('In ActionHandleProvidedInfo')
        name = tracker.get_slot('name')
        location = tracker.get_slot('location')

        buttons = [
            {
                'title': "That's all",
                'payload': '/goodbye'
            },
            {
                'title': 'Add More Information',
                'payload': '/supply_location_info'
            },
        ]

        # if name and location are provided, show
        # the user further options

        if name and location:
            dispatcher.utter_message(
                text="Thanks for the information!"\
                    "What would you like to do next1?"
            )
            dispatcher.utter_message(buttons=buttons)
        
        # if valid information isn't provided,
        # ask the user for the information
        # again.
        elif name:
            dispatcher.utter_message(text="Invalid data 1a.")
            dispatcher.utter_message(response="utter_ask_for_location")

        elif location:
            dispatcher.utter_message(text="Invalid data 1b.")
            dispatcher.utter_message(response="utter_ask_for_name")

        return []

class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(self, dispatcher, tracker, domain):
        # output a message saying that the conversation will now be
        # continued by a human.

        #message = "Sorry, couldn't understand that! Let me connect you to a human..."
        #dispatcher.utter_message(text=message)

        # pause tracker
        # undo last user interaction
        #return [ConversationPaused(), UserUtteranceReverted()]
        print('In ActionDefaultFallback')
        name = tracker.get_slot('name')
        location = tracker.get_slot('location')

        if name and location:
            dispatcher.utter_message(
                text="Thanks for the information!"\
                    "What would you like to do next2?"
            )
            dispatcher.utter_message(buttons=buttons)
        
        # if valid information isn't provided,
        # ask the user for the information
        # again.
        elif name:
            #dispatcher.utter_message(text="Invalid data 2a.")
            dispatcher.utter_message(response="utter_ask_for_location")

        elif location:
            dispatcher.utter_message(text="Invalid data 2b.")
            dispatcher.utter_message(response="utter_ask_for_name")

        return []

class ActionDefaultAskAffirmation(Action):
    def name(self):
        return "action_default_ask_affirmation"

    async def run(self, dispatcher, tracker, domain):
        print('In ActionDefaultAskAffirmation')
        name = tracker.get_slot('name')
        location = tracker.get_slot('location')

        if name and location:
            dispatcher.utter_message(
                text="Thanks for the information!"\
                    "What would you like to do next3?"
            )
            #dispatcher.utter_message(buttons=buttons)
        
        # if valid information isn't provided,
        # ask the user for the information
        # again.
        elif name:
            dispatcher.utter_message(text="Invalid data 3a.")
            dispatcher.utter_message(response="utter_ask_for_location")

        elif location:
            dispatcher.utter_message(text="Invalid data 3b.")
            dispatcher.utter_message(response="utter_ask_for_name")

        return []

