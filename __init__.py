from .action_prompt_node import ActionPromptNode
from .character_prompt_node import CharacterPromptNode
from .combine_prompt_strings import CombinePromptStringsNode

NODE_CLASS_MAPPINGS = {
    "ActionPromptNode": ActionPromptNode,
    "CharacterPromptNode": CharacterPromptNode,
    "CombinePromptStringsNode": CombinePromptStringsNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ActionPromptNode": "Action Prompt (Editable)",
    "CharacterPromptNode": "Character Prompt + Image",
    "CombinePromptStringsNode": "Combine Prompt Strings",
}
