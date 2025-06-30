// enhanced_prompt.js
// For ComfyUI_AnimeCharacterSelect — live insert from dropdown to prompt field

(function () {
    // Wait until ComfyUI is fully loaded
    function setup() {
        // Scan for our node panels every second (ComfyUI reactivity is slow)
        setInterval(() => {
            document.querySelectorAll(".node").forEach(node => {
                // Only patch nodes with our label!
                const header = node.querySelector('.node_title');
                if (!header || !header.innerText.includes("Character + Action Prompt")) return;

                // Get our widgets inside the node
                const selects = node.querySelectorAll("select");
                const textarea = node.querySelector("textarea.comfy-multiline-input");
                if (!textarea) return;

                // Attach only once
                if (node.dataset.enhancedPromptPatched) return;
                node.dataset.enhancedPromptPatched = "true";

                selects.forEach(select => {
                    select.addEventListener("change", function () {
                        const value = this.value;
                        if (!value || value.startsWith("Select")) return;

                        // Only append if not already present (prevent repeats)
                        let text = textarea.value.trim();
                        // Only add if not already at the start
                        if (!text.includes(value)) {
                            textarea.value = text.length > 0 ? text + ", " + value : value;
                            // Fire event so ComfyUI sees the change
                            textarea.dispatchEvent(new Event("input", { bubbles: true }));
                        }
                        // Reset dropdown to first item (optional)
                        this.selectedIndex = 0;
                    });
                });
            });
        }, 1000); // ComfyUI sometimes destroys/rebuilds node UIs
    }

    // Run after page load
    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", setup);
    } else {
        setup();
    }
})();
