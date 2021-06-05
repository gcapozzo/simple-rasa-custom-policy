import json
from typing import Any, List

from rasa.shared.core.domain import Domain
from rasa.shared.core.trackers import DialogueStateTracker
from rasa.shared.nlu.interpreter import NaturalLanguageInterpreter

from custom_policies.profiles_policy.profile import Profile


class Global(Profile):
    answersQA = {"scrum": "utter_global_scrum", "framework": "utter_global_framework"}

    def __init__(self,
                 domain: Domain): None

    def answer(self,
               tracker: DialogueStateTracker,
               domain: Domain,
               interpreter: NaturalLanguageInterpreter,
               **kwargs: Any,
               ) -> List[float]:
        if tracker.latest_message.intent['name'] == 'preguntar_tema':
            # aca estoy popeando la entidad, si se detecta mas de una entidad
            # probablemente esto no anda
            return self.answersQA[tracker.latest_message.entities.pop(0)['value']]

hola = Global(None)