from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Group, Post, User


class PostCreateForm(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='author')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post(self):
        posts_count = Post.objects.count()
        form_data = {
            'group': PostCreateForm.group.id,
            'text': 'Новый пост',
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
        new_post = Post.objects.first()

        self.assertEqual(new_post.author.username, self.user.username)
        self.assertEqual(new_post.group.id, form_data['group'])
        self.assertEqual(new_post.text, form_data['text'])


class PostUpdateForm(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='author')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',

        )
        cls.post = Post.objects.create(
            text='Новый пост',
            author=cls.user,
            group=cls.group,
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_update_form(self):
        posts_count = Post.objects.count()
        form_data = {
            'group': PostCreateForm.group.id,
            'text': 'Обновленный текст',
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}),
            data=form_data,
            follow=True
        )
        self.assertRedirects(
            response,
            reverse('posts:post_detail',
                    kwargs={'post_id': self.post.id}))
        self.assertEqual(Post.objects.count(), posts_count)
        new_post = Post.objects.first()

        self.assertEqual(new_post.author.username, self.user.username)
        self.assertEqual(new_post.group.id, form_data['group'])
        self.assertEqual(new_post.text, form_data['text'])
