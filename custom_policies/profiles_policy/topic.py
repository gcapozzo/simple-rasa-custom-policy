from custom_policies.profiles_policy.subtopic import Subtopic
from typing import List


class Topic:
    topic_name = ''
    subtopics = [Subtopic]
    last_subtopic = 0
    

    def __init__(self,
                 topic_name: str,
                 subtopics: List[Subtopic]
                 ):
        self.topic_name = topic_name
        self.subtopics = subtopics
