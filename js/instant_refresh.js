import { app } from "../../../scripts/app.js";

app.registerExtension({
    name: "Comfy.AnimeCharacterSelectRefresh",
    async nodeCreated(node) {
        if (node.comfyClass === "CharacterPromptNode") {
            const widget = node.widgets?.find((w) => w.name === "character");
            if (widget) {
                const originalCallback = widget.callback;

                // Track a dedicated internal variable for just the portrait aspect ratio height
                node._previewImgHeight = 0;

                const updateNodePreview = function(characterName) {
                    if (!characterName) return;
                    
                    const img = new Image();
                    img.src = `/anime_character_select/get_thumb?character=${encodeURIComponent(characterName)}&t=${Date.now()}`;
                    
                    img.onload = function() {
                        node.imgs = [img];
                        
                        // Calculate precise responsive aspect ratio dimensions based on node width
                        const drawWidth = node.size[0] - 20; 
                        node._previewImgHeight = (img.height / img.width) * drawWidth;
                        
                        // Explicitly query the original clean core height of the text/dropdown layout
                        const nativeWidgetsHeight = originalComputeSize.apply(node);
                        
                        // Force a strict, non-accumulating size array calculation [width, height]
                        node.size = [node.size[0], nativeWidgetsHeight[1] + node._previewImgHeight + 15];
                        
                        node.setDirtyCanvas(true, true);
                    };
                };

                widget.callback = function (value) {
                    if (originalCallback) originalCallback.apply(this, arguments);
                    updateNodePreview(value);
                };

                // --- FIXED SIZING HOOK ---
                // We pull clean base dimensions every single time, stopping the infinite growth loop
                const originalComputeSize = node.computeSize;
                node.computeSize = function() {
                    const size = originalComputeSize.apply(this, arguments);
                    if (this._previewImgHeight > 0) {
                        // Simply append the unique portrait height to the baseline clean text layout
                        size[1] = size[1] + this._previewImgHeight + 15;
                    }
                    return size;
                };

                node.onDrawBackground = function(ctx) {
                    if (this.imgs && this.imgs.length > 0) {
                        const img = this.imgs[0];
                        if (img.width) {
                            // Find exactly where the text dropdown elements structurally terminate
                            const nativeWidgetsHeight = originalComputeSize.apply(this);
                            const yOffset = nativeWidgetsHeight[1] + 5; 
                            
                            const drawWidth = this.size[0] - 20; 
                            const drawHeight = (img.height / img.width) * drawWidth; 
                            const xOffset = 10; 
                            
                            // Stamp the character portrait precisely onto the canvas view
                            ctx.drawImage(img, xOffset, yOffset, drawWidth, drawHeight);
                        }
                    }
                };

                setTimeout(() => updateNodePreview(widget.value), 200);
            }
        }
    }
});