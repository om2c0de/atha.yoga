from PIL import Image
from PIL.ImageDraw import ImageDraw

from core.models import User


class ProfilePhotoCreator:
    SIZE = 165

    def __init__(self, user: User, data):
        self.data = data
        self.user = user

    def create(self):
        path_for_profile_photo = "media/user_profile_foto/" + str(self.user.email) + ".png"

        profile_photo = self._create_profile_photo_from_file(self.data.validated_data["profile_photo"])
        profile_photo.save(fp=path_for_profile_photo)
        self.user.avatar = path_for_profile_photo
        self.user.save()

    def _create_profile_photo_from_file(self, file: Image) -> Image:
        image = Image.open(file)
        width, height = image.size
        if width != height:
            image = ProfilePhotoCreator._make_square(image)
        image.thumbnail(size=(self.SIZE, self.SIZE))
        image.putalpha(ProfilePhotoCreator._make_circle_mask(self.SIZE))
        return image

    @staticmethod
    def _make_square(image: Image) -> Image:
        width, height = image.size
        if height < width:
            square = image.crop(((width - height) // 2, 0, (width - height) // 2 + height, height))
        else:
            square = image.crop((0, 0, width, width))
        return square

    @staticmethod
    def _make_circle_mask(radius: int) -> Image:
        mask = Image.new('L', (radius, radius))
        mask_draw = ImageDraw(mask)
        mask_draw.ellipse((0, 0, radius, radius), fill=255)
        return mask
