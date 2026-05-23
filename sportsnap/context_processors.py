from datetime import datetime


def site_context(request):
    return {
        'site_name': 'SportSnap',
        'site_tagline': 'Capture Every Winning Moment.',
        'current_year': datetime.now().year,
    }
