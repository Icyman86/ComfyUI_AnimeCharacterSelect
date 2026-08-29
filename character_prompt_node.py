import os
import json
import base64
import torch
import numpy as np
from PIL import Image
from io import BytesIO
import folder_paths
from server import PromptServer
from aiohttp import web

# ---- GLOBAAL (buiten class) ----
CHARACTER_FOLDER = os.path.dirname(__file__)
CHARACTER_JSON_FILES = [
    os.path.join(CHARACTER_FOLDER, f)
    for f in os.listdir(CHARACTER_FOLDER)
    if f.startswith("dictoutput") and f.endswith(".json")
]

class CharacterPromptNode:
    # --- INJECTED CACHE SETUP ---
    # Create local directory to hold physical .png snapshots
    CACHE_DIR = os.path.join(folder_paths.get_output_directory(), "anime_character_thumbs")
    os.makedirs(CACHE_DIR, exist_ok=True)
    # -----------------------------
    """
    Node: Character selection for anime prompts.
    Non-editable output string, includes preview image (base64 in output_X.json).
    """

#    char_data = []
    CHARACTERS = []
    DATA = {}

    try:
        for path in CHARACTER_JSON_FILES:
            with open(path, "r", encoding="utf-8") as f:
                DATA.update( json.load(f) )
    except Exception as e:
        print(f"[CharacterPromptNode] ?? Error loading {path}: {e}")

    #CHARACTERS = [list(entry.keys())[0] for entry in char_data if isinstance(entry, dict) and len(entry) >= 1]
    CHARACTERS = list(DATA.keys())

    # --- INJECTED BULK EXTRACTION ---
    # Dump base64 data strings out into real image files once on boot
    for name, cdata in DATA.items():
        try:
            b64_str = cdata['image']
            if b64_str:
                if "," in b64_str:
                    b64_str = b64_str.split(",")[-1]
                safe_name = "".join([c if c.isalnum() else "_" for c in name]) + ".png"
                file_path = os.path.join(CACHE_DIR, safe_name)
#                print(file_path)
                if not os.path.exists(file_path):
                    img_data = base64.b64decode(b64_str)
                    with open(file_path, "wb") as img_file:
                        img_file.write(img_data)
        except Exception as e:
            print(f"[CharacterPromptNode] Batch image extraction failed for {name}: {e}")
    # ---------------------------------



    RETURN_TYPES = ("STRING", "IMAGE")
    RETURN_NAMES = ("character_prompt", "preview_image")
    FUNCTION = "run"
    CATEGORY = "Prompting/Anime Character"
    # Tells ComfyUI's frontend canvas to reserve space for image drawings
    OUTPUT_NODE = True 
    # create Filters
    FILTER_OPTIONS =["ALL",]
    for ele in CHARACTERS:
      x = ele.split(',')[0].strip()
      if x not in FILTER_OPTIONS:
        FILTER_OPTIONS.append(x)



    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                # Dropdown 1: The Category Filter
                "category_filter": (cls.FILTER_OPTIONS, {"default": "ALL"}),
                
                # Dropdown 2: Your original master list of 1000+ items
                "character": (cls.CHARACTERS,), 
            }
        }


    # THE DYNAMIC DROPDOWN FILTER ENGINE (Executed natively by ComfyUI frontend)
    # The exact name 'get_dynamic_characters' maps to our method definition
    @classmethod
    def get_dynamic_characters(cls, category_filter="ALL", **kwargs):
        # If 'ALL' is chosen, combine all lists to show every single item
        if category_filter == "ALL":
            all_characters = []
            for character_list in cls.DATA.values():
                all_characters.extend(character_list)
            return all_characters
        
        # Otherwise, instantly fetch only the array belonging to that specific category
        return cls.DATA.get(category_filter, ["-- No Characters Found --"])




    # THIS IS THE MAGIC JAVASCRIPT/PYTHON TRIGGER FOR MODERN COMFYUI
    # When filter_category changes, this dynamically rewrites the 'character' dropdown options
    @classmethod
    def VALIDATE_INPUTS(cls, category_filter, character):
        return True


    def execute(self, filter_category, character):
        # Your normal node generation code continues here...
        print(f"Selected Character: {character}")
        return (character,)
    
    def run(self, character, **kwargs):
        char_prompt = self.DATA[character]['prompt']
        preview_image = None
        if 1:
                value = self.DATA[character]['image']
                preview_data = value if isinstance(value, str) and value.startswith("data:image") else None
                if isinstance(preview_data, str) and preview_data.startswith("data:image"):
                    try:
                        base64_data = preview_data.split("base64,", 1)[1]
                        preview_image = self.decode_base64_to_image(base64_data)
                    except Exception as e:
                        print(f"[CharacterPromptNode] ?? Base64 decode failed for {character}: {e}")
        return (char_prompt, preview_image)

    def decode_base64_to_image(self, base64_str):
        data = base64.b64decode(base64_str)
        try:
            img = Image.open(BytesIO(data)).convert("RGB")
            # Convert to ComfyUI IMAGE format: torch.Tensor (B, H, W, C), float32, [0,1]
            img_np = np.array(img).astype(np.float32) / 255.0
            return torch.from_numpy(img_np).unsqueeze(0)
        except Exception as e:
            raise ValueError("Failed to decode base64 image") from e
            
# --- INJECTED HTTP ROUTE ---
# Web service endpoint to supply frontend cache loads
@PromptServer.instance.routes.get("/anime_character_select/get_thumb")
async def get_thumb(request):
    character = request.query.get("character", "")
    safe_name = "".join([c if c.isalnum() else "_" for c in character]) + ".png"
    file_path = os.path.join(CharacterPromptNode.CACHE_DIR, safe_name)
    
    if os.path.exists(file_path):
        return web.FileResponse(file_path)
    return web.Response(status=404)
# ---------------------------
