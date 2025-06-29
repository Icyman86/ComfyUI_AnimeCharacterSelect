import os
import json
import base64
from PIL import Image
from io import BytesIO

import nodes  # Register JS directory
nodes.EXTENSION_WEB_DIRS["ComfyUI_AnimeCharacterSelect"] = os.path.join(os.path.dirname(__file__), "js")


class EnhancedCharacterPromptNode:
    """ComfyUI node: select character + action, show preview image, output prompt + conditioning"""

    # JSON files with characters and actions
    CHARACTER_JSON_FILES = [
        os.path.join(os.path.dirname(__file__), f"output_{i}.json") for i in range(1, 12)
    ]
    ACTION_JSON = os.path.join(os.path.dirname(__file__), "action.json")

    # Class variables for data and dropdowns
    char_data = []
    action_data = {}
    CHARACTERS = []
    ACTIONS = []

    try:
        for path in CHARACTER_JSON_FILES:
            with open(path, "r", encoding="utf-8") as f:
                char_data.extend(json.load(f))
    except Exception as e:
        print(f"⚠️ Error loading {path}: {e}")

    try:
        with open(ACTION_JSON, "r", encoding="utf-8") as f:
            action_data = json.load(f)
    except Exception as e:
        print("❌ Error loading action.json:", e)

    CHARACTERS = [list(entry.keys())[0] for entry in char_data if isinstance(entry, dict) and len(entry) >= 1]
    ACTIONS = list(action_data.keys())

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True, "dynamicPrompts": False, "default": ""}),
                "Select to add Character": (["Select the character to insert"] + cls.CHARACTERS,),
                "Select to add Action": (["Select the action to insert"] + cls.ACTIONS,),
                "clip": ("CLIP",),
            }
        }

    RETURN_TYPES = ("STRING", "IMAGE", "CONDITIONING")
    RETURN_NAMES = ("prompt", "preview_image", "conditioning")
    FUNCTION = "build_prompt"
    CATEGORY = "Prompting/Anime Character"

    def build_prompt(self, prompt, **kwargs):
        selected_char = kwargs.get("Select to add Character", None)
        selected_act = kwargs.get("Select to add Action", None)
        clip = kwargs.get("clip")

        preview_image = None
        char_prompt = ""
        action_prompt = ""

        for entry in self.char_data:
            if isinstance(entry, dict) and selected_char in entry:
                value = entry[selected_char]
                if isinstance(value, str) and value.startswith("data:image"):
                    char_prompt = selected_char
                    preview_data = value
                else:
                    char_prompt = value
                    preview_data = entry.get("preview", "")

                if isinstance(preview_data, str) and preview_data.startswith("data:image"):
                    try:
                        base64_data = preview_data.split("base64,", 1)[1]
                        preview_image = self.decode_base64_to_image(base64_data)
                    except Exception as e:
                        print(f"⚠️ Base64 decode failed for {selected_char}: {e}")
                break

        action_prompt = self.action_data.get(selected_act, "")

        # Logging to help debug
        print(f"[DEBUG] char_prompt: {char_prompt}")
        print(f"[DEBUG] action_prompt: {action_prompt}")
        print(f"[DEBUG] input prompt: {prompt}")

        # Build the live-updated editable prompt
        new_prompt_parts = [char_prompt, action_prompt]
        combined_prompt = ", ".join([p for p in new_prompt_parts if p])

        if prompt.strip():
            if combined_prompt:
                prompt = combined_prompt + ", " + prompt
        else:
            prompt = combined_prompt

        print(f"[DEBUG] final prompt: {prompt}")

        conditioning_output = []
        if clip:
            try:
                cross_attn = clip.encode(prompt)
                # pooled = clip.encode_pooled(prompt)  # disabled for now due to missing method
                # cond_dict = {"pooled_output": pooled}
                cond_dict = {}
                conditioning_output = [(cross_attn, cond_dict)]
            except Exception as e:
                print(f"⚠️ CLIP encode failed: {e}")

        return (prompt, preview_image, conditioning_output)

    def decode_base64_to_image(self, base64_str):
        data = base64.b64decode(base64_str)
        try:
            from comfy.utils import pil_to_tensor
            return pil_to_tensor(Image.open(BytesIO(data)).convert("RGB"))
        except Exception as e:
            raise ValueError("Failed to decode base64 image") from e


NODE_CLASS_MAPPINGS = {
    "EnhancedCharacterPromptNode": EnhancedCharacterPromptNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EnhancedCharacterPromptNode": "Character + Action Prompt (Live Insert)",
}
