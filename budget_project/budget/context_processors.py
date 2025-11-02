from datetime import datetime


def current_year(request):
    return {
        'year': str(datetime.now().year).replace(' ', '')
    }
