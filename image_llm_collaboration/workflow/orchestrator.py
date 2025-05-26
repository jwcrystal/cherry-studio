from image_llm_collaboration.models.base import ImageUnderstandingModel, LanguageModel, MultimodalModel

class CollaborationWorkflow:
    def __init__(self, image_model: ImageUnderstandingModel, text_model: LanguageModel, prompt_template: str):
        """
        Initializes the CollaborationWorkflow.

        :param image_model: An instance of ImageUnderstandingModel.
        :param text_model: An instance of LanguageModel.
        :param prompt_template: A string template for generating prompts.
                                It should expect {image_description} and {user_question} placeholders.
        """
        self.image_model = image_model
        self.text_model = text_model
        self.prompt_template = prompt_template

    def process_request(self, image_path: str, question: str) -> str:
        """
        Processes an image and a question to generate an answer.

        It automatically detects if the text_model is a MultimodalModel and
        if it's the same instance as the image_model. If so, it uses the model's
        direct image and question processing capabilities. Otherwise, it uses
        the image_model to get a description, formats a prompt, and then uses
        the text_model to generate the answer.

        :param image_path: Path to the image file.
        :param question: The user's question about the image.
        :return: A string containing the generated answer.
        """
        # Check if the text_model is a multimodal model and is the same as the image_model
        # This implies a single model is being used for both capabilities.
        if isinstance(self.text_model, MultimodalModel) and self.text_model is self.image_model:
            print("Using single multimodal model for both image understanding and text generation.")
            # Ensure the model instance actually implements MultimodalModel
            # The type hint for self.text_model is LanguageModel, so we cast or assert
            multimodal_model_instance = self.text_model 
            return multimodal_model_instance.process_image_and_question(image_path=image_path, question=question)
        else:
            print("Using separate models for image understanding and text generation.")
            # 1. Image model processes the image
            image_description = self.image_model.describe_image(image_path)
            
            # 2. Construct prompt
            # Ensure all expected keys are present for formatting
            prompt = self.prompt_template.format(
                image_description=image_description,
                user_question=question  # Make sure this key matches the template
            )
            
            # 3. Text model generates the answer
            answer = self.text_model.generate_response(prompt)
            return answer
