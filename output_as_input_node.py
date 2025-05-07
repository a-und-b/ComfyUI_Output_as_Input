import os
import folder_paths
# from nodes import LoadImage # We will load images manually for more control

# Import necessary libraries for manual image loading
from PIL import Image
import numpy as np
import torch

class OutputAsInput:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()

    @classmethod
    def INPUT_TYPES(cls):
        output_dir = folder_paths.get_output_directory()
        images = []
        # Ensure output directory exists before trying to list its contents
        if os.path.exists(output_dir) and os.path.isdir(output_dir):
            images = [f for f in os.listdir(output_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif'))]
            if images:
                # Sort by modification time to get latest first
                images.sort(key=lambda x: os.path.getmtime(os.path.join(output_dir, x)), reverse=True)
        
        # Provide a "None" option if no images are found, or as a general choice
        image_options = images if images else ["None"]
        default_image = images[0] if images else "None"
        
        return {
            "required": {
                "image": (image_options, {"default": default_image}),
            },
        }

    RETURN_TYPES = ("IMAGE", "MASK")
    RETURN_NAMES = ("image_out", "mask_out") # Optional, but good practice
    FUNCTION = "load_image_and_mask"
    CATEGORY = "image"

    def load_image_and_mask(self, image):
        if image == "None" or not image:
            # Return dummy/empty tensors if "None" is selected or image name is invalid
            # Shape: (batch_size, height, width, channels) for image
            # Shape: (batch_size, height, width) for mask
            dummy_image = torch.zeros((1, 1, 1, 3), dtype=torch.float32) # 1x1 black pixel
            dummy_mask = torch.ones((1, 1, 1), dtype=torch.float32)   # 1x1 full mask
            return (dummy_image, dummy_mask)

        image_path = os.path.join(self.output_dir, image)

        if not os.path.exists(image_path):
            print(f"[OutputAsInput] Error: Image file not found at {image_path}")
            dummy_image = torch.zeros((1, 1, 1, 3), dtype=torch.float32)
            dummy_mask = torch.ones((1, 1, 1), dtype=torch.float32)
            return (dummy_image, dummy_mask)

        try:
            pil_image = Image.open(image_path)
            
            # Convert to numpy array and then to tensor
            img_rgb = pil_image.convert("RGB")
            img_array = np.array(img_rgb).astype(np.float32) / 255.0
            img_tensor = torch.from_numpy(img_array).unsqueeze(0) # Add batch dimension (B, H, W, C)

            # Handle mask (alpha channel or create a full mask)
            if 'A' in pil_image.getbands():
                mask_array = np.array(pil_image.split()[-1]).astype(np.float32) / 255.0
                # Mask should be (B, H, W)
                mask_tensor = torch.from_numpy(mask_array).unsqueeze(0) 
            else:
                mask_tensor = torch.ones((img_tensor.shape[1], img_tensor.shape[2]), dtype=torch.float32).unsqueeze(0) # (B, H, W)
            
            return (img_tensor, mask_tensor)

        except Exception as e:
            print(f"[OutputAsInput] Error loading image {image_path}: {e}")
            dummy_image = torch.zeros((1, 1, 1, 3), dtype=torch.float32)
            dummy_mask = torch.ones((1, 1, 1), dtype=torch.float32)
            return (dummy_image, dummy_mask)

# Node registration
NODE_CLASS_MAPPINGS = {
    "OutputAsInput": OutputAsInput
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "OutputAsInput": "Output As Input 🔄 (Preview)"
}
