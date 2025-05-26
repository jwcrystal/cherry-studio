# Models that run locally (e.g., Hugging Face Transformers)
from .base import BaseModel

class LocalModel(BaseModel):
    def __init__(self, model_path):
        self.model_path = model_path

    def load(self):
        # Implementation for loading local model
        pass

    def predict(self, data):
        # Implementation for local model prediction
        pass
