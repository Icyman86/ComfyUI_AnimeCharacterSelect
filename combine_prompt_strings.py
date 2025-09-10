class CombinePromptStringsNode:
    """Combine up to three character prompts with optional action/extra prompts."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "character_1": ("STRING", {"multiline": False, "default": ""}),
                "character_2": ("STRING", {"multiline": False, "default": ""}),
                "character_3": ("STRING", {"multiline": False, "default": ""}),
                "action_prompt": ("STRING", {"multiline": True, "default": ""}),
                "extra_prompt": ("STRING", {"multiline": True, "default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
    FUNCTION = "run"
    CATEGORY = "Prompting/Anime Character"

    def run(
        self,
        character_1="",
        character_2="",
        character_3="",
        action_prompt="",
        extra_prompt="",
    ):
        parts = [
            p.strip()
            for p in [
                character_1,
                character_2,
                character_3,
                action_prompt,
                extra_prompt,
            ]
            if p and p.strip()
        ]

        prompt = ", ".join(parts)
        return (prompt,)

# Usage: Connect the outputs of up to three CharacterPromptNodes and an
# ActionPromptNode, plus any extra string (or leave empty), to this node for
# your final prompt.
