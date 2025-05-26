from abc import ABC, abstractmethod

class ImageUnderstandingModel(ABC):
    @abstractmethod
    def describe_image(self, image_path: str) -> str:
        """
        Processes an image and returns a textual description.

        :param image_path: Path to the image file.
        :return: A string describing the image content.
        """
        pass

class LanguageModel(ABC):
    @abstractmethod
    def generate_response(self, prompt: str) -> str:
        """
        Generates a response based on a given prompt.

        :param prompt: The input prompt for the language model.
        :return: A string containing the model's response.
        """
        pass

class MultimodalModel(ImageUnderstandingModel, LanguageModel):
    @abstractmethod
    def process_image_and_question(self, image_path: str, question: str) -> str:
        """
        Processes an image and a question to generate a direct answer.
        This method is for models that can internally handle both image context and text query.

        :param image_path: Path to the image file.
        :param question: The user's question about the image.
        :return: A string containing the answer to the question.
        """
        pass

    # Optional: Depending on the specific multimodal model's capabilities,
    # it might use the inherited methods or have its own implementations.
    # If a multimodal model inherently uses describe_image and generate_response
    # as part of its process_image_and_question, those might not need separate calls.
    # However, to fulfill the interface, they should be implemented.

    # For a true multimodal model, describe_image might not be directly called by the orchestrator
    # if process_image_and_question is used. It could be implemented to describe the image
    # if the model is used solely as an ImageUnderstandingModel.
    @abstractmethod
    def describe_image(self, image_path: str) -> str:
        # This might internally call a part of its multimodal processing
        # or a specific image captioning feature.
        pass

    # Similarly, generate_response might not be directly called by the orchestrator
    # if process_image_and_question is used. It could be implemented to respond to
    # a text prompt if the model is used solely as a LanguageModel.
    @abstractmethod
    def generate_response(self, prompt: str) -> str:
        # This might internally call its text generation capabilities.
        pass
