app.registerExtension({
  name: "ComfyUI_AnimeCharacterSelect",

  beforeRegisterNodeDef(nodeType, nodeData, app) {
    if (nodeData.name !== "EnhancedCharacterPromptNode") return;

    const originalOnNodeCreated = nodeType.onNodeCreated;
    nodeType.onNodeCreated = function (node, app) {
      if (originalOnNodeCreated) originalOnNodeCreated(node, app);

      const promptWidget = node.widgets?.find(w => w.name === "prompt");
      const charWidget = node.widgets?.find(w => w.name === "Select to add Character");
      const actionWidget = node.widgets?.find(w => w.name === "Select to add Action");

      const insertValue = (value) => {
        if (!promptWidget || !promptWidget.inputEl) return;
        if (!value || value.startsWith("Select")) return;
        const current = promptWidget.inputEl.value;
        const toInsert = value;
        if (current && !current.includes(toInsert)) {
          const updated = current.trim().length > 0 ? current + ", " + toInsert : toInsert;
          promptWidget.inputEl.value = updated;
          promptWidget.value = updated;
          promptWidget.inputEl.dispatchEvent(new Event("input", { bubbles: true }));
        }
      };

      if (charWidget && charWidget.inputEl) {
        charWidget.inputEl.addEventListener("change", () => {
          const value = charWidget?.extra?.[charWidget.value] ?? charWidget.value;
          insertValue(value);
        });
      }

      if (actionWidget && actionWidget.inputEl) {
        actionWidget.inputEl.addEventListener("change", () => {
          const value = actionWidget?.extra?.[actionWidget.value] ?? actionWidget.value;
          insertValue(value);
        });
      }
    };
  }
});
