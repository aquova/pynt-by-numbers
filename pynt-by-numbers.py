import argparse
from PIL import Image, ImageDraw, ImageFont
from math import floor

LINE_WIDTH = 1
BLACK = "#000000"

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Creates Paint By Numbers image")
    parser.add_argument("file_name", action="store", type=str, help="Filename of input image")
    parser.add_argument("grid_size", action="store", type=int, help="Grid size, in pixels")
    parser.add_argument("out_filename", action="store", type=str, help="Filename of output image")
    parser.add_argument("--legend", dest="show_legend", action="store_true", help="Whether to show the color legend")
    args = parser.parse_args()

    # Import source image as RGB
    source_image_raw = Image.open(args.file_name)
    source_image = source_image_raw.convert("RGB")
    source_size = source_image.size
    out_x = source_size[0]
    out_y = source_size[1]

    # If we're going to render the legend, leave extra room
    if args.show_legend:
        out_y += 2 * args.grid_size

    out_image = Image.new("RGB", (out_x, out_y), "#ffffff")

    draw = ImageDraw.Draw(out_image)
    font = ImageFont.truetype("font/OpenSans-Regular.ttf", 12)

    # Draw boundary box
    draw.line((0, 0, source_size[0], 0), BLACK)
    draw.line((0, 0, 0, source_size[1]), BLACK)
    draw.line((source_size[0], 0, source_size[0], source_size[1]), BLACK)
    draw.line((0, source_size[1], source_size[0], source_size[1]), BLACK)

    # Draw grid on output image
    for x in range(0, source_size[0], args.grid_size):
        draw.line((x, 0, x, source_size[1]), BLACK, width=LINE_WIDTH)
    for y in range(0, source_size[1], args.grid_size):
        draw.line((0, y, source_size[0], y), BLACK, width=LINE_WIDTH)

    # List of discovered colors
    colors = []

    # Iterate through each tile in grid, noting index on output image
    for y in range(0, source_size[1], args.grid_size):
        for x in range(0, source_size[0], args.grid_size):
            color = source_image.getpixel((x, y))
            index = 0
            if color not in colors:
                colors.append(color)
                index = len(colors)
            else:
                index = colors.index(color) + 1

            draw.text((x + args.grid_size / 4, y + args.grid_size / 4), str(index), BLACK, font=font)

    if args.show_legend:
        # Get the margin sizes
        # TODO: Fix situation if we have more legend colors than grid width
        total_whitespace = out_x - (len(colors) * args.grid_size)
        margin_x = floor(total_whitespace / (len(colors) + 1))

        legend_x = margin_x
        legend_y = source_size[1] + args.grid_size / 2
        # Iterate through each color, drawing appropriate box
        for i in range(len(colors)):
            color = colors[i]
            draw.rectangle((legend_x, legend_y, legend_x + args.grid_size, legend_y + args.grid_size), fill=color, outline=BLACK)
            draw.text((legend_x + args.grid_size / 4, legend_y + args.grid_size / 4), str(i + 1), BLACK, font=font)
            legend_x += margin_x + args.grid_size

    out_image.save(args.out_filename)

if __name__ == "__main__":
    main()
