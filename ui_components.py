
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt
from weather_api import get_weather_data
from weather_helpers import get_weather_emoji

class WeatherApp(QWidget):
    """build the blueprint for the weather UI and its methods"""
    
    def __init__(self):
        """construct the objects and methods of the weather applications attributes"""
        
        super().__init__()
        self.city_label = QLabel("Enter City name: ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("get weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.initUI()
    
    
    def initUI(self):
        """allow for dynamic values and UI friendly app"""
        
        self.setWindowTitle("Weather App")
        
        vbox = QVBoxLayout() # allows managing positioning and sizing of the widget and its attributes
        
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        
        self.setLayout(vbox)        

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.temperature_label.setObjectName("temperature_label")
        self.description_label.setObjectName("description_label")
        self.emoji_label.setObjectName("emoji_label")
        self.get_weather_button.setObjectName("get_weather_button")
        
        # CSS Styling
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
        
        # aligning everything in the middle
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)
        
        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        city = self.city_input.text()
        data, error_message = get_weather_data(city)

        if data:
            self.display_weather(data)
        else:
            self.display_error(error_message)

    def display_error(self, message):
        """inform user of the error cause and clear other attributes"""
        
        self.temperature_label.setStyleSheet("font-size: 30px;")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()
    
    def display_weather(self, data):
        """find the data in the api response json and beautify it in the widget"""
        
        temperature_k = data['main']['temp']
        weather_description = data['weather'][0]['description']
        
        temperature_c = temperature_k - 273.15
        weather_id = data['weather'][0]['id']
        
        self.temperature_label.setStyleSheet("font-size: 75px;")
        self.temperature_label.setText(f'{temperature_c:.0f}°C\n')
        self.emoji_label.setText(get_weather_emoji(weather_id))
        self.description_label.setText(f'{weather_description}')
            
            
    

    
        
        