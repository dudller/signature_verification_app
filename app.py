from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageDraw
from MLmodule import check_signature, make_new_model


class App:
    signature_from_file = None
    signature_from_canvas = None
    username = ""
    result = False
    mouse_left_button = 'up'
    mouse_right_button = 'up'
    mouse_x, mouse_y = None, None
    WIDTH = 700
    HEIGHT = 300

    def mouse_left_button_down(self, event=None):
        self.mouse_left_button = 'down'

    def mouse_left_button_up(self, event=None):
        self.mouse_left_button = 'up'
        self.mouse_x, self.mouse_y = None, None

    def motion(self, event=None):
        if self.mouse_left_button is 'down':
            if self.mouse_y is not None and self.mouse_x is not None:
                event.widget.create_line(
                    self.mouse_x, self.mouse_y, event.x, event.y, smooth=True)
                self.draw.line(
                    [self.mouse_x, self.mouse_y, event.x, event.y], fill='black', width=1, joint=None)

            self.mouse_x, self.mouse_y = event.x, event.y

    def log_in(self):
        if self.username is not "":
            if self.signature_from_file is not None:
                self.result = check_signature(
                    self.signature_from_file, self.username)
            elif self.signature_from_canvas is not None:
                self.result = check_signature(
                    self.signature_from_file, self.username)

            if self.result is True:
                print("login succes")
            else:
                print("wrong signature")
        else:
            print("no username")

    def load_img(self):
        path = filedialog.askopenfilename(filetypes=(
            ("PNG files", "*.png"), ("JPG files", "*.jpg")))
        self.signature_from_file = Image.open(path)
        self.signature_from_file.show()

    def make_new_user(self):
        print("new user")

    def __init__(self, root):
        root.geometry("1000x500")
        root.configure(background='lightgray')
        root.resizable(0, 0)
        # controlls
        controls = Frame(root, padx=5, pady=5)
        new_user_button = Button(
            controls, text="Make new user", command=self.make_new_user)
        new_user_button.pack()
        username_label = Label(controls, text='Username')
        username_label.pack()
        username_area = Entry(controls)
        username_area.pack()
        use_image_button = Button(
            controls, text="Browse image from a file", command=self.load_img)
        use_image_button.pack()
        log_in_button = Button(controls, text='Log in', command=self.log_in)
        log_in_button.pack()

        controls.pack(side=LEFT)
        # canvas
        self.signature_from_canvas = Image.new(
            "RGB", (self.WIDTH, self.HEIGHT), (255, 255, 255))
        self.draw = ImageDraw.Draw(self.signature_from_canvas)

        write_canvas = Canvas(root, width=self.WIDTH,
                              height=self.HEIGHT, bg='white')
        write_canvas.pack(side=RIGHT)
        write_canvas.bind("<B1-Motion>", self.motion)
        write_canvas.bind("<Button-1>", self.mouse_left_button_down)
        write_canvas.bind("<ButtonRelease-1>", self.mouse_left_button_up)


root = Tk()
root.title('Signature security')
app = App(root)

root.mainloop()
