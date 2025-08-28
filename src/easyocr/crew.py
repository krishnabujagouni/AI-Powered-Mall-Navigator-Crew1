from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from typing import List
from tools.custom_tool import ExtractMapGraphTool, ImageReadTool, FileReadTool
import os



def get_llm_config():
        """Initializes and returns the Gemini 1.5 Flash model."""
    # Check for Gemini/Google API Key
        gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not gemini_key:
            raise ValueError("GEMINI_API_KEY or GOOGLE_API_KEY not found in environment variables.")

    # Define the single, powerful model we'll use for everything.
        model_name = "gemini-1.5-flash-latest"

        print(f"Using Google LLM Provider for all agents.")
        print(f"  - Shared Model: {model_name}")

    # Initialize a single LLM object to be shared.
        llm = LLM(
            model=f"gemini/{model_name}",
            api_key=gemini_key
        )
    
        return llm

@CrewBase
class WayfinderCrew:
    agents: List[Agent]
    tasks: List[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"




    def __init__(self, map_image_path: str):
        self.map_image_path = map_image_path
        self.llm = get_llm_config()

    @agent
    def ocr_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["ocr_agent"],
            tools=[ExtractMapGraphTool],
            llm=self.llm,  
            verbose=True,
        )
    

    @agent
    def navigator_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["navigator_agent"],
            llm=self.llm,  # Assign the multimodal LLM to this agent
            tools=[ImageReadTool, FileReadTool],
            verbose=True,
        )

    @task
    def extract_text_task(self) -> Task:
        return Task(
            config=self.tasks_config["extract_text_task"],
            agent=self.ocr_agent(),
        )
    
    @task
    def guidance_task(self) -> Task:
        return Task(
            config=self.tasks_config["guidance_task"],
            agent=self.navigator_agent(),
            # context=self._generate_navigation_context,
        )


    @crew
    def crew(self) -> Crew:
        """Creates the Wayfinder crew."""
        return Crew(
            agents=[self.ocr_agent(), self.navigator_agent()],
            tasks=[self.extract_text_task(), self.guidance_task()],
            process=Process.sequential,
            verbose=True,
        )
