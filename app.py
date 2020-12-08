from tkinter import *
from tkinter import filedialog, ttk, messagebox, StringVar
from PIL import Image, EpsImagePlugin
from MLmodule import check_signature, make_new_model
from skimage.io import imread, imshow
import os


class App:
    signature_from_file = None
    canvas_used = False
    images = []
    username = None
    result = False
    mouse_left_button = 'up'
    mouse_x, mouse_y = None, None
    WIDTH = 700
    HEIGHT = 300

    def mouse_left_button_down(self, event=None):
        self.mouse_left_button = 'down'
        self.canvas_used = True

    def mouse_left_button_up(self, event=None):
        self.mouse_left_button = 'up'
        self.mouse_x, self.mouse_y = None, None
        self.write_canvas.postscript(file='temp' + '.eps')

    def motion(self, event=None):
        if self.mouse_left_button is 'down':
            if self.mouse_y is not None and self.mouse_x is not None:
                event.widget.create_line(
                    self.mouse_x, self.mouse_y, event.x, event.y, smooth=True)

            self.mouse_x, self.mouse_y = event.x, event.y

    def log_in(self):
        if self.username is not None:
            if self.signature_from_file is not None:
                self.result = check_signature(
                    self.signature_from_file, self.username.get())
                print('file')
            elif self.canvas_used is True:
                print('canvas')
                im = Image.open('temp.eps')
                fig = im.convert('RGBA')
                fig.save('temp.png', lossless=True)
                sign = imread('temp.png')
                self.result = check_signature(
                    sign, self.username.get())
                os.remove("temp.png")

            print(self.result)
            if self.result == True:
                messagebox.showinfo('Logowanie udane',
                                    'Podpis się zgadza. Zalogowano!')
                self.signature_from_file = None

            else:
                messagebox.showinfo('Logowanie nieudane',
                                    'Nieprawidłowy podpis')
        else:
            messagebox.showinfo('Logowanie nieudane',
                                'Nieprawidłowa nazwa użytkownika')

    def load_img(self):
        try:
            path = filedialog.askopenfilename(filetypes=(
                ("PNG files", "*.png"), ("JPG files", "*.jpg")))
            self.signature_from_file = imread(path)
            imshow(self.signature_from_file)
        except Exception as err:
            print(err)
            messagebox.showinfo('Błąd',
                                'Wystąpił błąd podczas dodawania obrazu')

    def load_imgs(self):
        try:
            path = filedialog.askopenfilenames(filetypes=(
                ("PNG files", "*.png"), ("JPG files", "*.jpg")))
            files = root.tk.splitlist(path)
            self.images = []
            for file in files:
                self.images.append(imread(file))
        except:
            messagebox.showinfo('Błąd',
                                'Wystąpił błąd podczas dodawania obrazu')

    def make_new_user(self):
        if len(self.images) is not 0:
            result = make_new_model(self.images, self.username.get())
        if result:
            print('done')
        else:
            print("nah nah nah")

    def __init__(self, root):
        EpsImagePlugin.gs_windows_binary = 'C:/Program Files/gs/gs9.53.3/bin/gswin64c'
        root.geometry("1000x500")
        root.configure(background='lightgray')
        root.resizable(0, 0)
        panels = ttk.Notebook(root)
        self.username = StringVar()
        # controlls
        controls = Frame(panels, padx=5, pady=5)

        username_label = Label(controls, text='Username')
        username_label.grid(column=0, row=0)
        username_area = Entry(controls, textvariable=self.username)
        username_area.grid(column=0, row=1)
        use_image_button = Button(
            controls, text="Browse image from a file", command=self.load_img)
        use_image_button.grid(column=0, row=2)
        log_in_button = Button(controls, text='Log in', command=self.log_in)
        log_in_button.grid(column=0, row=3)
        self.write_canvas = Canvas(controls, width=self.WIDTH,
                                   height=self.HEIGHT, bg='white')
        self.write_canvas.grid(column=1)
        self.write_canvas.bind("<B1-Motion>", self.motion)
        self.write_canvas.bind("<Button-1>", self.mouse_left_button_down)
        self.write_canvas.bind("<ButtonRelease-1>", self.mouse_left_button_up)
        new_user_panel = Frame(panels, padx=5, pady=5)
        new_username_label = Label(new_user_panel, text='New username')
        new_username_label.grid(column=0, row=0)
        new_username_area = Entry(new_user_panel, textvariable=self.username)
        new_username_area.grid(column=0, row=1)
        new_load_images = Button(
            new_user_panel, text="Upload images", command=self.load_imgs)
        new_load_images.grid(column=0, row=2)
        new_user_button = Button(
            new_user_panel, text="Make new user", command=self.make_new_user)
        new_user_button.grid(column=0, row=3)
        panels.add(controls, text="Log in")
        panels.add(new_user_panel, text="New user")
        panels.pack()


root = Tk()
root.title('Signature security')
app = App(root)

root.mainloop()
