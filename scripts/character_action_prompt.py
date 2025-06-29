
import os
import json
import base64

class MinimalCharacterActionPrompt:
    """Minimal node: select character + action, output prompt + preview image"""

    # Laad JSON-bestanden
    CHARACTER_JSON = os.path.join(os.path.dirname(__file__), "output_1.json")
    ACTION_JSON = os.path.join(os.path.dirname(__file__), "action.json")

    try:
        with open(CHARACTER_JSON, "r", encoding="utf-8") as f:
            char_data = json.load(f)
        with open(ACTION_JSON, "r", encoding="utf-8") as f:
            action_data = json.load(f)
    except Exception as e:
        print("❌ JSON load error:", e)
        char_data = []
        action_data = {}

    CHARACTERS = [list(entry.keys())[0] for entry in char_data]
    ACTIONS = list(action_data.keys())

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "character": (cls.CHARACTERS,),
                "action": (cls.ACTIONS,),
            }
        }

    RETURN_TYPES = ("STRING", "STRING",)
    RETURN_NAMES = ("prompt", "preview_image_base64",)
    FUNCTION = "build_prompt"
    CATEGORY = "Prompting/Anime Character"

    def build_prompt(self, character, action):
        char_prompt = ""
        preview_image = ""
        action_prompt = self.action_data.get(action, "")

        for entry in self.char_data:
            if character in entry:
                char_prompt = entry[character]
                if "preview" in entry:
                    img_path = os.path.join(os.path.dirname(__file__), entry["preview"])
                    if os.path.isfile(img_path):
                        with open(img_path, "rb") as img:
                            preview_image = base64.b64encode(img.read()).decode("utf-8")
                break

        final_prompt = f"{char_prompt}, {action_prompt}".strip(", ")
        return (final_prompt, preview_image)

NODE_CLASS_MAPPINGS = {
    "MinimalCharacterActionPrompt": MinimalCharacterActionPrompt
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MinimalCharacterActionPrompt": "Character + Action Prompt (Minimal)"
}
