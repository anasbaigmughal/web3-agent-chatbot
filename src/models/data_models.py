from pydantic import BaseModel

class PromptAnalysis(BaseModel):
    is_safe: bool
    reasoning: str
