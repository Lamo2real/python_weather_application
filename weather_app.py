import sys
from PyQt5.QtWidgets import QApplication
from ui_components import WeatherApp


if __name__ == '__main__':
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_()) #here we exit the window (exec_() handle the events in the window)