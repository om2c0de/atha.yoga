from PIL import Image, ImageDraw

SIZE = 165


def create_profile_photo_from_file(file) -> Image:
    with Image.open(file) as image:
        image.load()
    width, height = image.size
    if width != height:
        image = make_square(image)
    image.thumbnail(size=(SIZE, SIZE))
    image.putalpha(make_circle_mask(SIZE))
    return image


def make_square(image: Image) -> Image:
    width, height = image.size
    if height < width:
        square = image.crop(((width - height) // 2, 0, (width - height) // 2 + height, height))
    else:
        square = image.crop((0, 0, width, width))
    return square


def make_circle_mask(radius: int) -> Image:
    mask = Image.new('L', (radius, radius))
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, radius, radius), fill=255)
    return mask
