from pydantic import BaseModel

class GherkinStep(BaseModel):
    step: str  # The Gherkin-style step input from consumer
