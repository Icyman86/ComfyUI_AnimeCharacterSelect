app.registerExtension({
    name: "ComfyUI_AnimeCharacterSelect_action_prompt",
    beforeWidgetRender: async ({ widget, node }) => {
        // Only on first render of action_prompt textarea
        if (widget.name !== "action_prompt") return;
        const textarea = widget.inputEl;
        if (!textarea) return;

        // Find dropdown widget for action_selector
        const dropdown = node.widgets.find(w => w.name === "action_selector");
        if (!dropdown || !dropdown.inputEl) return;

        // Build a lookup table (Action label => Prompt)
        let promptMap = {};
        try {
            // Try to read the map from the backend (Comfy passes extra_data sometimes)
            if (dropdown.options && dropdown.options.length > 0) {
                dropdown.options.forEach((opt, idx) => {
                    // Only works if promptMap is sent via extra_data or a hidden input.
                });
            }
        } catch (e) { /* fallback below */ }

        // Hard-coded for testing (for production, inject from Python via extra_data if possible)
        // Example (you should auto-inject this from .py as extra_data or as a hidden field!)
        promptMap = {
            "Cheering": "A girl cheering, hands up, energetic, smiling",
            "Sleeping": "A girl sleeping on her school desk, peaceful, drooling"
            // ... and so on, matching your action.json
        };

        dropdown.inputEl.addEventListener("change", () => {
            const selected = dropdown.inputEl.value;
            const prompt = promptMap[selected] || "";
            textarea.value = prompt;
            widget.value = prompt;
            textarea.dispatchEvent(new Event("input", { bubbles: true }));
        });
    }
});
