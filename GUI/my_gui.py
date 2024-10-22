import tkinter as tk
from tkinter import Label, Checkbutton
import matplotlib.pyplot as plt
import show_image
from PIL import ImageTk, Image
import tkinter.font as tkFont

annotations_list = []
bool_next = True

class MyGUI:


    def __init__(self, root):
        self.root = root


        # Set Process Title and window size
        self.root.title("Manga109 Database Viewer")
        self.root.geometry("1200x600")

        # Set Default Font 
        font = tkFont.Font(family="Times", size=12, weight="bold")


        # Get a random entry from the database and Display
        img, page_num, book, characters = show_image.get_random_entry(annotations_list=annotations_list, bool_next=True)
        self.display_image(img)

        # Set the book name and page number
        self.root.book_label = Label(self.root, text=f"Name: {book}", font=font, padx=10, pady=10, bg="white")
        self.root.book_label.place(x=200, y=7)  

        book_label_width = self.root.book_label.winfo_reqwidth()
        self.root.page_label = Label(self.root, text=f"Page: {page_num}", font=font, padx=10, pady=10, bg="white")
        self.root.page_label.place(x=book_label_width + 210, y=7)  # Adjust the y value to move the label down the y axi

                    #TODO Add a list of characters in the image
        character_title_font = tkFont.Font(family="Times", size=18, weight="bold", underline=True)
        self.root.page_label = Label(self.root, text=f"Characters", font=character_title_font, padx=10, pady=10)
        self.root.page_label.place(x=1025, y=50)

        characters_font = tkFont.Font(family="Times", size=12, weight="bold")
        self.root.characters_list = Label(self.root, text=f"Characters", font=characters_font, padx=10, pady=10)

        characters_str = ""
        for character in characters:
            characters_str += character + "\n"
        self.root.characters_list.config(text=characters_str)

        self.root.characters_list.place(x=1025, y=88)

        # Create Checkboxes for Annotations
        self.checkbox_var1 = tk.BooleanVar()
        self.checkbox_var2 = tk.BooleanVar()
        self.checkbox_var3 = tk.BooleanVar()
        self.checkbox_var4 = tk.BooleanVar()

        # Annotation Toggles
        self.checkbox1 = Checkbutton(self.root, text="Face", variable=self.checkbox_var1, font=font, command=self.toggle_annotations)
        self.checkbox1.place(x=10, y=50)

        self.checkbox2 = Checkbutton(self.root, text="Body", variable=self.checkbox_var2, font=font, command=self.toggle_annotations)
        self.checkbox2.place(x=10, y=80)

        self.checkbox3 = Checkbutton(self.root, text="Frame", variable=self.checkbox_var3, font=font, command=self.toggle_annotations)
        self.checkbox3.place(x=10, y=110)

        self.checkbox4 = Checkbutton(self.root, text="Text", variable=self.checkbox_var4, font=font, command=self.toggle_annotations)
        self.checkbox4.place(x=10, y=140)

        # Add a button to generate a new image
        self.generate_button = tk.Button(self.root, text="Generate", font=font, command=self.generate_new_image)
        self.generate_button.place(relx=0.5, y=550, anchor="n")

        self.root.mainloop()
        

    def display_image(self, img):
        # Resize the image to fit within the window while maintaining aspect ratio
        img = img.resize((800, 500), Image.LANCZOS)
        
        # Convert the image to a PhotoImage
        photo = ImageTk.PhotoImage(img)
        
        # Create a label to display the image
        label = Label(self.root, image=photo, width=1200, height=600)
        label.image = photo  # Keep a reference to avoid garbage collection
        label.pack()

    def toggle_annotations(self):
        global annotations_list
        global bool_next

        annotations_list.clear()

        if self.checkbox_var1.get():
            annotations_list.append("face")
        else:
            if annotations_list.count("face") > 0:
                annotations_list.remove("face")
        if self.checkbox_var2.get():
            annotations_list.append("body")
        else:
            if annotations_list.count("body") > 0:
                annotations_list.remove("body")
        if self.checkbox_var3.get():
            annotations_list.append("frame")
        else:
            if annotations_list.count("frame") > 0:
                annotations_list.remove("frame")
        if self.checkbox_var4.get():
            annotations_list.append("text")
        else:
            if annotations_list.count("text") > 0:
                annotations_list.remove("text")

        bool_next = False

        self.generate_image()
    
    def generate_new_image(self):
        global bool_next
        bool_next = True

        self.generate_image()

    def generate_image(self):
        global bool_next
        global annotations_list

        # Clear the existing image
        for widget in self.root.winfo_children():
            if isinstance(widget, Label):
                widget.destroy()

        font = tkFont.Font(family="Times", size=12, weight="bold")

        img, page_num, book, characters = show_image.get_random_entry(annotations_list, bool_next)

        self.display_image(img)

        self.root.book_label = Label(self.root, text=f"Name: {book}", font=font, padx=10, pady=10, bg="white")
        self.root.book_label.place(x=200, y=7)  

        book_label_width = self.root.book_label.winfo_reqwidth()
        self.root.page_label = Label(self.root, text=f"Page: {page_num}", font=font, padx=10, pady=10, bg="white")
        self.root.page_label.place(x=book_label_width + 210, y=7)  # Adjust the y value to move the label down the y axis

        self.generate_button = tk.Button(self.root, text="Generate", font=font, command=self.generate_new_image)
        self.generate_button.place(relx=0.5, y=550, anchor="n")

        # Add a list of characters in the image
        character_title_font = tkFont.Font(family="Times", size=18, weight="bold", underline=True)
        self.root.page_label = Label(self.root, text=f"Characters", font=character_title_font, padx=10, pady=10)
        self.root.page_label.place(x=1025, y=50)

        characters_font = tkFont.Font(family="Times", size=12, weight="bold")
        self.root.characters_list = Label(self.root, text=f"Characters", font=characters_font, padx=10, pady=10)

        characters_str = ""
        for character in characters:
            characters_str += character + "\n"
        self.root.characters_list.config(text=characters_str)

        # Create Checkboxes for Annotations
        self.checkbox_var1 = tk.BooleanVar()
        self.checkbox_var2 = tk.BooleanVar()
        self.checkbox_var3 = tk.BooleanVar()
        self.checkbox_var4 = tk.BooleanVar()

        # Annotation Toggles
        if annotations_list.count("face") > 0:
            self.checkbox_var1.set(True)
        self.checkbox1 = Checkbutton(self.root, text="Face", variable=self.checkbox_var1, font=font, command=self.toggle_annotations)
        self.checkbox1.place(x=10, y=50)
        
        if annotations_list.count("body") > 0:
            self.checkbox_var2.set(True)
        self.checkbox2 = Checkbutton(self.root, text="Body", variable=self.checkbox_var2, font=font, command=self.toggle_annotations)
        self.checkbox2.place(x=10, y=80)

        if annotations_list.count("frame") > 0:
            self.checkbox_var3.set(True)
        self.checkbox3 = Checkbutton(self.root, text="Frame", variable=self.checkbox_var3, font=font, command=self.toggle_annotations)
        self.checkbox3.place(x=10, y=110)

        if annotations_list.count("text") > 0:
            self.checkbox_var4.set(True)
        self.checkbox4 = Checkbutton(self.root, text="Text", variable=self.checkbox_var4, font=font, command=self.toggle_annotations)
        self.checkbox4.place(x=10, y=140)


        self.root.characters_list.place(x=1025, y=88)




MyGUI(tk.Tk())