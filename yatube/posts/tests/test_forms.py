from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Group, Post, User
from posts.forms import PostForm


class PostCreateForm(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = PostForm()

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.user = User.objects.create_user(username='author')
        self.authorized_client.force_login(self.user)

    def test_create_post(self):
        self.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        self.post = Post.objects.create(
            text='Текст поста',
            author=self.user,
            group=self.group,
        )
        posts_count = Post.objects.count()
        form_data = {
            'group': 'Тестовая группа',
            'text': PostCreateForm.post.text,
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(
            response,
            reverse('posts:profile', kwargs={'username': self.user.username}))

        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(
            Post.objects.filter(
                text=PostCreateForm.post.text,
                group='Тестовая группа',
            ).exists()
        )

    def test_cant_create_existing_slug(self):
        post_count = Post.objects.count()
        form_data = {
            'title': 'Тестовая группа',
            'description': 'Тестовое описание',
            'slug': 'test-slug'
        }
        response = self.guest_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertEqual(Post.objects.count(), post_count)
        self.assertEqual(response.status_code, 200)
