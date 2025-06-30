// ComfyUI/custom_nodes/ComfyUI_AnimeCharacterSelect/js/enhanced_prompt.js

function insertIntoPrompt(promptField, text) {
    if (!promptField || !text) return;
    // Only add if it's not already at the start
    if (!promptField.value.trim().startsWith(text)) {
        if (promptField.value.trim().length > 0) {
            promptField.value += ", " + text;
        } else {
            promptField.value = text;
        }
        promptField.dispatchEvent(new Event("input", { bubbles: true }));
    }
}

function setupLiveInsert() {
    document.querySelectorAll(".comfy-control").forEach(container => {
        const label = container.querySelector("label");
        const select = container.querySelector("select");
        let promptField = null;
        if (container.parentElement) {
            promptField = container.parentElement.querySelector("textarea");
        }
        if (!label || !select || !promptField) return;

        if (select.dataset._enhanced) return;
        select.dataset._enhanced = "true";

        // For character or action
        if (label.innerText.includes("Select the character to insert") ||
            label.innerText.includes("Select the action to insert")) {
            select.addEventListener("change", () => {
                const value = select.value;
                if (value && !value.startsWith("Select")) {
                    insertIntoPrompt(promptField, value);
                    select.value = select.options[0].value; // Reset to top
                    select.dispatchEvent(new Event("change"));
                }
            });
        }
    });
}

if (document.readyState !== "loading") setupLiveInsert();
else document.addEventListener("DOMContentLoaded", setupLiveInsert);

const observer = new MutationObserver(setupLiveInsert);
observer.observe(document.body, { childList: true, subtree: true });
