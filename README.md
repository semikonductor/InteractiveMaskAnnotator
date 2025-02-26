# Polygon Mask Annotation Tool

![Python](https://img.shields.io/badge/python-3.8%2B-blue)![OpenCV](https://img.shields.io/badge/OpenCV-4.x-orange)

Interactive tool for creating precise polygon masks with real-time visualization.

[Chinese Document]: README_ZH.md

## Use Cases

|       Domain       |                    Description & Examples                    |
| :----------------: | :----------------------------------------------------------: |
|  Image Inpainting  | ✅ Precisely mark damaged areas 🖼️ Example: Old photo restoration |
|  Medical Imaging   | ⚕️ Annotate organ boundaries in CT scans 🩺 Example: Lung nodule annotation |
| Satellite Analysis | 🛰️ Extract building polygons 🌆 Example: Urban expansion studies |

## Features
- 🖱️ Left-click to add points | Right-click to undo
- 🔍 Adaptive window scaling with coordinate mapping
- 🎨 Generates 3-channel PNG masks
- 📏 Preserves original image dimensions
- 🔄 Real-time visual feedback

## Installation

```bash
pip install opencv-python numpy
```

## Usage

1. Place your image as `test.png` (or modify `img_path` in code)
2. Run:
```bash
python main.py
```
3. Annotate:
   - **Left-click**: Add vertex
   - **Right-click**: Remove last vertex
   - **S**: Save mask (auto-closed) and exit
   - **ESC**: Quit without saving

## Output Example
| Original Image     | Generated Mask      |
| ------------------ | ------------------- |
| ![Input](test.png) | ![Output](mask.png) |

## Technical Notes
- Coordinate system conversion between screen and original image
- Automatic window centering with black borders
- BGR color space standard for OpenCV compatibility
