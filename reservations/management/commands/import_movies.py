import requests
from django.core.management.base import BaseCommand
from reservations.models import Movie
import os
from dotenv import load_dotenv

load_dotenv()  

class Command(BaseCommand):
    help = 'Import movies from The Movie Database API'

    def handle(self, *args, **kwargs):

        api_key = os.getenv('TMDB_API_KEY')
        url = f'https://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc&api_key={api_key}'
        
        try:
            response = requests.get(url)
            response.raise_for_status() 
            
            data = response.json()
            
            # check errors in response
            if 'errors' in data:
                self.stdout.write(self.style.ERROR(f"API Error: {data['errors']}"))
                return
            
            # process the data if no errors occurred
            for item in data.get('results', []):
                Movie.objects.update_or_create(
                    title=item['title'],
                    defaults={
                        'description': item.get('overview', 'No description available'),
                        'poster_image': f"https://image.tmdb.org/t/p/w1280{item.get('poster_path', '')}",
                    }
                )
            
            self.stdout.write(self.style.SUCCESS('Successfully imported movies'))
        
        except requests.RequestException as e:
            self.stdout.write(self.style.ERROR(f"Request failed: {e}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {e}"))
