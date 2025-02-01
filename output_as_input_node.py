import os
import folder_paths
from nodes import LoadImage

class OutputAsInput:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.image_path = None

    @classmethod
    def INPUT_TYPES(cls):
        output_dir = folder_paths.get_output_directory()
        # Get list of images from output directory
        images = [f for f in os.listdir(output_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
        # Sort by modification time to get latest first
        images.sort(key=lambda x: os.path.getmtime(os.path.join(output_dir, x)), reverse=True)
        
        return {
            "required": {
                "image": (sorted(images), {"default": images[0] if images else None}),
            },
        }

    RETURN_TYPES = ("IMAGE", "MASK")
    FUNCTION = "load_image"
    CATEGORY = "image"

    def load_image(self, image):
        image_path = os.path.join(self.output_dir, image)
        img = LoadImage()
        return img.load_image(image_path)

# Node registration
NODE_CLASS_MAPPINGS = {
    "OutputAsInput": OutputAsInput
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "OutputAsInput": "Output As Input 🔄"
}
