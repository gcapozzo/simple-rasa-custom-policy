from typing import Any, List

from rasa.shared.core.domain import Domain
from rasa.shared.core.trackers import DialogueStateTracker
from rasa.shared.nlu.interpreter import NaturalLanguageInterpreter


class Profile:
    def __init__(self,
                 domain: Domain):
        pass

    """
    Returns the array of probabilities of a prediction after receiving
    as parameters the information of the last user message  
    """

    def answer(self,
               tracker: DialogueStateTracker,
               domain: Domain,
               interpreter: NaturalLanguageInterpreter,
               **kwargs: Any,
               ) -> List[float]:
        raise NotImplementedError("Policy must have the capacity to answer.")
