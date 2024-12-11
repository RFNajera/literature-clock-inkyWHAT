#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Edited on Tue Dec 10 2024

@author: RFNajera
"""
Last login: Wed Dec 11 08:58:47 on ttys000
rnajera@Renes-MacBook-Pro-M1 ~ % ssh rnajera@litclock.local
rnajera@litclock.local's password: 
Linux litclock 6.6.51+rpt-rpi-v7 #1 SMP Raspbian 1:6.6.51-1+rpt3 (2024-10-08) armv7l

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Wed Dec 11 08:58:55 2024 from 192.168.86.43
rnajera@litclock:~ $ ls
Bookshelf  Desktop  Documents  Downloads  inky  literature-clock  Music  Pictures  Pimoroni  Public  Templates  Videos
rnajera@litclock:~ $ cd literature-clock
rnajera@litclock:~/literature-clock $ ls
csv_to_json.R  LICENCE.md              lit_clock.desktop  log.txt      pi_clock_what3_copy.py  README.md  venv
docs           litclock_annotated.csv  log_minute.txt     pi_clock.py  pi_clock_what3.py       temp.png
rnajera@litclock:~/literature-clock $ sudo nano pi_clock_what3.py
rnajera@litclock:~/literature-clock $ python3 pi_clock_what3.py
rnajera@litclock:~/literature-clock $ sudo nano pi_clock_what3.py
rnajera@litclock:~/literature-clock $ python3 pi_clock_what3.py
rnajera@litclock:~/literature-clock $ sudo nano pi_clock_what3.py
rnajera@litclock:~/literature-clock $ python3 pi_clock_what3.py
rnajera@litclock:~/literature-clock $ sudo nano pi_clock_what3.py
rnajera@litclock:~/literature-clock $ python3 pi_clock_what3.py
Traceback (most recent call last):
  File "/home/rnajera/literature-clock/pi_clock_what3.py", line 167, in <module>
    clock.update_display()
  File "/home/rnajera/literature-clock/pi_clock_what3.py", line 154, in update_display
    img = self.generate_image(quote, time_str)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/rnajera/literature-clock/pi_clock_what3.py", line 118, in generate_image
    draw.text((margin + draw.textbbox((0, 0), line[:start] + line[start:end]-1, font=highlight_font)[2], y_offset), line[end:], fill=inky_display.BLACK, font=font_quote)
                                              ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^~
TypeError: unsupported operand type(s) for -: 'str' and 'int'
rnajera@litclock:~/literature-clock $ sudo nano pi_clock_what3.py
rnajera@litclock:~/literature-clock $ python3 pi_clock_what3.py
Traceback (most recent call last):
  File "/home/rnajera/literature-clock/pi_clock_what3.py", line 167, in <module>
    clock.update_display()
  File "/home/rnajera/literature-clock/pi_clock_what3.py", line 154, in update_display
    img = self.generate_image(quote, time_str)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/rnajera/literature-clock/pi_clock_what3.py", line 118, in generate_image
    draw.text((margin + draw.textbbox((0, 0), line[:start] + line[start:end] - 1, font=highlight_font)[2], y_offset), line[end:], fill=inky_display.BLACK, font=font_quote)
                                              ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^~~
TypeError: unsupported operand type(s) for -: 'str' and 'int'
rnajera@litclock:~/literature-clock $ sudo nano pi_clock_what3.py
rnajera@litclock:~/literature-clock $ python3 pi_clock_what3.py
rnajera@litclock:~/literature-clock $ sudo nano pi_clock_what3.py















































  GNU nano 7.2                                                                      pi_clock_what3.py                                                                                
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
            if font_quote_size < 8:  # Set a minimum font size
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
                highlight_font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSansBold.ttf", font_quote_size)
                draw.text((margin + draw.textbbox((0, 0), line[:start], font=font_quote)[2], y_offset), line[start:end], fill=inky_display.BLACK, font=highlight_font)
                draw.text((margin + draw.textbbox((0, 0), line[:start] + line[start:end], font=highlight_font)[2], y_offset), line[end:], fill=inky_display.BLACK, font=font_quote)
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
        datetime_text = now.strftime("%B %d, %Y %H:%M")
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
