class CombinePromptStringsNode:
    """
    Node: Combines character prompt, action prompt, and extra prompt into one string.
    Connect the outputs of CharacterPromptNode and ActionPromptNode here, plus any extra prompt string.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "character_prompt": ("STRING", {"multiline": True, "default": ""}),
                "action_prompt": ("STRING", {"multiline": True, "default": ""}),
                "extra_prompt": ("STRING", {"multiline": True, "default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
    FUNCTION = "run"
    CATEGORY = "Prompting/Anime Character"

    def run(self, character_prompt, action_prompt, extra_prompt):
        parts = [p.strip() for p in [character_prompt, action_prompt, extra_prompt] if p and p.strip()]
        prompt = ", ".join(parts)
        return (prompt,)

# Usage: Connect the outputs of CharacterPromptNode and ActionPromptNode, plus any extra string (or leave empty), to this node for your final prompt.
