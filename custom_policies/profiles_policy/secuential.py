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
    subtopics = []

    def __init__(self,
                 topic: Topic,
                 tema_actual: Optional[Subtopic] = None
                 ):
        self.tema = topic

        dialogflow = json.load(open("/home/tomas/Escritorio/rasaS/simple-rasa-custom-policy/custom_policies/data"
                                    "/secuential_dialogflow.json"))
        for subtopic in dialogflow['scrum']:
            self.subtopics.append(Subtopic(subtopic['topic_name'], subtopic['explanation'], subtopic['examples']))
            print(self.subtopics[0].explanation)
        if tema_actual is not None:
            self.tema_actual = tema_actual
        else:
            self.tema_actual = self.subtopics[0]

    def answer(self,
               tracker: DialogueStateTracker,
               domain: Domain,
               interpreter: NaturalLanguageInterpreter,
               **kwargs: Any,
               ) -> str:
        if tracker.latest_message.intent['name'] == 'saludar':
            return 'utter_saludar'
        if tracker.latest_message.intent['name'] == 'preguntar_tema':
            # aca estoy popeando la entidad, si se detecta mas de una entidad
            # probablemente esto no anda
            return self.answersQA[tracker.latest_message.entities.pop(0)['value']]
        else:
            if tracker.latest_message.intent['name'] == 'avanzar_conversacion':
                index_actual = self.subtopics.index(self.tema_actual)
                self.tema_actual = self.subtopics[index_actual+1]
                respuesta = self.tema_actual.explanation[str(self.tema_actual.last_explanation)]
                self.tema_actual.last_explanation += 1
                return respuesta
            else:
                if tracker.latest_message.intent['name'] == 'ejemplo':
                    self.tema_actual.last_example += 1
                    return self.tema_actual.examples[self.tema_actual.last_example]
                else:
                    respuesta = self.tema_actual.explanation[str(self.tema_actual.last_explanation)]
                    self.tema_actual.last_explanation += 1
                    return respuesta
