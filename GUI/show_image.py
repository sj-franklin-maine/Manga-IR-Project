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

    books.remove('Arisa')
    books.remove('Count3DeKimeteAgeru')
    

    return random_book

# Pass book and gather all annotations 
def get_all_images_and_annotations(manga109_root_dir, book):
    page_num = 22

    p = manga109api.Parser(root_dir=manga109_root_dir)
    annotations = p.get_annotation(book=book)

    curr_page = annotations['page'][page_num]

    
    image_data = []

    # Get the image path and annotations for each page
    img_path = p.img_path(book=book, index=page_num)
    for annotation_type in ["body", "face", "frame", "text","character"]:
        rois = annotations["page"][page_num].get(annotation_type, [])
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

    entry = df.iloc[0]
    img_path = entry["image_path"]

    characters = []

    for index, entry in df.iterrows():
        if entry["annotation"] == "character":
            characters.append(entry["roi"])

            

    # Get File Path
    filename = os.path.basename(img_path)
    page_number, _ = os.path.splitext(filename)


    # Get Characters
    #characters = get_characters(book, page_number)

    return img_path, page_number, book

# Testing
get_random_entry()
