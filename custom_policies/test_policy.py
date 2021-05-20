import zlib

import base64
import json
import logging

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


class TestPolicy(Policy):
    def __init__(
            self,
            featurizer: Optional[TrackerFeaturizer] = None,
            priority: int = MEMOIZATION_POLICY_PRIORITY,
            usertype: Optional[float] = None,
            story_profiles: Optional[List] = None,
            **kwargs: Any,
    ) -> None:
        super().__init__(featurizer, priority, **kwargs)
        self.story_profiles = story_profiles if story_profiles is not None else []
        self.usertype = 0.0

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
        for s in training_trackers:
            # initialize dict with intents as keys and 0 counts in each history
            story_intents = dict.fromkeys(domain.intents, 0)
            for t in s.events:
                if isinstance(t, events.UserUttered):
                    intent = t.as_dict().get('parse_data').get('intent').get('name')
                    story_intents[intent] = story_intents[intent] + 1
            print(story_intents)
            self.story_profiles.append(story_intents)
            # todo: transform results to probabilities
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
        print(tracker.latest_message.intent.get('name'))
        print(tracker.latest_action)
        response = "utter_saludar"
        if tracker.latest_action['action_name'] == 'action_listen':
            return self._prediction(confidence_scores_for(response, 1.0, domain))
        if tracker.last_executed_action_has(response, skip=0):
            return self._prediction(confidence_scores_for("action_listen", 1.0, domain))
        return self._prediction(self._default_predictions(domain))

    def _metadata(self) -> Dict[Text, Any]:
        return {
            "priority": self.priority,
            "story_profiles": self.story_profiles
        }

    @classmethod
    def _metadata_filename(cls) -> Text:
        return "test_policy.json"
