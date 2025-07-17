"""
Core views for legal pages and general site information.
"""
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def api_root(request):
    """
    API root endpoint showing available endpoints
    """
    return Response({
        'message': 'Welcome to Videoflix API',
        'version': '1.0.0',
        'endpoints': {
            'authentication': {
                'register': '/api/register/',
                'login': '/api/login/',
                'logout': '/api/logout/',
                'profile': '/api/profile/',
                'verify_email': '/api/verify-email/{token}/',
                'password_reset': '/api/password_reset/',
                'password_confirm': '/api/password_confirm/{token}/'
            },
            'videos': {
                'list': '/api/videos/',
                'detail': '/api/videos/{id}/',
                'stream': '/api/videos/{id}/stream/{quality}/',
                'qualities': '/api/videos/{id}/qualities/',
                'progress': '/api/videos/{id}/progress/',
                'genres': '/api/videos/genres/',
                'featured': '/api/videos/featured/',
                'by_genre': '/api/videos/by-genre/',
                'continue_watching': '/api/videos/continue-watching/'
            },
            'health': '/api/health/'
        }
    })


def impressum(request):
    """Legal notice / Impressum page."""
    context = {
        'title': 'Impressum',
        'content': {
            'company': 'Videoflix GmbH',
            'address': 'Beispielstraße 123',
            'city': '12345 Musterstadt',
            'country': 'Deutschland',
            'phone': '+49 123 456789',
            'email': 'kontakt@videoflix.de',
            'managing_director': 'Max Mustermann',
            'register_court': 'Amtsgericht Musterstadt',
            'register_number': 'HRB 12345',
            'vat_id': 'DE123456789'
        }
    }
    return render(request, 'core/impressum.html', context)


def datenschutz(request):
    """Privacy policy / Datenschutz page."""
    context = {
        'title': 'Datenschutzerklärung',
        'last_updated': '01.01.2024'
    }
    return render(request, 'core/datenschutz.html', context)


@api_view(['GET'])
def health_check(request):
    """Health check endpoint for monitoring."""
    return Response({
        'status': 'healthy',
        'service': 'videoflix-backend',
        'version': '1.0.0'
    })


@api_view(['GET'])
def api_info(request):
    """API information endpoint."""
    return Response({
        'name': 'Videoflix API',
        'version': '1.0.0',
        'description': 'REST API for Videoflix video streaming platform',
        'endpoints': {
            'authentication': '/api/auth/',
            'videos': '/api/videos/',
            'health': '/api/health/',
            'admin': '/admin/'
        }
    })


def test_thumbnails(request):
    """View to display all videos and their thumbnails."""
    from videos.models import Video
    videos = Video.objects.all()
    return render(request, 'core/test_thumbnails.html', {'videos': videos})
