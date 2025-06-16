import os
import json

class AnimeCharacterPromptNode:
    """Anime Character + Action Prompt Builder"""

    # Zet hier je paden naar de bestanden (pas eventueel aan)
    CHARACTER_JSON = os.path.join(os.path.dirname(__file__), "output_1.json")
    ACTION_JSON = os.path.join(os.path.dirname(__file__), "action.json")

    # Voorladen
    try:
    with open(CHARACTER_JSON, "r", encoding="utf-8") as f:
        char_data = json.load(f)
    with open(ACTION_JSON, "r", encoding="utf-8") as f:
        action_data = json.load(f)
except Exception as e:
    print("❌ Fout bij het laden van JSON-bestanden:", e)
    char_data = []
    action_data = {}

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "character": (cls.CHAR_NAMES,),
                "action": (cls.ACTION_NAMES,),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
    FUNCTION = "build_prompt"
    CATEGORY = "Prompting/Anime Character"

    def build_prompt(self, character, action):
        char_prompt = ""
        action_prompt = ""

        for entry in self.char_data:
            if character in entry:
                char_prompt = entry[character]
                break

        action_prompt = self.action_data.get(action, "")

        final_prompt = f"{char_prompt}, {action_prompt}".strip(", ")

        return (final_prompt,)

NODE_CLASS_MAPPINGS = {
    "AnimeCharacterPromptNode": AnimeCharacterPromptNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AnimeCharacterPromptNode": "Anime Character + Action Prompt"
}
