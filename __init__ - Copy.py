import os
import json
import base64

class MinimalCharacterActionPrompt:
    """Minimal node: select character + action, output prompt + preview image"""

    # Verzamel alle JSON-bestanden (output_1.json t/m output_11.json)
    CHARACTER_JSON_FILES = [
        os.path.join(os.path.dirname(__file__), f"output_{i}.json") for i in range(1, 12)
    ]
    ACTION_JSON = os.path.join(os.path.dirname(__file__), "action.json")

    # Initialiseer class variables
    char_data = []
    action_data = {}
    CHARACTERS = []
    ACTIONS = []

    # Laad JSON-data bij class loading
    try:
        for path in CHARACTER_JSON_FILES:
            with open(path, "r", encoding="utf-8") as f:
                char_data.extend(json.load(f))
        with open(ACTION_JSON, "r", encoding="utf-8") as f:
            action_data = json.load(f)

        CHARACTERS = [list(entry.keys())[0] for entry in char_data]
        ACTIONS = list(action_data.keys())
    except Exception as e:
        print("❌ JSON load error:", e)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "character": (cls.CHARACTERS,),
                "action": (cls.ACTIONS,),
                "extra_prompt": ("STRING", {"multiline": True, "default": ""}),
                "clip": ("CLIP",),  # Alleen voor compatibiliteit
            }
        }

    RETURN_TYPES = ("STRING", "STRING",)
    RETURN_NAMES = ("prompt", "preview_image_base64",)
    FUNCTION = "build_prompt"
    CATEGORY = "Prompting/Anime Character"

    def build_prompt(self, character, action, extra_prompt, clip):
        char_prompt = ""
        preview_image = ""
        action_prompt = self.action_data.get(action, "")

        for entry in self.char_data:
            if character in entry:
                char_prompt = entry[character]
                if "preview" in entry:
                    img_path = os.path.join(os.path.dirname(__file__), entry["preview"])
                    if os.path.isfile(img_path):
                        try:
                            with open(img_path, "rb") as img:
                                preview_image = base64.b64encode(img.read()).decode("utf-8")
                        except Exception as e:
                            print(f"❌ Fout bij laden preview afbeelding voor {character}:", e)
                break

        final_prompt = ", ".join(filter(None, [char_prompt, action_prompt, extra_prompt]))
        return (final_prompt, preview_image)

NODE_CLASS_MAPPINGS = {
    "MinimalCharacterActionPrompt": MinimalCharacterActionPrompt
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MinimalCharacterActionPrompt": "Character + Action Prompt (WIP)"
}
