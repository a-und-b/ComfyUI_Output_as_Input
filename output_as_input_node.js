import { app } from "/scripts/app.js";

app.registerExtension({
    name: "Comfy.OutputAsInput.Preview.v2", // Incremented version for clarity
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "OutputAsInput") {
            console.log("[OutputAsInput Preview] Registering preview for node:", nodeData.name);

            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function () {
                onNodeCreated?.apply(this, arguments);
                console.log("[OutputAsInput Preview] Node created:", this.id, this.title);

                const imageWidget = this.widgets.find(w => w.name === "image");
                console.log("[OutputAsInput Preview] Found image widget:", imageWidget);

                if (imageWidget) {
                    this.previewImageElement = document.createElement("img");
                    this.previewImageElement.style.maxWidth = "100%";
                    this.previewImageElement.style.maxHeight = "200px";
                    this.previewImageElement.style.objectFit = "contain";
                    this.previewImageElement.style.display = "none";
                    this.previewImageElement.style.marginTop = "10px"; // Added a bit more margin
                    this.previewImageElement.setAttribute("aria-hidden", "true");
                    console.log("[OutputAsInput Preview] Preview img element created:", this.previewImageElement);

                    // Append to node's content area (more robust)
                    // The widget itself doesn't have a standard container, so we add to the node body
                    // We will try to add it to a common place where widgets reside.
                    // this.tbody is where LiteGraph typically adds widget rows for property display.
                    // If not available, fallback to this.content or this.root.
                    let parentElement = this.tbody || this.content || this.root;
                    if (parentElement) {
                        parentElement.appendChild(this.previewImageElement);
                        console.log("[OutputAsInput Preview] Appended preview to parent:", parentElement);
                    } else {
                        console.error("[OutputAsInput Preview] Could not find suitable parent (tbody, content, or root) to append preview image.");
                        return; // Stop if we can't append
                    }
                    
                    const originalOnRemoved = this.onRemoved;
                    this.onRemoved = () => {
                        if (this.previewImageElement) {
                            this.previewImageElement.remove();
                            this.previewImageElement = null;
                            console.log("[OutputAsInput Preview] Preview element removed.");
                        }
                        originalOnRemoved?.apply(this, arguments);
                    };

                    const updatePreview = (fileName) => {
                        console.log("[OutputAsInput Preview] updatePreview called with fileName:", fileName);
                        if (!this.previewImageElement) {
                            console.warn("[OutputAsInput Preview] Preview element not found in updatePreview.");
                            return;
                        }

                        if (!fileName || typeof fileName !== 'string' || fileName === "None") {
                            this.previewImageElement.style.display = 'none';
                            console.log("[OutputAsInput Preview] Hiding preview (no filename or 'None').");
                        } else {
                            const src = `/view?filename=${encodeURIComponent(fileName)}&type=output&subfolder=&rand=${Date.now()}`;
                            console.log("[OutputAsInput Preview] Setting preview src:", src);
                            this.previewImageElement.src = src;
                            this.previewImageElement.style.display = 'block';
                            
                            this.previewImageElement.onload = () => {
                                console.log("[OutputAsInput Preview] Image loaded successfully:", fileName);
                                this.setDirtyCanvas(true, true);
                            };
                            this.previewImageElement.onerror = () => {
                                console.error("[OutputAsInput Preview] Error loading image:", fileName, "at URL:", this.previewImageElement.src);
                                if (this.previewImageElement) {
                                   this.previewImageElement.style.display = 'none';
                                }
                                this.setDirtyCanvas(true, true);
                            };
                        }
                        this.setDirtyCanvas(true, true); // Redraw for visibility changes
                    };

                    const originalWidgetCallback = imageWidget.callback;
                    imageWidget.callback = (value, ...args) => {
                        console.log("[OutputAsInput Preview] Widget callback triggered. Value:", value);
                        let callback_result;
                        if (originalWidgetCallback) {
                            callback_result = originalWidgetCallback.apply(imageWidget, [value, ...args]);
                        }
                        updatePreview(value);
                        return callback_result;
                    };
                    
                    if (imageWidget.value) {
                        console.log("[OutputAsInput Preview] Initializing preview with widget value:", imageWidget.value);
                        updatePreview(imageWidget.value);
                    } else {
                        console.log("[OutputAsInput Preview] No initial widget value to preview.");
                    }
                } else {
                    console.warn("[OutputAsInput Preview] Image widget not found on node creation.");
                }
            };
        } else {
            // Optional: Log if the extension sees other node types (for debugging the registration itself)
            // console.log("[OutputAsInput Preview] Skipping node (not OutputAsInput):", nodeData.name);
        }
    }
}); 