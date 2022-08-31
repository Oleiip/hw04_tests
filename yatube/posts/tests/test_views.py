from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django import forms
from ..models import Post, Group

User = get_user_model()


class TaskPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user1 = User.objects.create_user(username='oleiip')
        cls.user2 = User.objects.create_user(username='fany')
        cls.group = Group.objects.create(
            title='someee',
            slug='some_people',
            description='everyyy some day'
        )

        cls.post1 = Post.objects.create(
            author=cls.user1,
            text='Тестовый текст',
            group=cls.group
        )

        for post in range(12):
            Post.objects.create(author=cls.user1,
                                text='Тестовый текст',
                                group=cls.group)

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user1)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list',
                    kwargs={'slug': self.group.slug}
                    ): 'posts/group_list.html',
            reverse('posts:profile',
                    kwargs={'username': self.user1.username}
                    ): 'posts/profile.html',
            reverse('posts:post_detail',
                    kwargs={'post_id': self.post1.id}
                    ): 'posts/post_detail.html',
            reverse('posts:post_edit',
                    kwargs={'post_id': self.post1.id}
                    ): 'posts/create_post.html',
            reverse('posts:post_create'): 'posts/create_post.html',
        }

        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:index'))
        first_object = response.context['page_obj'][0]
        task_author_0 = first_object.author.username
        task_text_0 = first_object.text
        task_group_0 = first_object.group.title
        self.assertEqual(task_author_0, self.user1.username)
        self.assertEqual(task_text_0, self.post1.text)
        self.assertEqual(task_group_0, self.group.title)

    def test_group_list_page_show_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:group_list',
                    kwargs={'slug': self.group.slug}
                    ))
        first_object = response.context['page_obj'][0]
        task_id_0 = first_object.group.id
        task_title_0 = first_object.group.title
        task_slug_0 = first_object.group.slug
        self.assertEqual(task_id_0, self.group.id)
        self.assertEqual(task_title_0, self.group.title)
        self.assertEqual(task_slug_0, self.group.slug)

    def test_profile_page_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:profile',
                    kwargs={'username': self.user1.username}
                    ))
        first_object = response.context['page_obj'][0]
        task_id_0 = first_object.author.id
        task_username_0 = first_object.author.username
        self.assertEqual(task_id_0, self.user1.id)
        self.assertEqual(task_username_0, self.user1.username)

    def test_post_detail_page_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:post_detail',
                    kwargs={'post_id': self.post1.id}
                    ))
        first_object = response.context['post']
        task_id_0 = first_object.id
        self.assertEqual(task_id_0, self.post1.id)

    def test_post_edit_page_show_correct_context(self):
        """Шаблон post_edit сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:post_edit',
                    kwargs={'post_id': self.post1.id}
                    ))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_post_create_page_show_correct_context(self):
        """Шаблон post_create сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:post_create'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_first_page_contains_ten_records(self):
        list_views = [
            reverse('posts:index'),
            reverse('posts:group_list',
                    kwargs={'slug': self.group.slug}),
            reverse('posts:profile',
                    kwargs={'username': self.user1.username})]

        for reverse_name in list_views:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_page_contains_three_records(self):
        list_views = [
            reverse('posts:index'),
            reverse('posts:group_list',
                    kwargs={'slug': self.group.slug}),
            reverse('posts:profile',
                    kwargs={'username': self.user1.username})]
        for reverse_name in list_views:
            with self.subTest(reverse_name=reverse_name):
                response = self.client.get(reverse_name + '?page=2')
                self.assertEqual(len(response.context['page_obj']), 3)
