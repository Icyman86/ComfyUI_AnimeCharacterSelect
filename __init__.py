import os
import json
import base64
from PIL import Image
from io import BytesIO

class EnhancedCharacterPromptNode:
    """ComfyUI node: kies character + action, toon preview image, output prompt + conditioning"""

    # JSON-bestanden met characters en actions
    CHARACTER_JSON_FILES = [
        os.path.join(os.path.dirname(__file__), f"output_{i}.json") for i in range(1, 12)
    ]
    ACTION_JSON = os.path.join(os.path.dirname(__file__), "action.json")

    # Class-variabelen voor data en dropdowns
    char_data = []
    action_data = {}
    CHARACTERS = []
    ACTIONS = []

    # Laad JSON data zodra class geladen wordt
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

    # Vul dropdown lijsten op basis van geladen data
    CHARACTERS = [list(entry.keys())[0] for entry in char_data if isinstance(entry, dict) and len(entry) >= 1]
    ACTIONS = list(action_data.keys())

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "character": (cls.CHARACTERS,),
                "action": (cls.ACTIONS,),
                "extra_prompt": ("STRING", {"multiline": True, "default": ""}),
                "clip": ("CLIP",),  # optioneel, voor conditioning
            }
        }

    RETURN_TYPES = ("STRING", "IMAGE", "CONDITIONING")
    RETURN_NAMES = ("prompt", "preview_image", "CONDITIONING")
    FUNCTION = "build_prompt"
    CATEGORY = "Prompting/Anime Character"

def build_prompt(self, character, action, extra_prompt, clip):
    char_prompt = ""
    action_prompt = self.action_data.get(action, "")
    preview_image = None

    for entry in self.char_data:
        if isinstance(entry, dict) and character in entry:
            value = entry[character]
            if isinstance(value, str) and value.startswith("data:image"):
                char_prompt = character
                preview_data = value
            else:
                char_prompt = value
                preview_data = entry.get("preview", "")

            if isinstance(preview_data, str) and preview_data.startswith("data:image"):
                try:
                    base64_data = preview_data.split("base64,", 1)[1]
                    preview_image = self.decode_base64_to_image(base64_data)
                except Exception as e:
                    print(f"⚠️ Base64 decode failed for {character}: {e}")
            break

    final_prompt = ", ".join(p for p in [char_prompt, action_prompt, extra_prompt] if p).strip()

    conditioning_output = None
    if clip:
        try:
            cond = clip.encode(final_prompt)
            # ComfyUI expects: [(cross_attn_tensor, extra_dict)]
            conditioning_output = [(cond, {})]
        except Exception as e:
            print(f"⚠️ CLIP encode failed: {e}")

    return (final_prompt, preview_image, conditioning_output)


    def decode_base64_to_image(self, base64_str):
        data = base64.b64decode(base64_str)
        try:
            img = Image.open(BytesIO(data)).convert("RGB")
        except Exception as e:
            raise ValueError("Failed to decode base64 image") from e
        return img


NODE_CLASS_MAPPINGS = {
    "EnhancedCharacterPromptNode": EnhancedCharacterPromptNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EnhancedCharacterPromptNode": "Character + Action Prompt + Preview",
}
