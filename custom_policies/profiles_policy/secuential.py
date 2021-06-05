from custom_policies.profiles_policy.subtopic import Subtopic
from custom_policies.profiles_policy.topic import Topic
import json
from typing import Any, List, Optional

from rasa.shared.core.domain import Domain
from rasa.shared.core.trackers import DialogueStateTracker
from rasa.shared.nlu.interpreter import NaturalLanguageInterpreter

from custom_policies.profiles_policy.profile import Profile
class Secuential(Profile):
    answersQA = {"scrum": "utter_scrum", "framework": "utter_framework"}
    tema_actual = Subtopic
    def __init__(self,
                 domain: Domain,
                 topic: Topic,
                 tema_actual: Optional[Subtopic] = None
                 ): 
            self.tema = topic
            if tema_actual is not None:
                self.tema_actual=tema_actual
            else:
                self.tema_actual = topic.subtopics[topic.last_subtopic]
                    

    def answer(self,
               tracker: DialogueStateTracker,
               domain: Domain,
               interpreter: NaturalLanguageInterpreter,
               **kwargs: Any,
               ) -> List[float]:
            if tracker.latest_message.intent['name'] == 'preguntar_tema':
                #aca estoy popeando la entidad, si se detecta mas de una entidad
                #probablemente esto no anda
                return self.answersQA[tracker.latest_message.entities.pop(0)['value']]
            else:
                if tracker.latest_message.intent['name'] == 'entendi':
                    self.tema_actual=self.tema.subtopics[self.tema.last_subtopic+1]
                    self.tema_actual.explanation[self.tema_actual.last_explanation]
                    self.tema_actual.last_explanation+=1
                else:
                    if tracker.latest_message.intent['name'] == 'ejemplo':
                        self.tema_actual.examples[self.tema_actual.last_example]
                        self.tema_actual.last_example+=1
                    else:
                        self.tema_actual.explanation[self.tema_actual.last_explanation]
                        self.tema_actual.last_explanation+=1

