import manga109api
import random
import os


def get_random_book(manga109_root_dir):

    p = manga109api.Parser(manga109_root_dir)
    books = p.books
    random_book = random.choice(books)

    return random_book

def main():
    manga109_root_dir = os.path.join(os.path.dirname(__file__), 'manga109', 'Manga109_released_2023_12_07')
    random_book = get_random_book(manga109_root_dir)
    
    print(random_book)

if __name__ == "__main__":
    main()

print(get_random_book())