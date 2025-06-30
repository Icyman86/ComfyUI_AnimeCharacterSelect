// comfyui-animecharacterselect/js/enhanced_prompt.js

console.log("EnhancedPrompt JS Loaded");

function insertIntoPrompt(node, dropdownName) {
    // Zoek het promptveld (textarea) en de dropdown
    const promptWidget = node.widgets.find(w => w.name === "prompt");
    const dropdownWidget = node.widgets.find(w => w.name === dropdownName);
    if (!promptWidget || !dropdownWidget) return;

    const promptInput = promptWidget.inputEl;
    const selectInput = dropdownWidget.inputEl;
    if (!promptInput || !selectInput) return;

    selectInput.addEventListener("change", () => {
        const value = selectInput.value;
        if (value && !value.startsWith("Select")) {
            let current = promptInput.value.trim();
            // Voeg toe als niet al aanwezig
            if (!current.includes(value)) {
                if (current.length > 0) {
                    current += ", " + value;
                } else {
                    current = value;
                }
                promptInput.value = current;
                promptWidget.value = current;
                promptInput.dispatchEvent(new Event("input", { bubbles: true }));
            }
            // Reset dropdown
            selectInput.value = selectInput.options[0].value;
            selectInput.dispatchEvent(new Event("change"));
        }
    });
}

// Hook in op Node create/update
app.registerExtension({
    name: "ComfyUI_AnimeCharacterSelect",
    nodeCreated(node) {
        // Je node heet "EnhancedCharacterPromptNode"
        if (node.type === "EnhancedCharacterPromptNode") {
            insertIntoPrompt(node, "Select to add Character");
            insertIntoPrompt(node, "Select to add Action");
        }
    },
    nodeRenamed(node) {
        if (node.type === "EnhancedCharacterPromptNode") {
            insertIntoPrompt(node, "Select to add Character");
            insertIntoPrompt(node, "Select to add Action");
        }
    }
});
