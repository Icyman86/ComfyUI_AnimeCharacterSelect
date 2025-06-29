// enhanced_prompt.js
function insertIntoPrompt(promptField, text) {
    if (!promptField || !text) return;
    if (promptField.value.trim().length > 0) {
        promptField.value += ", " + text;
    } else {
        promptField.value = text;
    }
    // Zorg dat ComfyUI ziet dat het veld veranderd is
    promptField.dispatchEvent(new Event("input", { bubbles: true }));
}

function setupEnhancedPromptHook() {
    const observer = new MutationObserver(() => {
        document.querySelectorAll(".node").forEach(nodeEl => {
            const labelEls = nodeEl.querySelectorAll("label");
            let promptField = nodeEl.querySelector("textarea");

            if (!promptField) return;

            labelEls.forEach(label => {
                const text = label.textContent.trim();
                if (text === "Select to add Character" || text === "Select to add Action") {
                    const select = label.parentElement.querySelector("select");
                    if (!select || select.dataset.hooked) return;

                    select.dataset.hooked = "true";

                    select.addEventListener("change", () => {
                        const value = select.value;
                        if (value && !value.startsWith("Select")) {
                            insertIntoPrompt(promptField, value);
                            select.value = select.options[0].value;
                            select.dispatchEvent(new Event("change")); // Reset dropdown
                        }
                    });
                }
            });
        });
    });

    observer.observe(document.body, { childList: true, subtree: true });
}

if (document.readyState !== "loading") setupEnhancedPromptHook();
else document.addEventListener("DOMContentLoaded", setupEnhancedPromptHook);
