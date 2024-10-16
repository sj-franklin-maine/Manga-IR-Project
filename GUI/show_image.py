import manga109api
import pandas as pd
import random
from PIL import Image, ImageDraw
import os

manga109_root_dir = os.path.join(os.path.dirname(__file__), 'manga109', 'Manga109_released_2023_12_07')

# Choose a random book from the database using Manga109
def get_random_book(manga109_root_dir):
    p = manga109api.Parser(manga109_root_dir)
    books = p.books
    random_book = random.choice(books)

    return random_book

# Pass book and gather all annotations 
def get_all_images_and_annotations(manga109_root_dir, book):
    p = manga109api.Parser(root_dir=manga109_root_dir)
    annotations = p.get_annotation(book=book)
    
    image_data = []

    # Get the image path and annotations for each page
    for page_index in range(len(annotations["page"])):
        img_path = p.img_path(book=book, index=page_index)
        for annotation_type in ["body", "face", "frame", "text"]:
            rois = annotations["page"][page_index].get(annotation_type, [])
            for roi in rois:
                image_data.append({
                    "image_path": img_path,
                    "annotation": annotation_type,
                    "roi": roi,
                })
    
    return pd.DataFrame(image_data)

# Get the characters in the image
def get_characters(book, page_number):
    p = manga109api.Parser(manga109_root_dir)
    annotation = p.get_annotation(book=book)
    
    
# Get a random entry from the annotations df
def get_random_entry():
    book = get_random_book(manga109_root_dir)
    df = get_all_images_and_annotations(manga109_root_dir, book)
    
    # Get a random entry from the dataframe
    random_entry = df.sample(n=1).iloc[0]

    # Get File Path
    img_path = random_entry["image_path"]
    filename = os.path.basename(img_path)

    # Get Page Number
    page_number, _ = os.path.splitext(filename)
    annotation_type = random_entry["annotation"]

    # Get Characters
    characters = get_characters(book, page_number)


    return img_path, page_number, annotation_type, book

# Testing
# get_random_entry()
