from PIL import Image, ImageDraw, ImageFont
import io
import os

class DonorCardGenerator:

    def __init__(self):

        self.exec_path = "donor/ImageGenerator"

        self.template_image = Image.open(os.path.join(self.exec_path, "assets/image/template.png")).convert("RGBA")
        self.input_image = ""

        self.width = 524
        self.height = 862
        self.red_color = (223, 42, 25)
        self.normal_font = os.path.join(self.exec_path, "assets/font/NotoSansKR-Medium.otf")
        self.light_font = os.path.join(self.exec_path, "assets/font/NotoSansKR-Light.otf")
        self.context_font = os.path.join(self.exec_path, "assets/font/GamjaFlower-Regular.ttf")

    def write_user_image(self, input_image_id):

        input_image_id = str(input_image_id).zfill(2)
        input_image = os.path.join(self.exec_path, "assets/image/{}.png".format(input_image_id))

        self.input_image = Image.open(input_image).convert("RGBA")
        self.input_image = self.input_image.resize((200, 200))
        self.template_image.paste(self.input_image, (270, 380), self.input_image)

    def write_template_text(self, date, place, type, volume, num):

        draw = ImageDraw.Draw(self.template_image)
        font_light = ImageFont.truetype(self.light_font, 24)
        font_normal = ImageFont.truetype(self.normal_font, 58)

        draw.text((50, 50), date, self.red_color, font_light)
        draw.text((50, 565), place, self.red_color, font_light)
        draw.text((50, 600), "{} {}ML".format(type, volume), self.red_color, font_normal)
        draw.text((350, 805), num, (248, 161, 156), font_light)

    def write_user_text(self, text):
        draw = ImageDraw.Draw(self.template_image)
        font_context = ImageFont.truetype(self.context_font, 34)
        text_width, text_height = draw.textsize(text, font=font_context)

        shape = [((self.width - text_width) / 2 - 10, 150 - 10), ((self.width - text_width) / 2 + text_width + 10, 150 + text_height + 10)]
        draw.rectangle(shape, fill="#FFEBE9")
        draw.text(((self.width - text_width) / 2, 150), text, self.red_color, font_context)

    def get_binary_image(self):

        output = io.BytesIO()
        self.template_image.save(output, "PNG")
        return output

    def show_image(self):
        self.template_image.show()
