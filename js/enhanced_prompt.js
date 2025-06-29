// enhanced_prompt.js

function insertIntoPrompt(promptField, text) {
    if (!promptField || !text) return;
    if (promptField.value.trim().length > 0) {
        promptField.value += ", " + text;
    } else {
        promptField.value = text;
    }
    promptField.dispatchEvent(new Event("input", { bubbles: true }));
}

function setupLiveInsert() {
    const observer = new MutationObserver(() => {
        document.querySelectorAll(".comfy-control").forEach(container => {
            const label = container.querySelector("label");
            const select = container.querySelector("select");
            const promptField = container.parentElement.querySelector("textarea");

            if (!label || !select || !promptField) return;

            if (label.innerText.includes("Select to add Character") || label.innerText.includes("Select to add Action")) {
                if (select.dataset._enhanced) return; // Already hooked
                select.dataset._enhanced = "true";

                select.addEventListener("change", () => {
                    const value = select.value;
                    if (value && !value.startsWith("Select")) {
                        insertIntoPrompt(promptField, value);
                        select.value = select.options[0].value;
                        select.dispatchEvent(new Event("change"));
                    }
                });
            }
        });
    });

    observer.observe(document.body, { childList: true, subtree: true });
}

if (document.readyState !== "loading") setupLiveInsert();
else document.addEventListener("DOMContentLoaded", setupLiveInsert);
