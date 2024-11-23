import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter City name: ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("get weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Weather App")
        
        vbox = QVBoxLayout()
        
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        
        self.setLayout(vbox)        
        
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        
        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.temperature_label.setObjectName("temperature_label")
        self.description_label.setObjectName("description_label")
        self.emoji_label.setObjectName("emoji_label")
        self.get_weather_button.setObjectName("get_weather_button")
        
        self.setStyleSheet("""
            QLabel, QPushButton{
                font-family: calibri;
            }  
            QLabel#city_label{
                font-size: 40px;
                font-style: italic;
            }              
            QLineEdit#city_input{
                font-size: 40px;
            }
            QPushButton#get_weather_button{
                font-size: 30px;
                font-weight: bold;
            }
            QLabel#temperature_label{
                font-size: 75px
            }
            QLabel#emoji_label{
                font-size: 90px;
                font-family: segoe UI emoji;
            }
            QLabel#description_label{
                font-size: 50px;
            }
        """)
        
        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        api_key = '590e5dd1cc0f1482366ead84de2e6d22'
        city = self.city_input.text()
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
        
        
        
        try: 
            response = requests.get(url)
            response.raise_for_status() #this method will raise an exception if there are any http errors
            data = response.json()
            
            if data['cod'] == 200:
                self.display_weather(data)
            
        except requests.exceptions.HTTPError as http_error: #if statue code is between 400 and 500
            match response.status_code:
                case 400:
                    self.display_error('Bad request:\n please check your prompt')
                case 401:
                    self.display_error('Unauthorized:\n invalid API Key')
                case 403:
                    self.display_error('Forbidden:\n Access is denied')
                case 404:
                    self.display_error('Not Found:\n City not found')
                case 500:
                    self.display_error('Internal Server Issues:\n please try again later')
                case 502:
                    self.display_error('bad gateway:\n Invalid response from the server')
                case 503:
                    self.display_error('Service Unavailable:\n Server is down')
                case 504:
                    self.display_error('Gateway Timeout:\n no response from the server')
                case _: #unexpeted error
                    self.display_error(f'HTTP error occured:\n {http_error} ')
          
        except requests.exceptions.ConnectionError: #if any connection errors eccours
            print('Connection Error:\ncheck your internet connection')
        except requests.exceptions.Timeout: # such as if any time loading the get request is too long
            print('Timeout Error:\nThe request timed out')
        except requests.exceptions.TooManyRedirects: 
            print('Too many Redirects\nCheck the URL')
        except requests.exceptions.RequestException as req_error: # if there are any network issues this excxeption will be raised
            print(f'Request Error\n{req_error} ')
            
            
            
    def display_error(self, message):
        self.temperature_label.setStyleSheet("font-size: 30px;")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()
    
    def display_weather(self, data):
        temperature_k = data['main']['temp']
        weather_description = data['weather'][0]['description']
        
        temperature_c = temperature_k - 273.15
        # temperature_f = (temperature_k * 9/5) - 459.67
        
        weather_id = data['weather'][0]['id']
        
        self.temperature_label.setStyleSheet("font-size: 75px;")
        self.temperature_label.setText(f'{temperature_c:.0f}°C\n')
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(f'{weather_description}')

    @staticmethod
    def get_weather_emoji(weather_id):
        if 200 <= weather_id <= 232:
            return '⛈️'
        elif 300 <= weather_id <= 321:
            return '☁️'
        elif 500 <= weather_id <= 531:
            return '☔'
        elif 600 <= weather_id <= 622:
            return '❄️'
        elif 701 <= weather_id <= 741:
            return '🌫️'
        elif weather_id == 762:
            return '🌋'
        elif weather_id == 771:
            return '💨'
        elif weather_id == 781:
            return '🌪️'
        elif weather_id == 800:
            return '☀️'
        elif 801 <= weather_id <= 804:
            return '🌥️'
        else: 
            return ''
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_()) #here we exit the window (exec_() handle the events in the window)