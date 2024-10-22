import random
import os 

manga109_root_dir = os.path.join(os.path.dirname(__file__), 'manga109', 'Manga109_released_2023_12_07')

page = 0
book = 0

def get_next_book(curr_book):
    global book 

    demo_books = ['','TsubasaNoKioku', 'UltraEleven', 'YamatoNoHane', 'ToutaMairimasu','ReveryEarth', 'TetsuSan', 'SeisinkiVulnus', 'ParaisoRoad']
    book = book + 1

    if book >= len(demo_books):
        book = 1

    return demo_books[book]

def get_new_page():
    page = 22

    return page

def curr_page():
    return page

def curr_book():
    demo_books = ['','TsubasaNoKioku', 'UltraEleven', 'YamatoNoHane', 'ToutaMairimasu','ReveryEarth', 'TetsuSan', 'SeisinkiVulnus', 'ParaisoRoad']
    return demo_books[book]

def get_new_entry():
    book = get_next_book('')
    page = get_new_page()
    

    return book, page

def get_curr_entry():
    book = curr_book()
    page = curr_page()
    

    return book, page
