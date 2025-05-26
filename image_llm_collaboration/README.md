# Image LLM Collaboration Workflow

This project implements a collaborative workflow between an image understanding model and a language model (LLM) to answer questions about images.

## 🌟 Features

-   **User Interaction**: Allows users to upload an image and ask a question related to it.
-   **Image Analysis**: Utilizes an image understanding model (e.g., GPT-4V, Qwen-VL) to extract descriptions, text, or objects from the image.
-   **Prompt Engineering**: Combines the image analysis results with the user's question to form a detailed prompt.
-   **Response Generation**: Feeds the combined prompt to a powerful language model (assistant model) to generate a natural language answer.
-   **Modular Design**:
    -   Supports easy replacement of image understanding models.
    -   Supports easy replacement of language models.
    -   Class-based interfaces for models.
-   **Flexible Model Usage**:
    -   Can automatically use a single multimodal LLM (if it supports both image and text processing) for both steps.
    -   Supports both API-based models (e.g., OpenAI) and local models (e.g., Qwen-VL, Llama). (Local model implementation is planned).
-   **Configurable Prompts**: Allows customization of prompt templates.

## 🚀 Example Flow

1.  **User**: Uploads `apple_basket.jpg` and asks, "How many apples are in the basket?"
2.  **Image Model**: Analyzes `apple_basket.jpg` and returns, "The image shows a basket containing 3 red apples and 2 bananas."
3.  **System (Prompt Construction)**:
    ```
    Image understanding result: The image shows a basket containing 3 red apples and 2 bananas.
    Question: How many apples are in the basket?
    Please answer the question based on the image information.
    ```
4.  **Language Model**: Processes the prompt and replies, "There are 3 apples in the basket."

## 🛠️ Project Structure

```
image_llm_collaboration/
├── models/               # Model interfaces and implementations
│   ├── __init__.py
│   ├── base.py           # Abstract base classes for models
│   ├── api_models.py     # Implementations for API-based models (OpenAI, etc.)
│   └── local_models.py   # (Placeholder) Implementations for local models
├── workflow/             # Orchestration logic
│   ├── __init__.py
│   └── orchestrator.py   # CollaborationWorkflow class
├── templates/            # Prompt templates
│   └── default_prompt.txt
├── tests/                # Unit tests
│   ├── __init__.py
│   ├── test_orchestrator.py
│   └── test_models.py
├── examples/             # Example scripts or notebooks (if any)
│   └── .gitkeep
├── main.py               # CLI entry point
├── config.py             # Configuration (API keys, model choices - placeholder)
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

## ⚙️ Setup and Usage (Current - Stubs)

Currently, the system uses placeholder ("stub") models that simulate the behavior of actual AI models without making real API calls or running heavy computations.

1.  **Prerequisites**:
    *   Python 3.8+

2.  **Running the CLI**:
    Navigate to the `image_llm_collaboration` directory. You can run the `main.py` script with an image path and a question:

    ```bash
    python main.py path/to/your/image.jpg "Your question about the image?"
    ```
    Example:
    ```bash
    # Create a dummy image file for testing
    touch dummy_image.jpg 
    
    python main.py dummy_image.jpg "How many objects are in this dummy image?"
    ```

    You can also specify the mode:
    ```bash
    # To test with separate stub models (default)
    python main.py dummy_image.jpg "Test question?" --mode separate

    # To test with a single multimodal stub model
    python main.py dummy_image.jpg "Test question?" --mode multimodal 
    ```

## 🔮 Future Work

-   Implement concrete classes for actual API-based models (e.g., OpenAI GPT-4V, Claude Vision).
-   Implement concrete classes for local models (e.g., Qwen-VL, Llama3.2-Vision) potentially using libraries like `transformers`.
-   Develop a more robust configuration system (e.g., using `.env` files for API keys, YAML for model selection).
-   Add comprehensive error handling and logging.
-   Build a simple web interface (e.g., using Flask or FastAPI).
-   Expand unit tests for full coverage.
