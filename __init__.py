import os
import json
import base64
import numpy as np
import torch
import cv2

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
    RETURN_NAMES = ("prompt", "preview_image", "conditioning")
    FUNCTION = "build_prompt"
    CATEGORY = "Prompting/Anime Character"

    def build_prompt(self, character, action, extra_prompt, clip):
        char_prompt = ""
        action_prompt = self.action_data.get(action, "")
        image_tensor = None

        for entry in self.char_data:
            if isinstance(entry, dict) and character in entry:
                char_prompt = entry[character]
                preview_data = entry.get("preview", "")
                if preview_data.startswith("data:image"):
                    try:
                        base64_data = preview_data.split("base64,", 1)[1]
                        image_tensor = self.decode_base64_to_tensor(base64_data)
                    except Exception as e:
                        print(f"⚠️ Base64 decode failed for {character}: {e}")
                break

        final_prompt = ", ".join(p for p in [char_prompt, action_prompt, extra_prompt] if p).strip()

        # Conditionering via CLIP als beschikbaar
        conditioning = clip.encode(final_prompt) if clip else None

        return (final_prompt, image_tensor, conditioning)

    def decode_base64_to_tensor(self, base64_str):
        nparr = np.frombuffer(base64.b64decode(base64_str), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)
        if img is None:
            raise ValueError("Failed to decode base64 image")
        if img.shape[2] == 4:
            alpha = img[:, :, 3]
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
            mask = torch.from_numpy((alpha / 255.0).astype(np.float32)).unsqueeze(0)
        else:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            mask = torch.ones((1, img.shape[0], img.shape[1]), dtype=torch.float32)

        img = img.astype(np.float32) / 255.0
        img_tensor = torch.from_numpy(img).permute(2, 0, 1).unsqueeze(0)  # [1, 3, H, W]
        return img_tensor


NODE_CLASS_MAPPINGS = {
    "EnhancedCharacterPromptNode": EnhancedCharacterPromptNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EnhancedCharacterPromptNode": "Character + Action Prompt + Preview",
}
