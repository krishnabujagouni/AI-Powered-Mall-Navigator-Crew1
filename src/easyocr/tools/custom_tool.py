from crewai.tools import tool
import os
import json
import easyocr
from PIL import Image
import numpy as np

# -----------------------------
# Helper functions
# -----------------------------
def get_image_files(image_dir: str):
    return [
        os.path.join(image_dir, f)
        for f in os.listdir(image_dir)
        if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))
    ]

def run_ocr(reader, image_path: str, min_confidence: float = 0.7):
    """
    Run OCR on the image and return a list of results with bbox, text, and confidence.
    Only keeps results with confidence >= min_confidence.
    """
    with Image.open(image_path) as img:
        if img is None:
            return []

    raw_results = reader.readtext(image_path)

    results = []
    for bbox, text, prob in raw_results:
        confidence = float(prob)
        if confidence < min_confidence:
            continue  # Skip low-confidence results

        # Convert bbox coordinates to integers
        bbox_int = [[int(x), int(y)] for [x, y] in bbox]

        results.append({
            "bbox": bbox_int,
            "text": text,
            "confidence": round(confidence, 3)  # Round to 3 decimals
        })

    return results

# -----------------------------
# JSON encoder for NumPy types
# -----------------------------
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return float(obj)
        if isinstance(obj, (np.ndarray,)):
            return obj.tolist()
        return super().default(obj)

def save_json(data, output_dir: str, filename: str):
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, cls=NpEncoder)
    return output_path

# -----------------------------
# The actual CrewAI tool
# -----------------------------
@tool
def ExtractMapGraphTool() -> dict:
    """
    Extracts OCR text + bounding boxes from all images in 'c:/easyocr/knowledge/images/',
    saves as JSON in 'c:/easyocr/knowledge/map-json/', and returns structured output.
    """
    try:
        image_dir = os.path.join(os.getcwd(), "c:/easyocr/knowledge/images")
        output_dir = os.path.join(os.getcwd(), "c:/easyocr/knowledge/map-json")

        reader = easyocr.Reader(["en"])
        processed_files = []

        for image_path in get_image_files(image_dir):
            filename = os.path.basename(image_path)
            with Image.open(image_path) as img:
                width, height = img.size

            ocr_results = run_ocr(reader, image_path, min_confidence=0.5)
            if not ocr_results:
                continue

            json_output = {
                "file": filename,
                "image_size": {"width": width, "height": height},
                "ocr_results": ocr_results,
            }

            json_filename = f"ocr_{os.path.splitext(filename)[0]}.json"
            save_json(json_output, output_dir, json_filename)
            processed_files.append(json_filename)

        if not processed_files:
            return {"message": "No images processed."}

        return {
            "message": "OCR extraction complete.",
            "processed_files": processed_files,
            "output_dir": output_dir
        }

    except Exception as e:
        return {"error": f"ExtractMapGraphTool failed: {str(e)}"}


# tools/custom_tool.py

# ... (keep all your existing code and add this new tool) ...

@tool
def ImageReadTool(image_path: str) -> Image.Image:
    """
    Reads an image from the specified file path and returns it
    as a PIL Image object. Use this tool to load the map image
    for visual analysis.
    """
    try:
        image = Image.open(image_path)
        return image
    except FileNotFoundError:
        return "Error: Image file not found at the specified path."
    except Exception as e:
        return f"An error occurred while reading the image: {str(e)}"
    

@tool
def FileReadTool(file_path: str) -> str:
    """
    Reads the entire content of a specified file and returns it as a single string.
    Use this tool to read the JSON file created by the OCR Specialist.
    The 'file_path' argument must be a valid path to a text-readable file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Error: File not found at the specified path."
    except Exception as e:
        return f"An error occurred while reading the file: {str(e)}"
# from crewai.tools import tool
# import os
# import json
# import easyocr
# from PIL import Image
# import numpy as np

# # -----------------------------
# # Helper functions
# # -----------------------------
# def get_image_files(image_dir: str):
#     return [
#         os.path.join(image_dir, f)
#         for f in os.listdir(image_dir)
#         if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))
#     ]

# def run_ocr(reader, image_path: str):
#     with Image.open(image_path) as img:
#         if img is None:
#             return []

#     results = reader.readtext(image_path)
#     return [
#         {"bbox": bbox, "text": text, "confidence": float(prob)}
#         for (bbox, text, prob) in results
#     ]

# # -----------------------------
# # JSON encoder for NumPy types
# # -----------------------------
# class NpEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, (np.integer,)):
#             return int(obj)
#         if isinstance(obj, (np.floating,)):
#             return float(obj)
#         if isinstance(obj, (np.ndarray,)):
#             return obj.tolist()
#         return super().default(obj)

# def save_json(data, output_dir: str, filename: str):
#     os.makedirs(output_dir, exist_ok=True)
#     output_path = os.path.join(output_dir, filename)
#     with open(output_path, "w", encoding="utf-8") as f:
#         json.dump(data, f, indent=2, cls=NpEncoder)
#     return output_path

# # -----------------------------
# # The actual CrewAI tool
# # -----------------------------
# @tool
# def ExtractMapGraphTool() -> dict:
#     """
#     Extracts OCR text + bounding boxes from all images in 'c:/easyocr/knowledge/images/',
#     saves as JSON in 'c:/easyocr/knowledge/map-json/', and returns structured output.
#     """
#     try:
#         image_dir = os.path.join(os.getcwd(), "c:/easyocr/knowledge/images")
#         output_dir = os.path.join(os.getcwd(), "c:/easyocr/knowledge/map-json")

#         reader = easyocr.Reader(["en"])
#         processed_files = []

#         for image_path in get_image_files(image_dir):
#             filename = os.path.basename(image_path)
#             with Image.open(image_path) as img:
#                 width, height = img.size

#             ocr_results = run_ocr(reader, image_path)
#             if not ocr_results:
#                 continue

#             json_output = {
#                 "file": filename,
#                 "image_size": {"width": width, "height": height},
#                 "ocr_results": ocr_results,
#             }

#             json_filename = f"ocr_{os.path.splitext(filename)[0]}.json"
#             save_json(json_output, output_dir, json_filename)
#             processed_files.append(json_filename)

#         if not processed_files:
#             return {"message": "No images processed."}

#         return {
#             "message": "OCR extraction complete.",
#             "processed_files": processed_files,
#             "output_dir": output_dir
#         }

#     except Exception as e:
#         return {"error": f"ExtractMapGraphTool failed: {str(e)}"}

