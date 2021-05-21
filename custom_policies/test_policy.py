import zlib

import base64
import json
import logging
from rasa.shared.core import domain

from tqdm import tqdm
from typing import Optional, Any, Dict, List, Text

import rasa.utils.io
import rasa.shared.utils.io
from rasa.shared.constants import DOCS_URL_POLICIES
from rasa.shared.core.domain import State, Domain
from rasa.shared.core import events
from rasa.core.featurizers.tracker_featurizers import (
    TrackerFeaturizer,
    MaxHistoryTrackerFeaturizer,
)
from rasa.shared.nlu.interpreter import NaturalLanguageInterpreter
from rasa.core.policies.policy import Policy, PolicyPrediction, confidence_scores_for
from rasa.shared.core.trackers import DialogueStateTracker
from rasa.shared.core.generator import TrackerWithCachedStates
from rasa.shared.utils.io import is_logging_disabled
from rasa.core.constants import MEMOIZATION_POLICY_PRIORITY

logger = logging.getLogger(__name__)

# temporary constants to support back compatibility
MAX_HISTORY_NOT_SET = -1
OLD_DEFAULT_MAX_HISTORY = 5
BESTY_POLICY_PRIORITY = 10
DEFAULT_LEARNING_STYLE = 'global'

class TestPolicy(Policy):
    def __init__(
            self,
            featurizer: Optional[TrackerFeaturizer] = None,
            priority: int = BESTY_POLICY_PRIORITY,
            usertype: Optional[dict] = None,
            story_profiles: Optional[dict] = None,
            learning_style: Optional[str] = None, 
            **kwargs: Any,
    ) -> None:
        super().__init__(featurizer, priority, **kwargs)
        self.story_profiles = story_profiles if story_profiles is not None else {}
        self.usertype = usertype if usertype is not None else {}
        self.learning_style = learning_style if learning_style is not None else DEFAULT_LEARNING_STYLE

    def count_intents_from_stories(self,s,story_intents):
        # this function counts the amount of intents in a story and update the ocurrences of
        # an intent in a story
        count_intents = 0
        for t in s.events:
            if isinstance(t, events.UserUttered):
                intent = t.as_dict().get('parse_data').get('intent').get('name')
                story_intents[intent] = story_intents[intent] + 1
                count_intents = count_intents + 1
        return count_intents

    def train(
            self,
            training_trackers: List[TrackerWithCachedStates],
            domain: Domain,
            interpreter: NaturalLanguageInterpreter,
            **kwargs: Any,
    ) -> None:
        # only original stories
        training_trackers = [
            t
            for t in training_trackers
            if not hasattr(t, "is_augmented") or not t.is_augmented
        ]
        stories = {}
        amount_intents = {}
        for s in training_trackers:
            story_name = s.as_dialogue().as_dict().get('name')
            # initialize dict with intents as keys and 0 counts in each history
            if story_name not in stories.keys():
                # if the story does not exist, is added to the dictionary and the ocurrences of intents are updated
                story_intents = dict.fromkeys(domain.intents, 0)
                stories.update({story_name: story_intents})
                count_intents = self.count_intents_from_stories(s, story_intents)
                amount_intents.update({story_name: count_intents})
                self.usertype.update({story_name: 0.0})
            else:
                # if the story already exists, is updated in the dictionary and the ocurrences of intents are added
                aux_intents = stories.get(story_name)
                count_intents = amount_intents.get(story_name) + self.count_intents_from_stories(s, story_intents)
                amount_intents.update({story_name: count_intents})
                stories.update({story_name: aux_intents})

        # here the training calculates the probability of ocurrence of each intent for each learning style
        for story_name in stories:
            for intent in stories.get(story_name):
                stories.get(story_name).update({
                    intent: stories.get(story_name).get(intent) / amount_intents.get(story_name)
                })
        print(self.usertype)
        print(stories)
        print(amount_intents)
        self.story_profiles.update(stories)
        print(self.story_profiles)
        """Trains the policy on given training trackers.

        Args:
            training_trackers:
                the list of the :class:`rasa.core.trackers.DialogueStateTracker`
            domain: the :class:`rasa.shared.core.domain.Domain`
            interpreter: Interpreter which can be used by the polices for featurization.
        """
        pass

    def predict_action_probabilities(
            self,
            tracker: DialogueStateTracker,
            domain: Domain,
            interpreter: NaturalLanguageInterpreter,
            **kwargs: Any,
    ) -> PolicyPrediction:
        intent = tracker.latest_message.intent.get('name')
        for s in self.usertype:
            self.usertype.update({s: self.usertype.get(s) + self.story_profiles.get(s).get(intent)})
        aux = 0.0
        for s in self.usertype:
            if (aux<self.usertype.get(s) and self.usertype.get(s)>2):
                self.learning_style= s
        print(self.story_profiles)
        print('')
        print(self.learning_style)
        print('')
        print(self.usertype)
        response = "utter_saludar"
        if tracker.latest_action['action_name'] == 'action_listen':
            return self._prediction(confidence_scores_for(response, 1.0, domain))
        if tracker.last_executed_action_has(response, skip=0):
            return self._prediction(confidence_scores_for("action_listen", 1.0, domain))
        return self._prediction(self._default_predictions(domain))

    def _metadata(self) -> Dict[Text, Any]:
        return {
            "priority": self.priority,
            "story_profiles": self.story_profiles,
            "usertype": self.usertype
        }

    @classmethod
    def _metadata_filename(cls) -> Text:
        return "test_policy.json"
