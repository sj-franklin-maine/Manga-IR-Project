import manga109api
import pandas as pd
import os
from PIL import Image
from tqdm import tqdm  # Import tqdm

def get_all_images_and_annotations(manga109_root_dir, book):
    p = manga109api.Parser(root_dir=manga109_root_dir)
    annotations = p.get_annotation(book=book)
    
    image_data = []
    for page_index in range(len(annotations["page"])):
        img_path = p.img_path(book=book, index=page_index)
        # Only store frame annotations
        rois = annotations["page"][page_index].get("frame", [])
        for roi in rois:
            image_data.append({
                "image_path": img_path,
                "annotation": "frame",  # Set the annotation type to "frame"
                "roi": roi
            })
    
    return pd.DataFrame(image_data)

def crop_panel(img, roi):
    x0 = int(roi["@xmin"])
    y0 = int(roi["@ymin"])
    x1 = int(roi["@xmax"])
    y1 = int(roi["@ymax"])
    return img.crop((x0, y0, x1, y1))

manga109_root_dir = "Manga109_released_2023_12_07"
output_root_dir = "panels"  # Main output directory

# Create the output directory if it doesn't exist
os.makedirs(output_root_dir, exist_ok=True)

# Get the list of books from books.txt
with open(os.path.join(manga109_root_dir, "books.txt"), "r") as f:
    books = [line.strip() for line in f.readlines()]

for book in tqdm(books, desc="Processing Books"):
    # Create a subfolder for each book
    book_output_dir = os.path.join(output_root_dir, book)
    os.makedirs(book_output_dir, exist_ok=True)

    # Get all images and annotations for the current book
    df = get_all_images_and_annotations(manga109_root_dir, book)

    # Iterate through each entry and save panels with progress tracking
    for index, entry in df.iterrows():
        img_path = entry["image_path"]
        roi = entry["roi"]

        # Load the image
        img = Image.open(img_path)

        # Crop the specific panel
        cropped_panel = crop_panel(img, roi)

        # Create a filename for the cropped panel
        panel_filename = f"{book}_page_{index + 1}_annotation_{entry['annotation']}.png"
        panel_path = os.path.join(book_output_dir, panel_filename)

        # Save the cropped panel
        cropped_panel.save(panel_path)
