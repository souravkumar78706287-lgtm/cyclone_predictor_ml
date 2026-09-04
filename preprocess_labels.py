import os
import pandas as pd
import numpy as np

csv_path = './cyclone_dataset/insat_3d_ds - Sheet.csv'
df = pd.read_csv(csv_path)
print("Original dataset shape:", df.shape)
print("Columns found:", df.columns.tolist())
df.columns = df.columns.str.strip()
def assign_imd_class(knots):
    if knots < 28:
        return 0  
    elif 28 <= knots <= 33:
        return 1  
    elif 34 <= knots <= 47:
        return 2  
    elif 48 <= knots <= 63:
        return 3 
    else:
        return 4  

intensity_col = [col for col in df.columns if 'knot' in col.lower() or 'int' in col.lower() or 'speed' in col.lower()]

if intensity_col:
    target_col = intensity_col[0]
    df['imd_class'] = df[target_col].apply(assign_imd_class)
    
   
    class_names = {
        0: 'Depression',
        1: 'Deep Depression',
        2: 'Cyclonic Storm',
        3: 'Severe Cyclonic Storm',
        4: 'Very Severe/Super Cyclonic Storm'
    }
    df['class_name'] = df['imd_class'].map(class_names)
    
    print("\nClass Distribution:")
    print(df['class_name'].value_counts())
else:
    print("Warning: Could not automatically detect intensity column. Using first numerical column after image name.")
    target_col = df.columns[1]
    df['imd_class'] = df[target_col].apply(assign_imd_class)


def find_image_path(img_name):
    ir_folder = './cyclone_dataset/insat3d_ir_cyclone_ds'
    raw_folder = './cyclone_dataset/insat3d_raw_cyclone_ds'
    
    full_path_ir = os.path.join(ir_folder, str(img_name))
    if os.path.exists(full_path_ir):
        return full_path_ir
        
    
    full_path_raw = os.path.join(raw_folder, str(img_name))
    if os.path.exists(full_path_raw):
        return full_path_raw
        
    for root, _, files in os.walk('./cyclone_dataset'):
        if str(img_name) in files:
            return os.path.join(root, str(img_name))
            
    return None

img_col = df.columns[0]
print("\nMapping full image file paths...")
df['file_path'] = df[img_col].apply(find_image_path)

missing_count = df['file_path'].isnull().sum()
if missing_count > 0:
    print(f"Removing {missing_count} rows where image files were not found.")
    df = df.dropna(subset=['file_path'])

output_csv = './cyclone_dataset/processed_cyclone_metadata.csv'
df.to_csv(output_csv, index=False)
print(f"\nProcessing complete! Cleaned dataset saved to: {output_csv}")