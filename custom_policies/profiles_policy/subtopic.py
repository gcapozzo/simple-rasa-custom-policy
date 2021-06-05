from typing import List


class Subtopic:
    topic_name = ''
    explanation = {
        1: "more_abstract",
        2: "more_detailed"
    }
    examples = {
        1: "example 1",
        2: "example 2"
    }
    last_explanation = 1
    last_example = 1

    def __init__(self,
                 topic_name: str,
                 explanations: {int: str},
                 examples: {int: str}
                 ):
        self.topic_name = topic_name
        self.explanation = explanations
        self.examples = examples
