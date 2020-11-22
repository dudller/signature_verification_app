from tkinter import *
from PIL import Image, ImageDraw


class App:
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
        print(self.signature)

    def load_img(self):
        return 0

    def __init__(self, root):
        root.geometry("1000x500")
        root.configure(background='lightgray')
        root.resizable(0, 0)
        # controlls
        controls = Frame(root, padx=5, pady=5)
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
        self.signature = Image.new(
            "RGB", (self.WIDTH, self.HEIGHT), (255, 255, 255))
        self.draw = ImageDraw.Draw(self.signature)

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
