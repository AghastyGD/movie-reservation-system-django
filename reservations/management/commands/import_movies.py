import requests
from django.core.management.base import BaseCommand
from reservations.models import Movie, Genre
import os
from dotenv import load_dotenv

class Command(BaseCommand):
    help = 'Import genres and movies from The Movie Database API'

    def handle(self, *args, **kwargs):
        load_dotenv()  
        api_key = os.getenv('TMDB_API_KEY')

        genre_url = f'https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}&language=en-US'
        self.import_genres(genre_url)

        movie_url = f'https://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc&api_key={api_key}&language=en-US'
        self.import_movies(movie_url)

    def import_genres(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()  
            
            data = response.json()
            
            if 'errors' in data:
                self.stdout.write(self.style.ERROR(f"API Error: {data['errors']}"))
                return
            
            for genre in data.get('genres', []):
                Genre.objects.update_or_create(
                    tmdb_id=genre['id'],
                    defaults={'name': genre['name']}
                )
            
            self.stdout.write(self.style.SUCCESS('Successfully imported genres'))
        
        except requests.RequestException as e:
            self.stdout.write(self.style.ERROR(f"Request failed: {e}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {e}"))

    def import_movies(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status() 
            
            data = response.json()
            
            # check errors in response
            if 'errors' in data:
                self.stdout.write(self.style.ERROR(f"API Error: {data['errors']}"))
                return
            
            # process data if no errors ocurred
            for item in data.get('results', []):
                movie, created = Movie.objects.update_or_create(
                    title=item['title'],
                    defaults={
                        'description': item.get('overview', 'No description available'),
                        'poster_image': f"https://image.tmdb.org/t/p/w1280{item.get('poster_path', '')}",
                    }
                )
                
                genre_ids = item.get('genre_ids', [])
                genres = Genre.objects.filter(tmdb_id__in=genre_ids)
                movie.genre.set(genres)
            
            self.stdout.write(self.style.SUCCESS('Successfully imported movies'))
        
        except requests.RequestException as e:
            self.stdout.write(self.style.ERROR(f"Request failed: {e}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {e}"))
