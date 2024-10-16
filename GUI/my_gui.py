import tkinter as tk
from tkinter import Label, Checkbutton
import matplotlib.pyplot as plt
import show_image
from PIL import ImageTk, Image
import tkinter.font as tkFont

class MyGUI:

    def __init__(self, root):
        self.root = root

        # Set Process Title and window size
        self.root.title("Manga109 Database Viewer")
        self.root.geometry("1200x600")

        # Set Default Font 
        font = tkFont.Font(family="Times", size=12, weight="bold")

        # Get a random entry from the database and Display
        img_path, page_num, annotation_type, book = show_image.get_random_entry()
        self.display_image(img_path)

        # Set the book name and page number
        self.root.book_label = Label(self.root, text=f"Name: {book}", font=font, padx=10, pady=10, bg="white")
        self.root.book_label.place(x=200, y=7)  

        book_label_width = self.root.book_label.winfo_reqwidth()
        self.root.page_label = Label(self.root, text=f"Page: {page_num}", font=font, padx=10, pady=10, bg="white")
        self.root.page_label.place(x=book_label_width + 210, y=7)  # Adjust the y value to move the label down the y axi

        #TODO Add a list of characters in the image
        characters_font = tkFont.Font(family="Times", size=18, weight="bold", underline=True)
        self.root.characters_list = Label(self.root, text=f"Characters", font=characters_font, padx=10, pady=10)
        self.root.characters_list.place(x=1025, y=50)

        # Add a button to generate a new image
        self.generate_button = tk.Button(self.root, text="Generate", font=font, command=self.generate_image)
        self.generate_button.place(relx=0.5, y=550, anchor="n")

        #self.checkbox_var1 = tk.BooleanVar()
        #self.checkbox_var2 = tk.BooleanVar()

        #self.checkbox1 = Checkbutton(self.root, text="Option 1", variable=self.checkbox_var1, font=font)
        #self.checkbox1.place(x=10, y=50)

        #self.checkbox2 = Checkbutton(self.root, text="Option 2", variable=self.checkbox_var2, font=font)
        #self.checkbox2.place(x=10, y=80)


        self.root.mainloop()

    def display_image(self, img_path):
        # Open the image
        img = Image.open(img_path)
        
        # Resize the image to fit within the window while maintaining aspect ratio
        img = img.resize((800, 500), Image.LANCZOS)
        
        # Convert the image to a PhotoImage
        photo = ImageTk.PhotoImage(img)
        
        # Create a label to display the image
        label = Label(self.root, image=photo, width=1200, height=600)
        label.image = photo  # Keep a reference to avoid garbage collection
        label.pack()

    def generate_image(self):
        # Clear the existing image
        for widget in self.root.winfo_children():
            if isinstance(widget, Label):
                widget.destroy()

        # Set New Image 
        font = tkFont.Font(family="Times", size=12, weight="bold")

        img_path, page_num, annotation_type, book = show_image.get_random_entry()

        self.display_image(img_path)
        self.root.book_label = Label(self.root, text=f"Name: {book}", font=font, padx=10, pady=10, bg="white")
        self.root.book_label.place(x=200, y=7)  

        book_label_width = self.root.book_label.winfo_reqwidth()
        self.root.page_label = Label(self.root, text=f"Page: {page_num}", font=font, padx=10, pady=10, bg="white")
        self.root.page_label.place(x=book_label_width + 210, y=7)  # Adjust the y value to move the label down the y axis

        self.generate_button = tk.Button(self.root, text="Generate", font=font, command=self.generate_image)
        self.generate_button.place(relx=0.5, y=550, anchor="n")


MyGUI(tk.Tk())