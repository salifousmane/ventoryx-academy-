from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from .models import Parcours, Course, Test

@require_http_methods(["GET"])
def parcours_list(request):
    """List all available courses"""
    parcours = Parcours.objects.all()
    return render(request, 'parcours/selection_metier.html', {'parcours': parcours})

@require_http_methods(["GET"])
def course_detail(request, course_id):
    """View course details"""
    course = Course.objects.get(id=course_id)
    return render(request, 'parcours/cours.html', {'course': course})

@require_http_methods(["GET"])
def test_detail(request, test_id):
    """View test"""
    test = Test.objects.get(id=test_id)
    return render(request, 'parcours/test.html', {'test': test})