import os
import json
import nodes

nodes.EXTENSION_WEB_DIRS["ComfyUI_AnimeCharacterSelect"] = os.path.join(os.path.dirname(__file__), "js")

class ActionPromptNode:
    ACTION_JSON = os.path.join(os.path.dirname(__file__), "action.json")
    ACTION_LABELS = []
    ACTION_PROMPTS = {}

    try:
        with open(ACTION_JSON, "r", encoding="utf-8") as f:
            _data = json.load(f)
            ACTION_LABELS = list(_data.keys())
            ACTION_PROMPTS = _data
    except Exception as e:
        print("Error loading action.json:", e)
        ACTION_LABELS = ["No actions found"]
        ACTION_PROMPTS = {}

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "action_selector": (cls.ACTION_LABELS,),
                "action_prompt": ("STRING", {"multiline": True, "default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("action_prompt",)
    FUNCTION = "set_prompt"
    CATEGORY = "Prompting/Anime"

    def set_prompt(self, action_selector, action_prompt):
        # Always output the editable prompt field, not the selector
        return (action_prompt,)
