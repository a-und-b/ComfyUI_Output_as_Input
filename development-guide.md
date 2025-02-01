# ComfyUI Custom Node Development Guide

## Table of Contents
1. [Setup & Prerequisites](#setup--prerequisites)
2. [Project Structure](#project-structure)
3. [Node Development](#node-development)
4. [Testing & Debugging](#testing--debugging)
5. [Publishing & Distribution](#publishing--distribution)
6. [Best Practices](#best-practices)
7. [Node Registry Integration](#node-registry-integration)

## Setup & Prerequisites

### Required Tools
- Python 3.10+
- Git
- ComfyUI installed locally
- Basic understanding of Python and Node.js

### Development Environment Setup
```bash
# Clone ComfyUI if you haven't already
git clone https://github.com/comfyanonymous/ComfyUI
cd ComfyUI

# Create custom_nodes directory if it doesn't exist
mkdir -p custom_nodes
cd custom_nodes

# Create your node project
mkdir my-custom-nodes
cd my-custom-nodes
```

## Project Structure

Standard directory structure for a ComfyUI custom node project:

```
my-custom-nodes/
├── __init__.py           # Main entry point
├── nodes/                # Node implementations
│   ├── __init__.py
│   ├── node1.py
│   └── node2.py
├── js/                   # Frontend components
│   └── extensions.js     # UI customizations
├── requirements.txt      # Python dependencies
└── README.md            # Documentation
```

## Node Development

### Basic Node Structure

```python
# nodes/example_node.py

class ExampleNode:
    """
    Node documentation goes here.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input1": ("STRING", {"default": "default value"}),
                "input2": ("INT", {"default": 0, "min": 0, "max": 100}),
            },
            "optional": {
                "optional_input": ("FLOAT", {"default": 1.0}),
            }
        }
    
    RETURN_TYPES = ("STRING", "INT")
    RETURN_NAMES = ("output1", "output2")
    FUNCTION = "process"
    CATEGORY = "examples"

    def process(self, input1, input2, optional_input=1.0):
        # Process inputs and return outputs
        return (f"Processed {input1}", input2 + 1)

# Node registration
NODE_CLASS_MAPPINGS = {
    "ExampleNode": ExampleNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ExampleNode": "Example Node"
}
```

### Common Input Types
- `STRING`: Text input
- `INT`: Integer number
- `FLOAT`: Decimal number
- `BOOLEAN`: True/False toggle
- `IMAGE`: Image data
- `LATENT`: Latent space representation
- `MODEL`: ML model
- `CONDITIONING`: Prompt conditioning
- `COMBO`: Dropdown selection

### Custom Widget Implementation
```python
class CustomWidget:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "custom_input": (
                    "CUSTOM", {
                        "widget": {
                            "type": "custom_widget",
                            "options": {"param1": "value1"}
                        }
                    }
                ),
            }
        }
```

## Testing & Debugging

### Local Testing
1. Place your node project in ComfyUI's custom_nodes directory
2. Restart ComfyUI to load new nodes
3. Check the console for loading errors
4. Test node in the UI workflow

### Debug Logging
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class DebugNode:
    def process(self, *args, **kwargs):
        logger.debug(f"Processing with args: {args}, kwargs: {kwargs}")
        # Process logic here
```

## Publishing & Distribution

### Package Preparation
1. Create comprehensive README.md
2. Document dependencies in requirements.txt
3. Add installation instructions
4. Include example workflows
5. Add screenshots/demonstrations

### Distribution Methods
1. GitHub Repository
   - Clear documentation
   - Release tags
   - License specification

2. ComfyUI Manager Integration
   - Add to custom-node-list.json
   - Follow naming conventions
   - Include preview images

3. Node Registry (New Standard)
   - Register with comfy.org registry
   - Implement standardized metadata
   - Follow versioning guidelines

## Best Practices

### Code Quality
- Use type hints
- Document functions and classes
- Follow PEP 8 style guide
- Handle errors gracefully
- Cache expensive operations

### Performance
```python
class OptimizedNode:
    def __init__(self):
        self.cache = {}
    
    def process(self, input_data):
        cache_key = hash(input_data)
        if cache_key in self.cache:
            return self.cache[cache_key]
            
        result = self.expensive_operation(input_data)
        self.cache[cache_key] = result
        return result
```

### UI/UX
- Clear node names and categories
- Informative tooltips
- Sensible default values
- Proper error messages
- Responsive UI updates

## Node Registry Integration

### Registry Standards
The official ComfyUI Node Registry (comfy.org) defines standards for node quality and distribution:

1. Metadata Requirements
```json
{
    "name": "my-custom-nodes",
    "version": "1.0.0",
    "author": "Your Name",
    "description": "Brief description",
    "repository": "https://github.com/username/my-custom-nodes",
    "license": "MIT",
    "tags": ["category1", "category2"],
    "min_comfy_version": "1.0.0",
    "max_comfy_version": "2.0.0",
    "dependencies": {
        "python": ["numpy>=1.20.0"],
        "comfy_nodes": ["another-custom-node>=1.0.0"]
    }
}
```

2. Quality Guidelines
- Comprehensive documentation
- Working example workflows
- Test coverage
- Performance benchmarks
- Security considerations

3. Publishing Process
```bash
# Install registry CLI tool
pip install comfy-registry-cli

# Initialize registry config
comfy-registry init

# Validate package
comfy-registry validate

# Publish to registry
comfy-registry publish
```

### Best Practices for Registry Integration
1. Version Management
   - Semantic versioning
   - Changelog maintenance
   - Dependency specifications

2. Documentation
   - API documentation
   - Usage examples
   - Installation guide
   - Troubleshooting section

3. Testing
   - Unit tests
   - Integration tests
   - Example workflows
   - Performance benchmarks

4. Maintenance
   - Issue tracking
   - Regular updates
   - Security patches
   - Compatibility checks