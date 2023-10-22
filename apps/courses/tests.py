from django.test import TestCase
from django.urls import reverse
from .models import Course
from .forms import CourseForm

class CourseModelTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            name='Test Course',
            location='Test Location',
            par=72
        )

    def test_course_creation(self):
        self.assertEqual(self.course.name, 'Test Course')
        self.assertEqual(self.course.location, 'Test Location')
        self.assertEqual(self.course.par, 72)

class CourseViewsTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            name='Test Course',
            location='Test Location',
            par=72
        )

    def test_course_list_view(self):
        url = reverse('courses:course_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/course_list.html')

    def test_course_detail_view(self):
        url = reverse('courses:course_detail', args=[self.course.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/course_detail.html')

    # Add more tests for create, update, and delete views

class CourseFormTest(TestCase):
    def test_course_form_valid_data(self):
        form = CourseForm(data={
            'name': 'Test Course',
            'location': 'Test Location',
            'par': 72
        })
        self.assertTrue(form.is_valid())

    def test_course_form_invalid_data(self):
        form = CourseForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)

        form = CourseForm(data={'name': 'Test Course'})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)

        form = CourseForm(data={'name': 'Test Course', 'location': 'Test Location'})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
