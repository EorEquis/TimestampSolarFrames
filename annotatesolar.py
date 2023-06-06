import os
from PIL import Image, ImageDraw, ImageFont

img_directory = "/path/to/images"                       # Location of images to be annotated
output_directory = "/path/to/save/annotated/images"     # Location to save annotated images
font_file = "/path/to/font/somefont.ttf"                # Should be a TTF
desired_date = "2023-01-01"                             # Date of images.  If images cross midnight, use date of first images.  Could also extract from filename if present
utc_offset = 5                                          # UTC Offset in hours
font_size = 14                                          # Font size for the timestamp
annotation_x_pos = 10                                   # x and y position to place annotation
annotation_y_pos = 10
border_size = 1                                         # Text border size in pixels, 0 for no border.
border_color = 0                                        # 0 (black) to 255 (white), RGB will have all channels set to this value.

# Get list of images in directory
image_files = [f for f in os.listdir(img_directory) if os.path.isfile(os.path.join(img_directory, f))]

# Find color space of first file, so we can process correctly below.
first_image_path = os.path.join(img_directory, image_files[0])
first_image = Image.open(first_image_path)
color_space = first_image.mode
first_image.close()

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

    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_file, font_size)
    
    if color_space == "RGB":
        draw.text((annotation_x_pos, annotation_y_pos), timestamp_str, font=font, fill=(255,255,255), stroke_width=border_size, stroke_fill=(border_color,border_color,border_color))   # RGB color values.
        annotated_file = f"annotated_{image_file}"
        annotated_path = os.path.join(output_directory, annotated_file)
        image.save(annotated_path)
    elif color_space == "L":
        draw.text((annotation_x_pos, annotation_y_pos), timestamp_str, font=font, fill=(255), stroke_width=border_size, stroke_fill=(border_color))   # Only a single value is required for greyscale images
        annotated_file = f"annotated_{image_file}"
        annotated_path = os.path.join(output_directory, annotated_file)
        image.save(annotated_path)
    elif color_space == "I;16":
        draw.text((annotation_x_pos, annotation_y_pos), timestamp_str, font=font, fill=(255), stroke_width=border_size, stroke_fill=(border_color))   # Only a single value is required for greyscale images
        annotated_file = f"annotated_{image_file.split('.')[0]}.png"        # So some things (PI, PIPP) don't like the I;16 greyscale output as TIF for some reason...
        annotated_path = os.path.join(output_directory, annotated_file)
        image.save(annotated_path, format="PNG")                            # So we make them .PNG

    image.close()

    # Print something to console so we know it's working
    print("Annotated image saved:", annotated_path)
