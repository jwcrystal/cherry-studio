import argparse
import os

# Attempt to set up imports assuming the script is run from the project root
# or the 'image_llm_collaboration' directory is in PYTHONPATH.
try:
    from workflow.orchestrator import CollaborationWorkflow
    from models.api_models import OpenAIImageModel, OpenAILanguageModel, OpenAIGPT4V
    from models.base import ImageUnderstandingModel, LanguageModel, MultimodalModel # For type checking if needed
except ImportError:
    # Fallback for running directly from within the 'image_llm_collaboration' directory
    # This adjusts sys.path to allow for top-level package imports
    import sys
    if '.' not in sys.path: # Add current directory to path if not already there
        sys.path.insert(0, '.')
    if os.path.basename(os.getcwd()) == 'image_llm_collaboration':
        # If running from inside image_llm_collaboration, adjust path to parent for package-like imports
        sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), '..')))
        from image_llm_collaboration.workflow.orchestrator import CollaborationWorkflow
        from image_llm_collaboration.models.api_models import OpenAIImageModel, OpenAILanguageModel, OpenAIGPT4V
        from image_llm_collaboration.models.base import ImageUnderstandingModel, LanguageModel, MultimodalModel
    else: # If run from project root (e.g. .../image_llm_collaboration_project/image_llm_collaboration/main.py)
          # and image_llm_collaboration_project is the content root.
        from image_llm_collaboration.workflow.orchestrator import CollaborationWorkflow
        from image_llm_collaboration.models.api_models import OpenAIImageModel, OpenAILanguageModel, OpenAIGPT4V
        from image_llm_collaboration.models.base import ImageUnderstandingModel, LanguageModel, MultimodalModel


DEFAULT_PROMPT_TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "templates", "default_prompt.txt")

def load_prompt_template(template_path: str = DEFAULT_PROMPT_TEMPLATE_PATH) -> str:
    """Loads the prompt template from a file."""
    if not os.path.exists(template_path):
        # Fallback if the default path isn't found (e.g. running from a different CWD)
        # This might happen if __file__ is not where templates/default_prompt.txt is relative to.
        # A more robust solution might involve better path configuration or package resources.
        alt_path = os.path.join(os.getcwd(), "templates", "default_prompt.txt") # If CWD is project root
        if os.path.exists(alt_path):
            template_path = alt_path
        else: # if CWD is image_llm_collaboration
            alt_path_2 = os.path.join(os.path.dirname(os.getcwd()), "templates", "default_prompt.txt")
            if os.path.exists(alt_path_2):
                 template_path = alt_path_2
            else:
                raise FileNotFoundError(f"Prompt template not found at {template_path} or {alt_path} or {alt_path_2}")
                
    with open(template_path, "r") as f:
        return f.read()

def main():
    parser = argparse.ArgumentParser(description="Image LLM Collaboration CLI")
    parser.add_argument("image_path", type=str, help="Path to the image file.")
    parser.add_argument("question", type=str, help="Question about the image.")
    parser.add_argument("--mode", type=str, choices=["separate", "multimodal"], default="separate",
                        help="Execution mode: 'separate' for distinct image/text models, "
                             "'multimodal' for a single multimodal model.")
    parser.add_argument("--template_path", type=str, default=DEFAULT_PROMPT_TEMPLATE_PATH,
                        help="Path to the prompt template file.")

    args = parser.parse_args()

    print(f"Loading prompt template from: {args.template_path}")
    try:
        prompt_template = load_prompt_template(args.template_path)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        # Try to load from a relative path assuming script is in project root/image_llm_collaboration
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__)) # .../image_llm_collaboration
            template_file = os.path.join(base_dir, "templates", "default_prompt.txt")
            print(f"Attempting to load template from: {template_file}")
            prompt_template = load_prompt_template(template_file)
        except FileNotFoundError:
            print(f"CRITICAL: Could not load prompt template. Please check paths. Default expected: {DEFAULT_PROMPT_TEMPLATE_PATH}")
            return


    if args.mode == "separate":
        print("\n--- Running in SEPARATE models mode ---")
        # Instantiate example models
        image_model_stub = OpenAIImageModel()
        language_model_stub = OpenAILanguageModel()

        # Instantiate workflow
        workflow = CollaborationWorkflow(
            image_model=image_model_stub,
            text_model=language_model_stub,
            prompt_template=prompt_template
        )
        
        # Process request
        print(f"Processing request for image: '{args.image_path}' and question: '{args.question}'")
        answer = workflow.process_request(args.image_path, args.question)
        print(f"\nFinal Answer:\n{answer}")

    elif args.mode == "multimodal":
        print("\n--- Running in MULTIMODAL model mode ---")
        # Instantiate a multimodal model
        # Note: For the CollaborationWorkflow's multimodal detection logic to trigger,
        # both image_model and text_model parameters should be the *same* multimodal model instance.
        multimodal_model_stub = OpenAIGPT4V()
        
        workflow_multimodal = CollaborationWorkflow(
            image_model=multimodal_model_stub, # Pass the same instance for both
            text_model=multimodal_model_stub,  # Pass the same instance for both
            prompt_template=prompt_template # Template might be used differently or not at all by some multimodal direct calls
        )

        print(f"Processing request with multimodal model for image: '{args.image_path}' and question: '{args.question}'")
        answer = workflow_multimodal.process_request(args.image_path, args.question)
        print(f"\nFinal Answer (Multimodal):\n{answer}")

if __name__ == "__main__":
    # To make imports work when running main.py directly from project root:
    # Assuming 'image_llm_collaboration' is the main package directory.
    # If image_llm_collaboration_project is the root, and main.py is in image_llm_collaboration_project/image_llm_collaboration/main.py
    # One common way is to add the parent of 'image_llm_collaboration' to sys.path if it's not already.
    current_dir = os.path.dirname(os.path.abspath(__file__)) # .../image_llm_collaboration
    project_root_parent = os.path.dirname(current_dir) # .../image_llm_collaboration_project (assuming this is content root)
    
    # Add project_root_parent to sys.path so 'from image_llm_collaboration...' works
    # This is a common pattern but can sometimes be tricky depending on execution environment.
    # Using an __init__.py in project_root_parent and installing as editable package (`pip install -e .`)
    # from project_root_parent is often more robust for development.
    
    # For this subtask, the import block at the top of the file attempts to handle common scenarios.
    main()
