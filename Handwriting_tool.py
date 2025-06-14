import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from litellm import completion
import dotenv, os
from dotenv import load_dotenv,find_dotenv
_ = load_dotenv(find_dotenv())
API_KEY = os.getenv("GEMINI_API_KEY")
os.environ["GEMINI_API_KEY"]=os.getenv("Gemini_API_Key")
def main(Hukam:str):
    font_path = "IndieFlower-Regular.ttf" 
    font_size = 32
    page_width = 2000
    page_height = 1000
    margin = 65
    jitter_range = 2
    line_spacing = font_size + 10
    text_color = (20, 20, 20)

    response = completion(
    model="gemini/gemini-2.0-flash",
    messages=[{ "content":Hukam,"role": "user"}]
    )
    text=response['choices'][0]['message']['content']
    font = ImageFont.truetype(font_path, font_size)

    #Function to create a new blank or textured page
    def create_new_page():
        try:
            bg = Image.open("pagws.jpg").convert("RGB").resize((page_width, page_height))
        except:
            bg = Image.new("RGB", (page_width, page_height), (255, 255, 240))
        return bg

    # Setup first page
    current_page = 1
    background = create_new_page()
    draw = ImageDraw.Draw(background)
    x, y = margin, 50

    # Track created pages
    pages = []
    for char in text:
        if char == '\n':
            x = margin
            y += line_spacing
            continue

        bbox = font.getbbox(char)
        char_width = bbox[2] - bbox[0]

        if x + char_width >= page_width - margin:
            x = margin
            y += line_spacing

        # Create new page if vertical space is exceeded
        if y + line_spacing >= page_height - margin:
            background = background.filter(ImageFilter.GaussianBlur(radius=0.3))
            background.save(f"page_{current_page}.png")
            pages.append(f"page_{current_page}.png")
        #New page
            current_page += 1
            background = create_new_page()
            draw = ImageDraw.Draw(background)
            x, y = margin, 50
        dx = random.randint(-jitter_range, jitter_range)
        dy = random.randint(-jitter_range, jitter_range)
        draw.text((x + dx, y + dy), char, font=font, fill=text_color)

        # Move x forward
        x += char_width

    # Save the final page
    background = background.filter(ImageFilter.GaussianBlur(radius=0.3))
    background.save(f"page_{current_page}.png")
    pages.append(f"page_{current_page}.png")

    print(f"Saved {len(pages)} page(s): {', '.join(pages)}")
