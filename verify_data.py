import os
import zipfile
import pandas as pd
from PIL import Image

zip_path = 'insat3d-infrared-raw-cyclone-images-20132021.zip'
extract_dir = './cyclone_dataset'

if os.path.exists(zip_path):
    print("Zip file found. Extracting...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
    print("Extraction complete.")
else:
    print("Error: Zip file not found. Download may have failed.")
    exit()

csv_files = [f for f in os.listdir(extract_dir) if f.endswith('.csv')]
if not csv_files:
    print("Error: No CSV label file found in the extracted folder.")
else:
    csv_path = os.path.join(extract_dir, csv_files[0])
    df = pd.read_csv(csv_path)
    print(f"\nCSV loaded successfully! Found {len(df)} labels.")
    print("Sample data mapping (Image Name -> Knots):")
    print(df.head())
 
try:
    first_image_name = df.iloc[0, 0] # Gets the 'img_name' from the first row
    
    image_found = False
    for root, dirs, files in os.walk(extract_dir):
        if first_image_name in files:
            img_path = os.path.join(root, first_image_name)
            img = Image.open(img_path)
            img.verify() # Checks for image file corruption
            print(f"\nImage verification passed! Successfully validated: {first_image_name}")
            print(f"Image Resolution: {img.size}, Mode: {img.mode}")
            image_found = True
            break
            
    if not image_found:
        print(f"\nWarning: Could not find the image '{first_image_name}' in the extracted folders.")
        
except Exception as e:
    print(f"\nError reading image or CSV: {e}")