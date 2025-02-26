"""
Interactive Mask Annotation 

Usage:
1. Image Display:
- Images are auto-scaled to fit window while maintaining aspect ratio
- Black borders added when window aspect ratio doesn't match image

2. Controls:
- Left Click: Add polygon vertex at cursor position
- Right Click: Remove last added vertex
- Press 'S': Save current polygon as 3-channel mask (mask.png)
- Press ESC: Exit program

3. Workflow:
a) Left-click to place vertices around target area
b) Connect back to first vertex visually (auto-connection not implemented)
c) Press 'S' to save mask when satisfied with polygon
d) Press ESC to exit

Note:
- Coordinates are automatically converted between display and original image spaces
- Valid clicks must be within the scaled image area (black borders ignored)
- Minimum 3 vertices required for mask generation
- Saved mask uses white (255,255,255) for selected area, black (0,0,0) background

Requirements:
- OpenCV 3.x+
- NumPy
"""
import cv2
import numpy as np

# Global variables
points = []         # Stores polygon vertex coordinates (original image coordinate system)
img_orig = None     # Original image
h_orig, w_orig = 0, 0  # Dimensions of the original image
scale = 1.0         # Current zoom scale
x_offset, y_offset = 0, 0  # Image offset in the window

def draw_points():
    global scale, x_offset, y_offset
    
    # Create a copy of the image for drawing
    img_draw = img_orig.copy()
    
    # Draw all points and connections
    for i, (x, y) in enumerate(points):
        cv2.circle(img_draw, (x, y), 5, (0, 0, 255), -1)
        cv2.putText(img_draw, str(i+1), (x+5, y), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    if len(points) > 1:
        for i in range(len(points)-1):
            cv2.line(img_draw, points[i], points[i+1], (0, 255, 0), 2)
    
    # Get current window dimensions
    win_rect = cv2.getWindowImageRect("Image")
    win_w = max(win_rect[2], 100)  # Minimum width constraint
    win_h = max(win_rect[3], 100)  # Minimum height constraint
    
    # Calculate scaled dimensions maintaining aspect ratio
    scale = min(win_w / w_orig, win_h / h_orig)
    scaled_w = int(w_orig * scale)
    scaled_h = int(h_orig * scale)
    
    # Resize the image
    img_scaled = cv2.resize(img_draw, (scaled_w, scaled_h), 
                           interpolation=cv2.INTER_AREA)
    
    # Calculate centering offsets
    x_offset = (win_w - scaled_w) // 2
    y_offset = (win_h - scaled_h) // 2
    
    # Create display image with black borders
    img_display = np.zeros((win_h, win_w, 3), dtype=np.uint8)
    img_display[y_offset:y_offset+scaled_h, x_offset:x_offset+scaled_w] = img_scaled
    
    cv2.imshow("Image", img_display)

def mouse_callback(event, x, y, flags, param):
    # Convert coordinates to original image coordinate system
    x_img = int((x - x_offset) / scale)
    y_img = int((y - y_offset) / scale)
    
    # Coordinate validity check
    if not (0 <= x_img < w_orig and 0 <= y_img < h_orig):
        return
    
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x_img, y_img))
        draw_points()
    elif event == cv2.EVENT_RBUTTONDOWN:
        if points:
            points.pop()
            draw_points()

def create_mask():
    global h_orig, w_orig
    if len(points) < 3:
        print("At least 3 points required to create a polygon")
        return
    
    # Create three-channel mask (height, width, 3 channels)
    mask = np.zeros((h_orig, w_orig, 3), dtype=np.uint8)
    
    # Convert point coordinates to numpy array format
    pts = np.array([points], dtype=np.int32)
    
    # Fill the polygon (using BGR three-channel white)
    cv2.fillPoly(mask, pts, color=(255, 255, 255))
    
    # Debug information
    print("Number of channels in generated mask:", mask.shape[2])  # Should output 3
    
    # Force save as three-channel PNG
    cv2.imwrite("mask.png", mask)
    print("Three-channel mask saved")

if __name__ == "__main__":
    # Read image
    img_path = "test.png"
    img_orig = cv2.imread(img_path)
    if img_orig is None:
        print("Failed to read image, please check path")
        exit()
    
    h_orig, w_orig = img_orig.shape[:2]
    
    # Create window
    cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
    cv2.setMouseCallback("Image", mouse_callback)
    
    # Initial window size (scaled to 60% of screen size)
    screen_scale = 0.6
    screen_w = int(w_orig * screen_scale)
    screen_h = int(h_orig * screen_scale)
    cv2.resizeWindow("Image", screen_w, screen_h)
    
    draw_points()
    
    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            create_mask()
            break
        elif key == 27:
            break
    
    cv2.destroyAllWindows()