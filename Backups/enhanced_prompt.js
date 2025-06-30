console.log("EnhancedPromptNode JS loaded!")
function updatePromptValue(textarea, value) {
    if (!textarea || !value || value.startsWith("Select")) return;
    const existing = textarea.value.trim();
    const parts = existing.length > 0 ? existing.split(",").map(p => p.trim()) : [];
    if (!parts.includes(value)) {
        parts.push(value);
        textarea.value = parts.join(", ");
        textarea.dispatchEvent(new Event("input", { bubbles: true }));
    }
}

function setupLiveCharacterActionPromptHook() {
    const observer = new MutationObserver(() => {
        document.querySelectorAll(".comfy-control").forEach(container => {
            const label = container.querySelector("label");
            const select = container.querySelector("select");

            if (!label || !select) return;

            const labelText = label.innerText.trim();
            if (
                (labelText.includes("Select to add Character") || labelText.includes("Select to add Action")) &&
                !select.dataset._enhanced_hooked
            ) {
                select.dataset._enhanced_hooked = "true";
                select.addEventListener("change", () => {
                    const node = container.closest(".node");
                    if (!node) return;

                    const textarea = node.querySelector("textarea");
                    if (!textarea) return;

                    const selectedValue = select.value;
                    updatePromptValue(textarea, selectedValue);
                });
            }
        });
    });

    observer.observe(document.body, { childList: true, subtree: true });
}

if (document.readyState !== "loading") {
    setupLiveCharacterActionPromptHook();
} else {
    document.addEventListener("DOMContentLoaded", setupLiveCharacterActionPromptHook);
}
