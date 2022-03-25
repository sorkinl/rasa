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
        print('In ActionHandleProvidedInfo!')
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
                text="From out custom action ActionHandleProvidedInfo - Thanks for tell me about your trip " + name + "."\
                    "I'll think about going to " + location + " next time."
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
        print('In ActionDefaultFallback!')
        name = tracker.get_slot('name')
        location = tracker.get_slot('location')

        if name and location:
            dispatcher.utter_message(
                text="From out custom action ActionDefaultFallback - Thanks for tell me about your trip " + name + "."\
                    "I'll think about going to " + location + " next time."
            )
            #dispatcher.utter_message(buttons=buttons)
        
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
        print('In ActionDefaultAskAffirmation!!')
        name = tracker.get_slot('name')
        location = tracker.get_slot('location')
#We'll probably need to put if statments here to get the intent, and then use that to set the slot
#right now we only have one story, but this will grow.  Think about how to handle this.
        if name and location:
            dispatcher.utter_message(
                text="From out custom action ActionDefaultAskAffirmation - Thanks for tell me about your trip " + name + "."\
                    "I'll think about going to " + location + " next time."
            )
            #dispatcher.utter_message(buttons=buttons)
            return[]
        
        # if valid information isn't provided,
        # ask the user for the information
        # again.
        elif name:
            dispatcher.utter_message(text="Invalid data 3a.")
            dispatcher.utter_message(response="utter_ask_for_location")

        elif location:
            #dispatcher.utter_message(text="Invalid data 3b. I'm going to call you Bob.")
            #dispatcher.utter_message(response="utter_ask_for_name")
            print("message is " + tracker.latest_message['text'], "text")
            #We could do some Python here to extract our best guess from the whole previous string for their name.
            lastOutput = tracker.latest_message['text']
            buttons = [
                {
                    'title': "Can I call you " + lastOutput,
                    'payload': '/gave_name'
                }
            ]
        #should we do button or no buttons and just enter our last best guess regardless?
        dispatcher.utter_message(buttons=buttons)
        #dispatcher.utter_message("going to call you by your last message")
        #return []
        #lastOutput2 = tracker.latest_message['text']
        #That attempt above doesn't works, so can only get latest message to be the one before they entered fallback function
        return [SlotSet("name", lastOutput)]

