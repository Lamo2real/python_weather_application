import requests
import os
from dotenv import load_dotenv


BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

def get_weather_data(city):
    """fetch data from API source and manage data with error handling and control with exceptions"""
    load_dotenv(dotenv_path='../.env')
    api_key = os.getenv('API_KEY')
    url = f"{BASE_URL}?q={city}&appid={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data['cod'] == 200:
            return data, None
        else:
            return None, "City not found. Please try again."
    
    except requests.exceptions.HTTPError as http_error:
        match response.status_code:
            case 400:
                return None, 'Bad request:\n Please check your prompt'
            case 401:
                return None, 'Unauthorized:\n Invalid API Key'
            case 403:
                return None, 'Forbidden:\n Access is denied'
            case 404:
                return None, 'Not Found:\n City not found'
            case 500:
                return None, 'Internal Server Issues:\n Please try again later'
            case 502:
                return None, 'Bad gateway:\n Invalid response from the server'
            case 503:
                return None, 'Service Unavailable:\n Server is down'
            case 504:
                return None, 'Gateway Timeout:\n No response from the server'
            case _:
                return None, f'HTTP error occurred:\n {http_error} '
          
    except requests.exceptions.ConnectionError: # Raised when there are connection issues
        return None, 'Connection Error:\n Check your internet connection'
    
    except requests.exceptions.Timeout: # Raised when the request times out
        return None, 'Timeout Error:\n The request timed out'
    
    except requests.exceptions.TooManyRedirects: # Raised when the URL keeps redirecting indefinitely
        return None, 'Too many Redirects\n Check the URL' 
    
    except requests.exceptions.RequestException as req_error:  # Catch-all exception for other errors in requests
        return None, f'Request Error\n{req_error} '
