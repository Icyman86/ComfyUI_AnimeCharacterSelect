import { app } from "../../../scripts/app.js";

app.registerExtension({
    name: "Comfy.AnimeCharacterSelectRefresh",
    async nodeCreated(node) {
        if (node.comfyClass === "CharacterPromptNode") {
            const filterWidget = node.widgets?.find((w) => w.name === "category_filter");
            const characterWidget = node.widgets?.find((w) => w.name === "character");
            
            if (characterWidget && filterWidget) {
                const originalCharCallback = characterWidget.callback;

                // 1. CAPTURE THE TRUE MASTER LIST AT INITIALIZATION TIME
                const masterList = [...characterWidget.options.values];
                node._previewImgHeight = 0;

                const updateNodePreview = function(characterName) {
                    try {
                        let cleanName = characterName;
                        if (Array.isArray(cleanName)) {
                            cleanName = cleanName[0] || "";
                        }
                        if (typeof cleanName !== "string") {
                            cleanName = String(cleanName);
                        }

                        if (!cleanName || cleanName.trim() === "" || cleanName.startsWith("--") || cleanName === "undefined") {
                            console.log("[DEBUG] Preview skip due to invalid character name:", cleanName);
                            return;
                        }
                        
                        const img = new Image();
                        img.src = `/anime_character_select/get_thumb?character=${encodeURIComponent(cleanName)}&t=${Date.now()}`;
                        
                        img.onload = function() {
                            try {
                                // Assign the downloaded texture safely to the node model
                                node.imgs = [img];
                                
                                if (!node.size || !Array.isArray(node.size)) {
                                    node.size = [300, 150]; 
                                }

                                const drawWidth = node.size[0] - 20; 
                                node._previewImgHeight = (img.height / img.width) * drawWidth;
                                
                                const nativeWidgetsHeight = originalComputeSize.apply(node);
                                const coreLayoutHeight = Array.isArray(nativeWidgetsHeight) ? nativeWidgetsHeight[1] : 100;
                                
                                // Expand the node container bounds dynamically
                                node.size = [node.size[0], coreLayoutHeight + node._previewImgHeight + 15];
                                node.setDirtyCanvas(true, true);
                            } catch (innerImgError) {
                                console.error("IMAGE ONLOAD ERROR:", innerImgError);
                            }
                        };

                        img.onerror = function() {
                            console.error(`IMAGE FETCH REJECTED BY SERVER FOR: "${cleanName}"`);
                        };

                    } catch (imgSetupError) {
                        console.error("PREVIEW GENERATOR FAILURE:", imgSetupError);
                    }
                };

                // 2. THE CASCADING FILTER LOGIC
                filterWidget.callback = function(value) {
                    try {
                        let filteredSubset = [];
                        const targetCategory = value.toLowerCase();

                        if (targetCategory === "all") {
                            filteredSubset = [...masterList];
                        } else {
                            filteredSubset = masterList.filter(item => 
                                String(item).toLowerCase().includes(targetCategory)
                            );
                        }

                        if (filteredSubset.length === 0) {
                            filteredSubset = ["-- No Matches --"];
                        }

                        // Rebind dropdown choices array
                        characterWidget.options.values = filteredSubset;
                        
                        // FIX: Secure the first text item primitive string directly from our verified array
                        const targetSelection = filteredSubset[0] || "";
                        characterWidget.value = targetSelection;

                        // FIX: Pass our pristine, verified selection string directly into the thumbnail engine
                        updateNodePreview(targetSelection);
                        node.setDirtyCanvas(true, true);
                    } catch (filterError) {
                        console.error("FILTER PROCESSING FAILURE:", filterError);
                    }
                };

                characterWidget.callback = function (value) {
                    try {
                        if (originalCharCallback) originalCharCallback.apply(this, arguments);
                        updateNodePreview(value);
                    } catch (charWidgetError) {
                        console.error("WIDGET INTERACTION FAILURE:", charWidgetError);
                    }
                };

                // --- STRUCTURAL CANVAS DIMENSION SIZING HOOKS ---
                const originalComputeSize = node.computeSize;
                node.computeSize = function() {
                    try {
                        const size = originalComputeSize.apply(this, arguments);
                        if (this._previewImgHeight > 0 && Array.isArray(size)) {
                            size[1] = size[1] + this._previewImgHeight + 15;
                        }
                        return size;
                    } catch (sizeHookError) {
                        console.error("COMPUTE SIZE CRASH:", sizeHookError);
                        return;
                    }
                };

                node.onDrawBackground = function(ctx) {
                    try {
                        if (node.imgs && Array.isArray(node.imgs) && node.imgs.length > 0) {
                            const img = node.imgs[0];
                            
                            if (img){
                              console.error("img test passed")
                            }
                            if (img.width){
                                console.error("img.width test passed")
                            }
                            if (node.size){
                                console.error("node.size test passed")
                            }
                            if (node.size.length > 1){
                                console.error("Array.isArray test passed")
                            }
                            if (img && img.width && node.size && node.size.length > 1){
                                const nativeWidgetsHeight = originalComputeSize.apply(this);
                                const coreHeight = Array.isArray(nativeWidgetsHeight) ? nativeWidgetsHeight[1] : 100;
                                const yOffset = coreHeight + 5; 
                                
                                const drawWidth = node.size[0] - 20; 
                                const drawHeight = (img.height / img.width) * drawWidth; 
                                const xOffset = 10; 
                                
                                ctx.drawImage(img, xOffset, yOffset, drawWidth, drawHeight);
                            }
                        }
                    } catch (drawBackgroundError) {
                        console.error("BACKGROUND DRAW MATRIX ENGINE FAILURE:", drawBackgroundError);
                    }
                };

                setTimeout(() => {
                    try {
                        const startupValue = Array.isArray(characterWidget.value) ? characterWidget.value[0] : characterWidget.value;
                        updateNodePreview(startupValue);
                    } catch (bootError) {
                        console.error("INITIALIZATION RUNTIME ERROR:", bootError);
                    }
                }, 200);
            }
        }
    }
});