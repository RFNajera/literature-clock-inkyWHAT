#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Edited on Tue Dec 10 2024

@author: RFNajera
"""
import os
import json
import random
from datetime import datetime
from inky import InkyWHAT
from PIL import Image, ImageDraw, ImageFont

# Inky WHAT setup
inky_display = InkyWHAT("black")
inky_display.set_border(inky_display.WHITE)

# Paths and configurations
FONT_PATH = "/usr/share/fonts/truetype/freefont/FreeSans.ttf"
QUOTE_PATH = "docs/times"  # Path to the folder containing the time-based JSON files
IMAGE_SIZE = (inky_display.WIDTH, inky_display.HEIGHT)
FONT_SIZE_QUOTE = 20
FONT_SIZE_AUTHOR = 14
FONT_SIZE_DATETIME = 12

class LiteratureClock:
    def __init__(self, fixed_time=None):
        self.fixed_time = fixed_time
        self.quote_data = self.load_quotes()
        self.font_datetime = ImageFont.truetype(FONT_PATH, FONT_SIZE_DATETIME)

    def load_quotes(self):
        """Load all quotes from JSON files into a dictionary."""
        quotes = {}
        for hour in range(24):
            for minute in range(60):
                time_str = f"{hour:02d}:{minute:02d}"
                file_path = os.path.join(QUOTE_PATH, f"{time_str}.json")
                try:
                    with open(file_path, "r") as file:
                        quotes[time_str] = json.load(file)
                except FileNotFoundError:
                    pass
        return quotes

    def get_quote_for_time(self, time_str):
        """Retrieve a random quote for the given time."""
        if time_str in self.quote_data:
            return random.choice(self.quote_data[time_str])
        return {
            "quote_first": "No quote available.",
            "quote_time_case": "",
            "quote_last": "",
            "title": "N/A",
            "author": "Unknown",
        }

    def wrap_text(self, draw, text, max_width, font):
        """Wrap text to fit within the max width."""
        words = text.split(" ")
        lines = []
        current_line = ""
        for word in words:
            test_line = f"{current_line} {word}".strip()
            if draw.textbbox((0, 0), test_line, font=font)[2] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        return lines

    def generate_image(self, quote, time_str):
        """Generate an image for the Inky WHAT display with dynamic font scaling."""
        # Create a blank image
        img = Image.new("P", IMAGE_SIZE, color=inky_display.WHITE)
        draw = ImageDraw.Draw(img)

        # Quote text
        quote_text = f"{quote['quote_first']} {quote['quote_time_case']} {quote['quote_last']}"
        author_text = f"- {quote['title']}, {quote['author']}"
        margin = 10
        max_width = IMAGE_SIZE[0] - 2 * margin
        max_height = IMAGE_SIZE[1] - 60  # Leave space for date/time and margins

        # Start with default font sizes
        font_quote_size = FONT_SIZE_QUOTE
        font_author_size = FONT_SIZE_AUTHOR
        line_spacing = 10

        # Create fonts
        font_quote = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", font_quote_size)
        font_author = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", font_author_size)

        # Wrap the quote text into lines
        wrapped_lines = self.wrap_text(draw, quote_text, max_width, font_quote)

        # Calculate total height of the quote text
        while True:
            line_height = font_quote.getbbox("A")[3] - font_quote.getbbox("A")[1] + line_spacing
            total_text_height = line_height * len(wrapped_lines)

            # Check if the text fits within the available height
            if total_text_height + 40 <= max_height:  # 40 leaves space for author text
                break  # Text fits, exit the loop

            # Reduce the font size and re-wrap text
            font_quote_size -= 1
            if font_quote_size < 10:  # Set a minimum font size
                break
            font_quote = ImageFont.truetype(FONT_PATH, font_quote_size)
            wrapped_lines = self.wrap_text(draw, quote_text, max_width, font_quote)

        # Render the wrapped quote text line by line
        y_offset = (max_height - total_text_height) // 2 + 30  # Leave space for the date/time at the top
        for line in wrapped_lines:
            if quote['quote_time_case'] in line:
                start = line.find(quote['quote_time_case'])
                end = start + len(quote['quote_time_case'])
                draw.text((margin, y_offset), line[:start], fill=inky_display.BLACK, font=font_quote)
                highlight_font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf", font_quote_size)
                draw.text((margin + draw.textbbox((0, 0), line[:start], font=font_quote)[2], y_offset), line[start:end].upper(), fill=inky_display.BLACK, font=highlight_font)
                draw.text((margin + draw.textbbox((0, 0), line[:start] + line[start:end].upper(), font=highlight_font)[2], y_offset), line[end:], fill=inky_display.BLACK, font=font_quote)
            else:
                draw.text((margin, y_offset), line, fill=inky_display.BLACK, font=font_quote)
            y_offset += line_height

        # Render the author text at the bottom, left-aligned
        draw.text(
            (margin, IMAGE_SIZE[1] - margin - font_author.getbbox(author_text)[3]),
            author_text,
            fill=inky_display.BLACK,
            font=font_author,
        )

        # Render the current date and time at the top-right corner
        now = datetime.now()
        datetime_text = now.strftime("%B %d, %Y")
        datetime_width = draw.textbbox((0, 0), datetime_text, font=self.font_datetime)[2]
        draw.text(
            (IMAGE_SIZE[0] - margin - datetime_width, margin),
            datetime_text,
            fill=inky_display.BLACK,
            font=self.font_datetime,
        )

        return img

    def update_display(self):
        """Update the Inky WHAT display with the current time's quote."""
        # Determine current time
        now = datetime.now()
        time_str = self.fixed_time or now.strftime("%H:%M")

        # Get the quote for the current time
        quote = self.get_quote_for_time(time_str)

        # Generate the image
        img = self.generate_image(quote, time_str)

        # Display the image
        inky_display.set_image(img)
        inky_display.show()


if __name__ == "__main__":
    # Set working directory to script location
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Create LiteratureClock instance and update display
    clock = LiteratureClock()
    clock.update_display()
