from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from sf_auth.models import Profile, ProfilePhoto


class ProfilePhotoModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='password123'
        )
        self.profile = Profile.objects.create(user=self.user)

    def test_profile_photo_creation(self):
        """Тест: создание фото профиля с обязательными полями"""
        mock_image = SimpleUploadedFile(
            name='photo1.jpg',
            content=b'fake image content',
            content_type='image/jpeg'
        )
        photo = ProfilePhoto.objects.create(
            profile=self.profile,
            image=mock_image
        )
        self.assertEqual(photo.profile, self.profile)
        self.assertTrue(photo.image.name.startswith('profile_photos/gallery/photo1'))
        self.assertFalse(photo.is_main)  # по умолчанию False
        self.assertIsNotNone(photo.uploaded_at)

    def test_profile_photo_str_method(self):
        """Тест: метод __str__ возвращает ожидаемую строку"""
        mock_image = SimpleUploadedFile(
            name='test.jpg',
            content=b'fake',
            content_type='image/jpeg'
        )
        photo = ProfilePhoto.objects.create(profile=self.profile, image=mock_image)
        expected = f"Photo for {self.user.username} - {photo.uploaded_at}"
        self.assertEqual(str(photo), expected)

    def test_profile_photo_is_main_default(self):
        """Тест: по умолчанию is_main = False"""
        mock_image = SimpleUploadedFile(name='img.jpg', content=b'x', content_type='image/jpeg')
        photo = ProfilePhoto.objects.create(profile=self.profile, image=mock_image)
        self.assertFalse(photo.is_main)

    def test_profile_photo_can_be_main(self):
        """Тест: можно установить is_main = True"""
        mock_image = SimpleUploadedFile(name='main.jpg', content=b'x', content_type='image/jpeg')
        photo = ProfilePhoto.objects.create(profile=self.profile, image=mock_image, is_main=True)
        self.assertTrue(photo.is_main)

    def test_multiple_photos_for_one_profile(self):
        """Тест: у одного профиля может быть несколько фото"""
        img1 = SimpleUploadedFile(name='p1.jpg', content=b'1', content_type='image/jpeg')
        img2 = SimpleUploadedFile(name='p2.jpg', content=b'2', content_type='image/jpeg')

        photo1 = ProfilePhoto.objects.create(profile=self.profile, image=img1)
        photo2 = ProfilePhoto.objects.create(profile=self.profile, image=img2, is_main=True)

        self.assertEqual(self.profile.photos.count(), 2)
        self.assertIn(photo1, self.profile.photos.all())
        self.assertIn(photo2, self.profile.photos.all())
        self.assertTrue(photo2.is_main)
        self.assertFalse(photo1.is_main)

    def test_photo_ordering(self):
        """Тест: фото сортируются по uploaded_at (Meta.ordering = ['-uploaded_at'])"""
        img1 = SimpleUploadedFile(name='a.jpg', content=b'a', content_type='image/jpeg')
        img2 = SimpleUploadedFile(name='b.jpg', content=b'b', content_type='image/jpeg')

        photo1 = ProfilePhoto.objects.create(profile=self.profile, image=img1)
        photo2 = ProfilePhoto.objects.create(profile=self.profile, image=img2)

        photos = self.profile.photos.all()
        # Последнее загруженное — первое
        self.assertEqual(photos[0], photo2)
        self.assertEqual(photos[1], photo1)