from typing import Any, Text, Dict, List
from rasa_sdk.forms import FormValidationAction, ActiveLoop
from rasa_sdk import Action, Tracker
#from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.events import ConversationResumed
#from rasa_sdk.events import ConversationPaused
from rasa_sdk.events import UserUttered
from rasa_sdk.events import ActionExecuted
from rasa_sdk.events import FollowupAction
from rasa.shared.nlu.training_data.message import Message
import json


#from rasa_sdk import Action, Tracker
#from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, ConversationPaused

#As of now, I can send any user sent via NLU uncertainty, set the slot and redirect them to a new story.
#The first function sets the story slot at the beginning so we know they're on the trip story.
#Second function we overwrite the DefaultAffirmation function.  Right now, I just set the slot to be New York.
#Key bit is that follow_up_action we can then trigger next.  That function does nothing, but by starting it
#we send the user to the start of the third story in stories.yml.
#it would be nicer if we could prompt them again to enter just the location.  Probably easiest way to do that 
#is to add a prompt at the start of this story that says "Enter a location like Paris or China" and follow that
#with a slot called "location_we_take_anything" and mimic the above story with a near duplicate but using this second 
#slot.


#We will define a function at the start of each story whose only purpose to fill the story slot.  We need this 
#so that later we can know within other functions what story they are on.
class ActionSetStorySlotAsTrip(Action):
    def name(self):
        return "action_set_story_slot_as_trip"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('In ActionSetStorySlotAsTrip!')
        story = tracker.get_slot('story')
        #That attempt above doesn't works, so can only get latest message to be the one before they entered fallback function
        if story is None:
          return [SlotSet("story", "trip")]
        else:
            #If we're here, we kicked here after not providing a location Rasa understood
          return [FollowupAction("after_handle_no_trip_location")]


# We will catch NLU uncertainty here and override their function.  In general, we just want our best guess, a default value, or send them onto a story that 
# doesn't need it.  Avoid having users get frustrated by having their input not recognized.
class ActionDefaultAskAffirmation(Action):
    def name(self):
        return "action_default_ask_affirmation"

    async def run(self, dispatcher, tracker, domain):
        print('In ActionDefaultAskAffirmation!!')
        story = tracker.get_slot('story')
        location = tracker.get_slot('location')
        lastOutput = tracker.latest_message['text']

#We will start each story with an action that sets the story slot so we know which conversation the user is having.
        if story == 'trip' and location is None:
          print("message is " + tracker.latest_message['text'], "text2")

#We could put Python here and just guess best location, if nothing set a default, or we can bounce them to a new story where we don't reference the location.


          #buttons = [
          #  {
          #  'title': "Sorry, I'm just a bot and I didn't recognize the place in your last sentence.  My best guess is the button below.  Either click it or give me just the place, like Paris or Africa  " + lastOutput,
          #  'payload': '/inform_location'
          #  }
          #]

          #dispatcher.utter_message(text="Click the button below", buttons=buttons)
          #dispatcher.utter_message(text="I will just set the location in the function")

          return [SlotSet("location", "New York"), FollowupAction("after_handle_no_trip_location")]

        else:
          print("We are in default ask affirmation action and have not handled this scenario")
          return []

class AfterHandleNoTripLocation(Action):
    def name(self) -> Text:
        return "after_handle_no_trip_location"

    def run(self, dispatcher, tracker, domain):
        #return [SlotSet("location", "New York")]
        return []
