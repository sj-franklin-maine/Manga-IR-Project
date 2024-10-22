import manga109api
import pandas as pd
import random
from PIL import Image, ImageDraw
import os
import get_page


manga109_root_dir = os.path.join(os.path.dirname(__file__), 'manga109', 'Manga109_released_2023_12_07')


# Pass book and gather all annotations 
def get_all_images_and_annotations(manga109_root_dir, book, bool_next):

    page_num = get_page.get_new_page()


    p = manga109api.Parser(root_dir=manga109_root_dir)
    annotations = p.get_annotation(book=book)

    #curr_page = annotations["page"][page_num].get(annotation_type, [])

    
    image_data = []

    # Get the image path and annotations for each page
    img_path = p.img_path(book=book, index=page_num)
    for annotation_type in ["body", "face", "frame", "text"]:
        rois = annotations["page"][page_num].get(annotation_type, [])
        for roi in rois:
            image_data.append({
                "annotation": annotation_type,
                "roi": roi,
            })
    
    return pd.DataFrame(image_data), img_path

# Get the characters in the image
def get_characters(df):
    characters = []
    for index, entry in df.iterrows():
        if entry["annotation"] == "body" or entry["annotation"] == "face":
            if entry["roi"]["@character"] not in characters and entry["roi"].get("@character", None) is not None:
                characters.append(entry["roi"]["@character"])
    return characters

def draw_rectangle(img, x0, y0, x1, y1, annotation_type):
    assert annotation_type in ["body", "face", "frame", "text"]
    color = {"body": "#258039", "face": "#f5be41",
             "frame": "#31a9b8", "text": "#cf3721"}[annotation_type]
    draw = ImageDraw.Draw(img)
    draw.rectangle([x0, y0, x1, y1], outline=color, width=10)

def draw_annotations_on_image(img_path, df, annotations_list):
    img = Image.open(img_path)
    draw = ImageDraw.Draw(img)

    for index, entry in df.iterrows():
        roi = entry["roi"]
        x0 = int(roi["@xmin"])
        y0 = int(roi["@ymin"])
        x1 = int(roi["@xmax"])
        y1 = int(roi["@ymax"])

        if entry["annotation"] in annotations_list:
            draw_rectangle(img, x0, y0, x1, y1, entry["annotation"])

    return img
    
    
# Get a random entry from the annotations df
def get_random_entry(annotations_list, bool_next):

# Get Book, If next page get next book else get current book
    if bool_next:
        book = get_page.get_next_book('')
    else:
        book = get_page.curr_book()

    df, img_path = get_all_images_and_annotations(manga109_root_dir, book, bool_next)

    # draw annotations on image
    img = draw_annotations_on_image(img_path, df, annotations_list)

    # Get Characters
    characters = get_characters(df)

    # Get File Path
    filename = os.path.basename(img_path)
    page_number, _ = os.path.splitext(filename)

    return img, page_number, book, characters


# Testing
#get_random_entry(["face", "body", "frame", "text"], test = True)





# TODO make a way for when the checkboxes are pressed it updates the highlighted annotations 
# 