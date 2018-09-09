import io
import requests
from PIL import Image, ImageTk
from six.moves import tkinter as tk


class GuiCaptchaHandler(object):

    @staticmethod
    def _get_captcha_image(captcha_image_url):
        response = requests.get(captcha_image_url)
        captcha_image_bytes = io.BytesIO(response.content)
        captcha_image = Image.open(captcha_image_bytes)
        return ImageTk.PhotoImage(captcha_image)

    def __call__(self, _, captcha_image_url):
        root = tk.Tk()
        root.title("Captcha")

        frame = tk.Frame(root)
        frame.pack()

        captcha_image = self._get_captcha_image(captcha_image_url)
        captcha_label = tk.Label(frame, image=captcha_image)
        captcha_label.pack()

        captcha_var = tk.StringVar(frame)
        captcha_input = tk.Entry(frame, textvariable=captcha_var)
        captcha_input.focus_set()
        captcha_input.pack()

        button = tk.Button(frame, text="Go", command=root.destroy)
        captcha_input.bind("<Return>", lambda _: button.invoke())
        button.pack()

        root.mainloop()

        return captcha_var.get()
