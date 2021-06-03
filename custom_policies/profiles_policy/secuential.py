import json
from typing import Any, List

from rasa.shared.core.domain import Domain
from rasa.shared.core.trackers import DialogueStateTracker
from rasa.shared.nlu.interpreter import NaturalLanguageInterpreter

from custom_policies.profiles_policy.profile import Profile
class Secuential(Profile):
    answersQA = {}

    def __init__(self,
                 domain: Domain):
        json.load(open(''))

    def answer(self,
               tracker: DialogueStateTracker,
               domain: Domain,
               interpreter: NaturalLanguageInterpreter,
               **kwargs: Any,
               ) -> List[float]:
        if intent = preguntar
            answersQA.get(lastmessage.entity)

