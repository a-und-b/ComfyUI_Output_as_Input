import os
import folder_paths
from nodes import LoadImage


def _list_output_images(output_dir):
    images = [
        f
        for f in os.listdir(output_dir)
        if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))
    ]
    images.sort(
        key=lambda x: os.path.getmtime(os.path.join(output_dir, x)),
        reverse=True,
    )
    return images


class OutputAsInput:
    @classmethod
    def INPUT_TYPES(cls):
        output_dir = folder_paths.get_output_directory()
        images = _list_output_images(output_dir) if os.path.isdir(output_dir) else []
        return {
            "required": {
                "image": (sorted(images), {"default": images[0] if images else None}),
            },
        }

    RETURN_TYPES = ("IMAGE", "MASK")
    FUNCTION = "load_image"
    CATEGORY = "image"

    @classmethod
    def IS_CHANGED(cls, image):
        # Re-run only when the chosen file changes, not when other outputs appear.
        path = os.path.join(folder_paths.get_output_directory(), image)
        return os.path.getmtime(path) if os.path.isfile(path) else float("nan")

    def load_image(self, image):
        # ComfyUI rejects absolute paths; the annotation resolves inside output/.
        return LoadImage().load_image(f"{image} [output]")

# Node registration
NODE_CLASS_MAPPINGS = {
    "OutputAsInput": OutputAsInput
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "OutputAsInput": "Output As Input 🔄"
}
