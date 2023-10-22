from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Course
from .forms import CourseForm

class CourseListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'

class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'

class CourseCreateView(CreateView):
    model = Course
    template_name = 'courses/course_create.html'
    form_class = CourseForm
    success_url = reverse_lazy('courses:course_list')

class CourseUpdateView(UpdateView):
    model = Course
    template_name = 'courses/course_update.html'
    form_class = CourseForm
    context_object_name = 'course'
    success_url = reverse_lazy('courses:course_list')

class CourseDeleteView(DeleteView):
    model = Course
    template_name = 'courses/course_delete.html'
    context_object_name = 'course'
    success_url = reverse_lazy('courses:course_list')
