import unittest
from unittest.mock import MagicMock

# Adjust imports based on how tests will be run (e.g., from project root)
# Assuming tests are run in an environment where 'image_llm_collaboration' is discoverable
try:
    from image_llm_collaboration.workflow.orchestrator import CollaborationWorkflow
    from image_llm_collaboration.models.base import ImageUnderstandingModel, LanguageModel, MultimodalModel
except ImportError:
    # Simple fallback for path issues, consider a proper test setup (e.g., tox, pytest config)
    import sys
    import os
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    # Since test_orchestrator.py is in image_llm_collaboration/tests/
    # '..' would be image_llm_collaboration/
    # So the imports should be:
    from workflow.orchestrator import CollaborationWorkflow # Corrected path
    from models.base import ImageUnderstandingModel, LanguageModel, MultimodalModel # Corrected path


class TestCollaborationWorkflow(unittest.TestCase):

    def setUp(self):
        """Set up for test methods."""
        self.mock_image_model = MagicMock(spec=ImageUnderstandingModel)
        self.mock_language_model = MagicMock(spec=LanguageModel)
        self.mock_multimodal_model = MagicMock(spec=MultimodalModel)
        # Ensure the mock_multimodal_model also has the methods of its parent specs if they are called directly
        # For MultimodalModel, it inherits from ImageUnderstandingModel and LanguageModel
        # MagicMock with spec=MultimodalModel should inherently handle methods from MultimodalModel,
        # and if MultimodalModel correctly lists its inherited abstract methods, spec should cover them.
        # However, process_image_and_question is specific to MultimodalModel.
        # describe_image and generate_response are part of its interface too.
        self.mock_multimodal_model.process_image_and_question = MagicMock(return_value="Direct multimodal response")
        self.mock_multimodal_model.describe_image = MagicMock(return_value="Multimodal image description")
        self.mock_multimodal_model.generate_response = MagicMock(return_value="Multimodal text response")

        self.prompt_template = "Image: {image_description}, Question: {user_question}"
        self.sample_image_path = "path/to/sample_image.jpg"
        self.sample_question = "What is in the image?"

    def test_process_request_separate_models(self):
        """Test the workflow with separate image and language models."""
        self.mock_image_model.describe_image.return_value = "A cat sitting on a mat."
        self.mock_language_model.generate_response.return_value = "The image contains a cat on a mat."

        workflow = CollaborationWorkflow(
            image_model=self.mock_image_model,
            text_model=self.mock_language_model,
            prompt_template=self.prompt_template
        )

        result = workflow.process_request(self.sample_image_path, self.sample_question)

        self.mock_image_model.describe_image.assert_called_once_with(self.sample_image_path)
        expected_prompt = self.prompt_template.format(
            image_description="A cat sitting on a mat.",
            user_question=self.sample_question
        )
        self.mock_language_model.generate_response.assert_called_once_with(expected_prompt)
        self.assertEqual(result, "The image contains a cat on a mat.")
        print("Test TestCollaborationWorkflow.test_process_request_separate_models PASSED (structure)")

    def test_process_request_multimodal_model(self):
        """Test the workflow when a single multimodal model is used."""
        # Use the mock_multimodal_model created in setUp
        self.mock_multimodal_model.process_image_and_question.return_value = "The multimodal model says: A cat is on the mat."

        workflow = CollaborationWorkflow(
            image_model=self.mock_multimodal_model, 
            text_model=self.mock_multimodal_model,  
            prompt_template=self.prompt_template 
        )

        result = workflow.process_request(self.sample_image_path, self.sample_question)

        self.mock_multimodal_model.process_image_and_question.assert_called_once_with(
            image_path=self.sample_image_path,
            question=self.sample_question
        )
        # Ensure the other model methods on this specific mock were not called BY THE ORCHESTRATOR in this path
        self.mock_multimodal_model.describe_image.assert_not_called()
        self.mock_multimodal_model.generate_response.assert_not_called()
        self.assertEqual(result, "The multimodal model says: A cat is on the mat.")
        print("Test TestCollaborationWorkflow.test_process_request_multimodal_model PASSED (structure)")

    def test_process_request_multimodal_model_as_separate_not_called(self):
        """Test that if a multimodal model is passed for both, only its combined method is called by the orchestrator."""
        # This test uses the self.mock_multimodal_model from setUp.
        # Its process_image_and_question method is already mocked.
        
        workflow = CollaborationWorkflow(
            image_model=self.mock_multimodal_model, 
            text_model=self.mock_multimodal_model, 
            prompt_template="Template: {image_description} Q: {user_question}"
        )
        
        workflow.process_request("image.png", "What is this?")
        
        self.mock_multimodal_model.process_image_and_question.assert_called_once()
        
        # Critical check: The orchestrator should not call these on the *text_model* (which is the multimodal_model here)
        # if it has already used process_image_and_question.
        self.mock_multimodal_model.describe_image.assert_not_called()
        self.mock_multimodal_model.generate_response.assert_not_called()

        print("Test TestCollaborationWorkflow.test_process_request_multimodal_model_as_separate_not_called PASSED (structure)")


if __name__ == '__main__':
    # To run tests directly using `python tests/test_orchestrator.py` from the project root,
    # the imports need to resolve. The try-except block handles one common case.
    # For more robust testing, use a test runner like `python -m unittest discover tests` from root,
    # or pytest. This often requires __init__.py in the tests folder and potentially the parent folders
    # to be recognized as packages.
    
    # If image_llm_collaboration is the project root directory itself (where .git might be)
    # and tests/ are directly under it, then the original relative imports
    # from ..workflow.orchestrator import CollaborationWorkflow
    # from ..models.base import ...
    # would be more standard when running with a test runner from the project root.
    # The current import structure with sys.path manipulation is a workaround for some direct run scenarios.
    unittest.main()
