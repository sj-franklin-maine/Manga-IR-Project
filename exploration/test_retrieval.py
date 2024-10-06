###
### Sample code provided from: https://github.com/manga109/manga109api
###

# Testing examples from manga109 API

import manga109api
from pprint import pprint

# (0) Instantiate a parser with the root directory of Manga109
manga109_root_dir = "Manga109/Manga109_released_2023_12_07"
p = manga109api.Parser(root_dir=manga109_root_dir)


# (1) Book titles 
print(p.books)
# Output: ['ARMS', 'AisazuNihaIrarenai', 'AkkeraKanjinchou', 'Akuhamu', ...


# (2) Path to an image (page).
print(p.img_path(book="ARMS", index=3))  # the 4th page of "ARMS"
# Output (str): YOUR_DIR/Manga109_2017_09_28/images/ARMS/003.jpg


# (3) The main annotation data
annotation = p.get_annotation(book="ARMS")

# annotation is a dictionary. Keys are "title", "character", and "page":
# - annotation["title"] : (str) Title
# - annotation["character"] : (list) Characters who appear in the book
# - annotation["page"] : (list) The main annotation data for each page

# (3-a) title
print(annotation["title"])  # Output (str): ARMS

# (3-b) character
pprint(annotation["character"])
# Output (list):
# [{'@id': '00000003', '@name': '女1'},
#  {'@id': '00000010', '@name': '男1'},
#  {'@id': '00000090', '@name': 'ロボット1'},
#  {'@id': '000000fe', '@name': 'エリー'},
#  {'@id': '0000010a', '@name': 'ケイト'}, ... ]

# (3-c) page
# annotation["page"] is the main annotation data (list of pages)
pprint(annotation["page"][3])  # the data of the 4th page of "ARMS"
# Output (dict):
# {'@height': 1170,    <- Height of the img
#  '@index': 3,        <- The page number
#  '@width': 1654,     <- Width of the img
#  'body': [{'@character': '00000003',     <- Character body annotations
#            '@id': '00000006',
#            '@xmax': 1352,
#            '@xmin': 1229,
#            '@ymax': 875,
#            '@ymin': 709},
#           {'@character': '00000003',   <- character ID
#            '@id': '00000008',          <- annotation ID (unique)
#            '@xmax': 1172,
#            '@xmin': 959,
#            '@ymax': 1089,
#            '@ymin': 820}, ... ],
#  'face': [{'@character': '00000003',     <- Character face annotations
#            '@id': '0000000a',
#            '@xmax': 1072,
#            '@xmin': 989,
#            '@ymax': 941,
#            '@ymin': 890},
#           {'@character': '00000003',
#            '@id': '0000000d',
#            '@xmax': 453,
#            '@xmin': 341,
#            '@ymax': 700,
#            '@ymin': 615}, ... ],
#  'frame': [{'@id': '00000009',        <- Frame annotations
#             '@xmax': 1170,
#             '@xmin': 899,
#             '@ymax': 1085,
#             '@ymin': 585},
#            {'@id': '0000000c',
#             '@xmax': 826,
#             '@xmin': 2,
#             '@ymax': 513,
#             '@ymin': 0}, ... ],
#  'text': [{'#text': 'キャーッ',     <- Speech annotations
#            '@id': '00000005',
#            '@xmax': 685,
#            '@xmin': 601,
#            '@ymax': 402,
#            '@ymin': 291},
#           {'#text': 'はやく逃げないとまきぞえくっちゃう',   <- Text data
#            '@id': '00000007',
#            '@xmax': 1239,
#            '@xmin': 1155,
#            '@ymax': 686,
#            '@ymin': 595} ... ]}

# (4) Preserve the raw tag ordering in the output annotation data
annotation_ordered = p.get_annotation(book="ARMS", separate_by_tag=False)

# In the raw XML in the Manga109 dataset, the bounding box data in the
# `page` tag is not sorted by its annotation type, and each bounding
# box type appears in an arbitrary order. When the `separate_by_tag=False`
# option is set, the output will preserve the ordering of each
# bounding box tag in the raw XML data, mainly for data editing purposes.
# Note that the ordering of the bounding box tags does not carry any
# useful information about the contents of the data.

# Caution: Due to the aforementioned feature, the format of the output
# dictionary will differ slightly comapred to when the option is not set.

# Here is an example output of the ordered data:
pprint(annotation_ordered["page"][3])  # the data of the 4th page of "ARMS"
# Output (dict):
# {'@height': 1170,
#  '@index': 3,
#  '@width': 1654,
#  'contents': [{'#text': 'キャーッ',
#                '@id': '00000005',
#                '@xmax': 685,
#                '@xmin': 601,
#                '@ymax': 402,
#                '@ymin': 291,
#                'type': 'text'},
#               {'@character': '00000003',
#                '@id': '00000006',
#                '@xmax': 1352,
#                '@xmin': 1229,
#                '@ymax': 875,
#                '@ymin': 709,
#                'type': 'body'},
#               {'#text': 'はやく逃げないとまきぞえくっちゃう',
#                '@id': '00000007',
#                '@xmax': 1239,
#                '@xmin': 1155,
#                '@ymax': 686,
#                '@ymin': 595,
#                'type': 'text'}, ... ]}