# import os
# from crew import OcrCrew

# from dotenv import load_dotenv

# load_dotenv()

# api_key = os.getenv("GEMINI_API_KEY")
# model_name = os.getenv("MODEL")

# inputs = {
#     "image_path": "c:/easyocr/knowledge/images/5250.gif"  # Example input
# }

# def run():
#     crew_instance = OcrCrew()
#     crew_instance.crew().kickoff(inputs=inputs)


# if __name__ == "__main__":
#     run()

import os
import json
from PIL import Image
from crew import WayfinderCrew # Import the crew class from your crew.py file
from dotenv import load_dotenv
load_dotenv()

def run():
    """
    Sets up and runs the WayfinderCrew for a specific navigation query.
    """
    # 1. Define paths and user query
    map_image_file = "5250.gif"
    image_directory = "C:/easyocr/knowledge/images"
    json_output_directory = "C:/easyocr/knowledge/map-json"
    full_image_path = os.path.join(image_directory, map_image_file)
    
    if not os.path.exists(full_image_path):
        print(f"ERROR: The map image was not found at {full_image_path}")
        return

    print("Welcome to the Mall Wayfinder!")
    start_location = input("Where are you starting from? (e.g., Marshalls): ")
    destination = input("Where would you like to go? (e.g., forever21): ")
    # start_location = "Marshalls"
    # destination = "forever21"
    # user_query = f"I am at '{start_location}' and want to go to '{destination}'."

    # 2. Instantiate the WayfinderCrew class
    wayfinder_crew_instance = WayfinderCrew(map_image_path=full_image_path)

  

    
    # The crew will automatically pass the necessary inputs to the correct tasks
    # inputs = {
    #     'json_output_dir': json_output_directory,
    #     'user_query': user_query,
    #     'image_file_path': full_image_path
    # }

    inputs = {
        'json_output_dir': json_output_directory,
        'image_file_path': full_image_path,
        'start_location': start_location,
        'destination': destination
    }

    # 4. Get the configured crew and kick off the process
    print("\n--- Kicking off the Wayfinder Crew ---")
    crew = wayfinder_crew_instance.crew()
    result = crew.kickoff(inputs=inputs)
    
    print("\n\n########################")
    print("## Final Navigation Guidance:")
    print("########################\n")
    print(result)


if __name__ == "__main__":
    run()