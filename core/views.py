"""
Core views for legal pages and general site information.
"""
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response


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
