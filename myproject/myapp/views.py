import requests
from django.shortcuts import render
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

def home(request):
    cache_key = 'random_dog_image'
    data = cache.get(cache_key)

    if not data:
        url = 'https://dog.ceo/api/breeds/image/random'

        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            cache.set(cache_key, data, timeout=300)  # Cache for 5 minutes

        except requests.exceptions.HTTPError as http_err:
            logger.error(f'HTTP error occurred: {http_err}')
            return render(request, 'error.html', {
                'error_message': 'HTTP error occurred.',
                'status_code': response.status_code if response else 500
            }, status=response.status_code if response else 500)

        except requests.exceptions.RequestException as req_err:
            logger.error(f'Request error occurred: {req_err}')
            return render(request, 'error.html', {
                'error_message': 'An error occurred during the request.'
            }, status=500)

        except Exception as e:
            logger.exception('An unexpected error occurred.')
            return render(request, 'error.html', {
                'error_message': 'An unexpected error occurred.'
            }, status=500)

    return render(request, 'home.html', {'image_url': data.get('message')})
