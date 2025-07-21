import os
import json
import base64
from PIL import Image
from io import BytesIO

class CharacterPromptNode:
    """
    Node: Character selection for anime prompts.
    Non-editable output string, includes preview image (base64 in output_X.json).
    """

    CHARACTER_JSON_FILES = [
        os.path.join(os.path.dirname(__file__), f"output_{i}.json") for i in range(1, 13)
    ]

    char_data = []
    CHARACTERS = []

    try:
        for path in CHARACTER_JSON_FILES:
            with open(path, "r", encoding="utf-8") as f:
                char_data.extend(json.load(f))
    except Exception as e:
        print(f"[CharacterPromptNode] ⚠️ Error loading {path}: {e}")

    CHARACTERS = [list(entry.keys())[0] for entry in char_data if isinstance(entry, dict) and len(entry) >= 1]

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "character": (cls.CHARACTERS,),
            }
        }

    RETURN_TYPES = ("STRING", "IMAGE")
    RETURN_NAMES = ("character_prompt", "preview_image")
    FUNCTION = "run"
    CATEGORY = "Prompting/Anime Character"

    def run(self, character):
        char_prompt = character
        preview_image = None
        # Find preview
        for entry in self.char_data:
            if isinstance(entry, dict) and character in entry:
                value = entry[character]
                preview_data = value if isinstance(value, str) and value.startswith("data:image") else entry.get("preview", "")
                if isinstance(preview_data, str) and preview_data.startswith("data:image"):
                    try:
                        base64_data = preview_data.split("base64,", 1)[1]
                        preview_image = self.decode_base64_to_image(base64_data)
                    except Exception as e:
                        print(f"[CharacterPromptNode] ⚠️ Base64 decode failed for {character}: {e}")
                break
        return (char_prompt, preview_image)

    def decode_base64_to_image(self, base64_str):
        data = base64.b64decode(base64_str)
        try:
            from comfy.utils import pil_to_tensor
            return pil_to_tensor(Image.open(BytesIO(data)).convert("RGB"))
        except Exception as e:
            raise ValueError("Failed to decode base64 image") 
