import manga109api
import pandas as pd
import os
from PIL import Image
from tqdm import tqdm

manga109_root_dir = "Manga109_released_2023_12_07"
output_root_dir = "panels"

os.makedirs(output_root_dir, exist_ok=True)

with open(os.path.join(manga109_root_dir, "books.txt"), "r") as f:
    books = [line.strip() for line in f.readlines()]

keep_books = ['ARMS']
books = [book for book in books if book in keep_books]

# Specify the number of pages you want to process
max_pages = 10  # Change this number as needed

def get_all_images_and_annotations(manga109_root_dir, book, max_pages=None):
    p = manga109api.Parser(root_dir=manga109_root_dir)
    annotations = p.get_annotation(book=book)
    
    image_data = []
    total_pages = len(annotations["page"])
    
    # Limit the pages processed to max_pages if provided
    num_pages_to_process = min(total_pages, max_pages) if max_pages is not None else total_pages

    for page_index in range(num_pages_to_process):
        img_path = p.img_path(book=book, index=page_index)
        # Only store frame annotations
        rois = annotations["page"][page_index].get("frame", [])
        for roi in rois:
            image_data.append({
                "image_path": img_path,
                "annotation": "frame",
                "roi": roi
            })
    
    return pd.DataFrame(image_data)

def crop_panel(img, roi):
    x0 = int(roi["@xmin"])
    y0 = int(roi["@ymin"])
    x1 = int(roi["@xmax"])
    y1 = int(roi["@ymax"])
    return img.crop((x0, y0, x1, y1))

for book in tqdm(books, desc="Processing Books"):
    book_output_dir = os.path.join(output_root_dir, book)
    os.makedirs(book_output_dir, exist_ok=True)

    df = get_all_images_and_annotations(manga109_root_dir, book, max_pages)

    for index, entry in df.iterrows():
        img_path = entry["image_path"]
        roi = entry["roi"]

        img = Image.open(img_path)
        cropped_panel = crop_panel(img, roi)

        panel_filename = f"{book}_page_{index + 1}_annotation_{entry['annotation']}.png"
        panel_path = os.path.join(book_output_dir, panel_filename)

        cropped_panel.save(panel_path)
