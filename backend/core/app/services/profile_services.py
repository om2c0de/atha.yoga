from PIL import Image
from PIL.ImageDraw import ImageDraw

from core.models import User


def make_square(image: Image) -> Image:
    width, height = image.size
    if height < width:
        square = image.crop(((width - height) // 2, 0, (width - height) // 2 + height, height))
    else:
        square = image.crop((0, 0, width, width))
    return square


def make_circle_mask(radius: int) -> Image:
    mask = Image.new('L', (radius, radius))
    mask_draw = ImageDraw(mask)
    mask_draw.ellipse((0, 0, radius, radius), fill=255)
    return mask


class ProfilePhotoCreator:
    SIZE = 165

    def __init__(self, user: User, data):
        self.data = data
        self.user = user

        path_for_profile_photo = "media/user_profile_foto/" + str(user.email) + ".png"

        profile_photo = self.create_profile_photo_from_file(data.validated_data["profile_photo"])
        profile_photo.save(fp=path_for_profile_photo)
        user.avatar = path_for_profile_photo
        user.save()

    def create_profile_photo_from_file(self, file: Image) -> Image:
        image = Image.open(file)
        width, height = image.size
        if width != height:
            image = make_square(image)
        image.thumbnail(size=(self.SIZE, self.SIZE))
        image.putalpha(make_circle_mask(self.SIZE))
        return image
