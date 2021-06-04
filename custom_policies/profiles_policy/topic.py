from typing import List


class Topic:
    topic_name = ''
    subtopics = ['Topic']
    explanation = {
        1: "more_abstract",
        2: "more_detailed"
    }
    examples = {
        1: "example 1",
        2: "example 2"
    }
    required_concepts = ['Topic']
    history = {
        "last_explanation": 0,
        "last_example": 0
    }

    def __init__(self,
                 topic_name: str,
                 subtopics: List['Topic']
                 ):
        self.topic_name = topic_name
