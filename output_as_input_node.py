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
    """Load an image from ComfyUI's output directory as a workflow input."""

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
    RETURN_NAMES = ("image", "mask")
    FUNCTION = "load_image"
    CATEGORY = "image"
    # Retired 2026-11-23: loads in saved workflows, hidden from search; use the core node.
    DEPRECATED = True
    DESCRIPTION = (
        "Loads an image from the ComfyUI output folder so generated files can "
        "be reused as inputs. New workflows can use the native "
        "Load Image (from Outputs) node instead."
    )

    @classmethod
    def IS_CHANGED(cls, image):
        # Re-run only when the chosen file changes, not when other outputs appear.
        path = os.path.join(folder_paths.get_output_directory(), image)
        return os.path.getmtime(path) if os.path.isfile(path) else float("nan")

    def load_image(self, image):
        # ComfyUI rejects absolute paths; the annotation resolves inside output/.
        return LoadImage().load_image(f"{image} [output]")


NODE_CLASS_MAPPINGS = {
    "OutputAsInput": OutputAsInput
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "OutputAsInput": "Output as Input"
}
