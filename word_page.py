from PySide6.QtWidgets import QApplication, QDateTimeEdit
from PySide6.QtUiTools import QUiLoader
from datetime import datetime

# 在QApplication之前先实例化
uiLoader = QUiLoader()

class WORD_PAGE:
    def __init__(self):       
        # 再加载界面
        self.word_page = uiLoader.load('ui/word_page.ui')
        self.current_datetime = datetime.now()
        # 设置时间到 QDateTimeEdit 部件
        self.word_page.DATE_TIME.setDateTime(self.current_datetime)
        # 禁止用户调整时间
        self.word_page.DATE_TIME.setReadOnly(True)

    # 其它代码 ...

# app = QApplication([])
# stats = WORD_PAGE()
# stats.word_page.show()
# app.exec() 