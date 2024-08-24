from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import QUiLoader
import sys
# 在 QApplication 之前先实例化
uiLoader = QUiLoader()

class Main_Stats:
    def __init__(self):
        self.ui = uiLoader.load('ui/homePage.ui')


