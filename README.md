> [!NOTE]
> There is now a native ComfyUI node called **"Load Image (from Outputs)"** available.  
> I recommend using it instead. As a result, this repository is no longer under development.

---

# ComfyUI_Output_as_Input

This is a simple custom ComfyUI node that allows you to easily use recent output images as input in your workflows. It does not allow image uploads on purpose and does not require any additional dependencies.

## Manual Installation

1. Download the `output_as_input_node.py` file.
2. Move the file to the `custom_nodes` folder in your ComfyUI directory.
3. Restart ComfyUI.

As soon as this node is published in the official ComfyUI registry, it will be available for installation via the ComfyUI extension manager.

## Usage

1. Add the **Output as Input** node (category: `image`).
2. Pick an image from the ComfyUI `output/` folder in the dropdown.
3. Connect the `IMAGE` / `MASK` outputs into the rest of your graph.

Prefer the native **Load Image (from Outputs)** node for new workflows.
