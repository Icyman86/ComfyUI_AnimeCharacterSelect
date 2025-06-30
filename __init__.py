import os
import json
import base64
from PIL import Image
from io import BytesIO

import nodes
# Register JS web dir for custom hook
nodes.EXTENSION_WEB_DIRS["ComfyUI_AnimeCharacterSelect"] = os.path.join(os.path.dirname(__file__), "js")

class EnhancedCharacterPromptNode:
    """ComfyUI node: select character + action, show preview image, editable prompt (live insert), output prompt + conditioning"""

    # Load all character/action data on class load
    CHARACTER_JSON_FILES = [
        os.path.join(os.path.dirname(__file__), f"output_{i}.json") for i in range(1, 12)
    ]
    ACTION_JSON = os.path.join(os.path.dirname(__file__), "action.json")

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
                "character": (["Select character..."] + cls.CHARACTERS,),
                "action": (["Select action..."] + cls.ACTIONS,),
                "clip": ("CLIP",),
            }
        }

    RETURN_TYPES = ("STRING", "IMAGE", "CONDITIONING")
    RETURN_NAMES = ("prompt", "preview_image", "conditioning")
    FUNCTION = "build_prompt"
    CATEGORY = "Prompting/Anime Character"

    def build_prompt(self, prompt, character, action, clip):
        # Lookup preview image for character
        preview_image = None
        if character and character != "Select character...":
            for entry in self.char_data:
                if isinstance(entry, dict) and character in entry:
                    value = entry[character]
                    preview_data = value if isinstance(value, str) and value.startswith("data:image") else entry.get("preview", "")
                    if preview_data and preview_data.startswith("data:image"):
                        try:
                            base64_data = preview_data.split("base64,", 1)[1]
                            preview_image = self.decode_base64_to_image(base64_data)
                        except Exception as e:
                            print(f"⚠️ Base64 decode failed for {character}: {e}")
                    break

        # Prompt is fully user-editable: whatever is in the text field is what you get!
        final_prompt = prompt.strip()
        conditioning_output = []
        if clip and final_prompt:
            try:
                cross_attn = clip.encode(final_prompt)
                conditioning_output = [(cross_attn, {})]
            except Exception as e:
                print(f"⚠️ CLIP encode failed: {e}")

        return (final_prompt, preview_image, conditioning_output)

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
