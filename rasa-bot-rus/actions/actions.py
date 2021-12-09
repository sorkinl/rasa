""" from typing import Text, List, Optional, Dict, Any
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Tracker, Action """


# class ActionSayStuff(Action):
#     def name(self) -> Text:
#         return "action_say_stuff"
#
#     def run(self,
#             dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         dispatcher.utter_message("Stuff")
#
#         return []
