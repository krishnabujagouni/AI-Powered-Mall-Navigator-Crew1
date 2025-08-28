### \#\# 🗺️ AI-Powered Mall Wayfinder Crew

This project is an autonomous AI agent crew designed to provide real-time, step-by-step navigation instructions within a shopping mall using a visual map and Optical Character Recognition (OCR).

-----

### \#\# 🎯 Project Goal

Navigating large, complex indoor environments like shopping malls can be challenging. Static directories are often confusing and don't provide personalized, turn-by-turn directions. This project solves this by creating an intelligent, conversational agent system that acts as a personal mall guide, transforming a static map image into an interactive navigation experience.

-----

### \#\# ✨ Core Features

  * **Automated Map Digitization:** Automatically scans a mall map image using OCR to extract all store names and their precise bounding box coordinates.
  * **Dual-Agent Workflow:** Utilizes a specialized two-agent crew for a clear separation of tasks: one agent for data extraction (OCR) and another for reasoning and navigation.
  * **Multimodal Reasoning:** The navigation agent combines visual understanding of the map's layout with the structured text data from the OCR to plan the most logical route.
  * **Tool-Augmented Agents:** Agents are equipped with a suite of tools to read files, load images, and perform OCR, allowing them to interact with their environment.
  * **Dynamic and Interactive:** The system interactively prompts the user for their start and end locations, providing a customized route for each request.

-----

### \#\# 🤖 How It Works: The Two-Agent Crew

The system operates through a sequential process managed by a CrewAI crew:

1.  **User Input:** The process begins when the user runs the `main.py` script and is prompted to enter their starting location and desired destination.

2.  **Agent 1: OCR Specialist**

      * **Task:** `extract_text_task`
      * **Action:** This agent's sole responsibility is data extraction. It is given the path to the mall map's directory and uses its `ExtractMapGraphTool` to:
        1.  Scan the mall map image.
        2.  Identify all text elements using the `easyocr` library.
        3.  Save the extracted text and its corresponding coordinates into a single, predictably named JSON file (`ocr_output.json`).

3.  **Agent 2: Expert Mall Navigator**

      * **Task:** `guidance_task`
      * **Action:** This agent acts as the "brain" of the operation. Its instructions are to:
        1.  Receive the user's start/end locations and the paths to the image and JSON directory.
        2.  Use its `FileReadTool` to open and read the `ocr_output.json` file created by the first agent.
        3.  Use its `ImageReadTool` to load the visual mall map.
        4.  Correlate the user's request with the data from the JSON file to find the precise coordinates for the start and end points.
        5.  Analyze the visual layout of the map (from the image) to understand walkable paths, corridors, and potential landmarks.
        6.  Synthesize all this information to formulate the most efficient route and generate the final, step-by-step directions in natural language.

-----

### \#\# 🛠️ Technology Stack

  * **AI Framework:** **CrewAI**
  * **Language Model (LLM):** **Google Gemini 1.5 Flash** (for its multimodal and cost-effective capabilities)
  * **OCR Engine:** **easyocr**
  * **Core Language:** **Python**
  * **Key Libraries:**
      * `python-dotenv` for environment variable management.
      * `Pillow` for image manipulation.

-----

### \#\# 🚀 Setup and Usage

To run this project on your local machine:

1.  **Clone the Repository:**
    ```bash
    git clone <your-repository-url>
    cd <your-project-folder>
    ```
2.  **Set up Virtual Environment:**
    ```bash
    python -m venv venv
    venv\Scripts\activate  # On Windows
    source venv/bin/activate # On macOS/Linux
    ```
3.  **Install Dependencies:**
    ```bash
    pip install crewai python-dotenv easyocr Pillow torch torchvision torchaudio
    ```
4.  **Create `.env` File:** Create a file named `.env` in the root project folder and add your Google API key:
    ```
    GOOGLE_API_KEY="YOUR_API_KEY_HERE"
    ```
5.  **Set up Directories:** Create the necessary folder structure and place your map image inside:
      * `c:/easyocr/knowledge/images/` (Place your `5250.gif` or other map image here)
      * `c:/easyocr/knowledge/map-json/` (This will be created automatically)
6.  **Run the Application:**
    ```bash
    python main.py
    ```
    The script will then prompt you for your starting and destination locations.

-----

### \#\# 🔮 Future Enhancements

  * **Real-time Location:** Integrate with indoor positioning systems (IPS) to automatically detect the user's starting location.
  * **Multi-floor Navigation:** Expand the logic to handle directions across different floors, including stairs, escalators, and elevators.
  * **Graphical User Interface (GUI):** Develop a simple web or mobile interface where the user can see the map and the generated path highlighted.
  * **Dynamic Obstacle Avoidance:** Incorporate a way to account for temporary obstacles like promotional kiosks or cleaning crews.
