import io
from PIL import Image, ImageDraw, ImageFont
from src.colors import *

class ImageGen:
    """
    A class responsible for generating images for the tweets.

    Attributes:
        title (str): Title of the song.
        artist (str): Name of the artist.
        album (str): Name of the album.
        line (str): Randomly taken line of the song.
        image_data (bytes): Song cover binary data.
        album_image_data (bytes): Album cover binary data used for the image's background.
        primary_color (str): Primary color of the album cover represented in a hex value. .
        secondary_color (str): Secondary color of the album cover represented in a hex value. 

    Methods:
        add_corners(): Adds corners to provided image.
        prepare_album_cover(): Responsible for adding gradient to the album cover.
        generate(): Generates the image.
    """

    def __init__(self, title: str, artist: str, album: str, line: str, image_data: bytes, album_image_data: bytes, 
            primary_color: str, secondary_color: str, text_color: str):
        self.title = title
        self.artist = artist 
        self.album = album 
        self.line = line
        self.image_data = image_data 
        self.album_image_data = album_image_data
        self.primary_color = primary_color 
        self.secondary_color = secondary_color
        self.text_color = hex_to_rgb(text_color)

    def add_corners(self, image: Image, radius: int) -> Image:
        if image.mode == "P":
            image = image.convert("RGBA")

        circle = Image.new('L', (radius * 2, radius * 2), 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, radius * 2 - 1, radius * 2 - 1), fill=255)
        alpha = Image.new('L', image.size, 255)
        width, height = image.size
        alpha.paste(circle.crop((0, 0, radius, radius)), (0, 0))
        alpha.paste(circle.crop((0, radius, radius, radius * 2)), (0, height - radius))
        alpha.paste(circle.crop((radius, 0, radius * 2, radius)), (width - radius, 0))
        alpha.paste(circle.crop((radius, radius, radius * 2, radius * 2)), (width - radius, height - radius))
        image.putalpha(alpha)
        
        return image

    def prepare_album_cover(self) -> Image:
        image = Image.open(io.BytesIO(self.album_image_data))

        if image.mode == "P":
            image = image.convert("RGBA")

        width, height = image.size

        gradient = Image.linear_gradient('L')
        gradient = gradient.rotate(90, expand=True)
        gradient = gradient.resize((height, width + 40))

        alpha = Image.new('L', (width, height), 'white')
        alpha.paste(gradient)
        image.putalpha(alpha)
        image = image.resize((400, 400))

        return image

    def generate(self) -> Image:
        margin = 30

        width, height = 746, 400
        primary_color_hex, secondary_color_hex = compare_hex_colors(self.primary_color, self.secondary_color)

        primary_color = hex_to_rgb(primary_color_hex)
        secondary_color = hex_to_rgb(secondary_color_hex)

        image = Image.new('RGBA', (width, height))

        for x in range(width):
            factor = x / (width - 1)

            r = int(primary_color[0] * (1 - factor) + secondary_color[0] * factor)
            g = int(primary_color[1] * (1 - factor) + secondary_color[1] * factor)
            b = int(primary_color[2] * (1 - factor) + secondary_color[2] * factor)

            for y in range(height):
                image.putpixel((x, y), (r, g, b))

        album_cover = self.prepare_album_cover()
        album_cover.convert('RGBA')
        image.paste(album_cover, (346, 0), album_cover)

        song_cover = Image.open(io.BytesIO(self.image_data)).resize((80, 80))
        song_cover.resize((80, 80))
        song_cover = self.add_corners(song_cover, 10)
        song_cover.convert('RGBA')
        image.paste(song_cover, (margin, margin), song_cover)
   
        draw = ImageDraw.Draw(image)

        title_font = ImageFont.truetype("fonts/Roboto-Bold.ttf", 26)
        artist_font = ImageFont.truetype("fonts/Roboto-Bold.ttf", 20)
        line_font = ImageFont.truetype("fonts/Roboto-Bold.ttf", 30)
        watermark_font = ImageFont.truetype("fonts/Roboto-Bold.ttf", 15)

        title_bbox = draw.textbbox((0, 0), self.title, font=title_font)
        artist_bbox = draw.textbbox((0, 0), self.artist, font=artist_font)
        line_bbox = draw.textbbox((0, 0), self.line, font=line_font)

        title_y = ((margin + 80) // 2) - title_bbox[1] - 10
        artist_y = ((margin + 80) // 2) + artist_bbox[1] + 10
        line_y = (height // 2) - line_bbox[1]

        draw.text(((margin + 110), title_y), self.title, fill=self.text_color, font=title_font)
        draw.text(((margin + 110), artist_y), self.artist, fill=self.text_color, font=artist_font)
        draw.text((margin, line_y), self.line, fill=self.text_color, font=line_font)
        draw.text((margin, 400 - margin - 15), "@sentinobot", fill=self.text_color, font=watermark_font)

        return image
