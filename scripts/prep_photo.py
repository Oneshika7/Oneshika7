import sys
import os
import cv2
import numpy as np
from PIL import Image
from rembg import remove

def prep_photo(input_path, output_path="data/source-prepped.png"):
    print(f"Processing {input_path}...")
    # 1. Remove background
    with open(input_path, 'rb') as i:
        input_data = i.read()
    subject_data = remove(input_data)
    
    temp_path = "data/temp_no_bg.png"
    with open(temp_path, "wb") as o:
        o.write(subject_data)
        
    # 2. Boost local contrast with CLAHE
    img = cv2.imread(temp_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        print("Error: Could not read image after background removal.")
        return
        
    if len(img.shape) == 3 and img.shape[2] == 4:
        alpha = img[:, :, 3]
        bgr = img[:, :, :3]
        gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    elif len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        alpha = np.ones_like(gray) * 255
    else:
        gray = img
        alpha = np.ones_like(gray) * 255
        
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    cl1 = clahe.apply(gray)
    
    # 3. Composite onto pure white
    white_bg = np.ones_like(cl1) * 255
    alpha_norm = alpha / 255.0
    final = (cl1 * alpha_norm + white_bg * (1 - alpha_norm)).astype(np.uint8)
    
    cv2.imwrite(output_path, final)
    print(f"Prepped photo saved to {output_path}")
    
    if os.path.exists(temp_path):
        os.remove(temp_path)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python prep_photo.py <input_image>")
        sys.exit(1)
    
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    prep_photo(sys.argv[1])
