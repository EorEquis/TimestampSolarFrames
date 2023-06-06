import os
from PIL import Image, ImageDraw, ImageFont

img_directory = "/path/to/images"                       # Location of images to be annotated
output_directory = "/path/to/save/annotated/images"     # Location to save annotated images
desired_date = "2023-01-01"                             # Date of images.  If images cross midnight, use date of first images.  Could also extract from filename if present
utc_offset = 5                                          # UTC Offset in hours
font_file = "/path/to/font/somefont.ttf"                # Should be a TTF
font_size = 14                                          # Font size for the timestamp
annotation_x_pos = 10                                   # x and y position to place annotation
annotation_y_pos = 10

# Get list of images in directory
image_files = [f for f in os.listdir(img_directory) if os.path.isfile(os.path.join(img_directory, f))]

# Loop through images and annotate
for image_file in image_files:
    image_path = os.path.join(img_directory, image_file)

    image = Image.open(image_path)

    # Get time from file name.  
    time_parts = image_file.split("_")[0:3]             # Presumes time is HH_MM_SS. If not, change this line to suit.
    hour = int(time_parts[0]) + utc_offset
    minute = int(time_parts[1])
    second = int(time_parts[2])

    # Timestamp string to annotate.
    timestamp_str = f"{desired_date} {hour:02d}:{minute:02d}:{second:02d} UTC"

    # Creates copy of image.  Honestly don't know why this is necessary, but annotating the original image broke shit.
    annotated_image = image.copy()

    draw = ImageDraw.Draw(annotated_image)
    font = ImageFont.truetype(font_file, font_size)

    draw.text((annotation_x_pos, annotation_y_pos), timestamp_str, font=font, fill=(255))   # 255 is white.  Adjust as necssary.  Presumes mono image

    annotated_file = f"annotated_{image_file.split('.')[0]}.png"        # Pillow breaks tifs for some reason.  Converting to PNG
    annotated_path = os.path.join(output_directory, annotated_file)
    annotated_image.save(annotated_path, format="PNG")
    
    image.close()

    # Print something to console so we know it's working
    print("Annotated image saved:", annotated_path)
