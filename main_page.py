from PySide6.QtWidgets import QApplication,QStackedWidget, QFileDialog, QDialog, QVBoxLayout, QListWidget, QLineEdit, QPushButton,QHBoxLayout
from PySide6.QtUiTools import QUiLoader
# import pandas as pd
import shutil
import os


# 在 QApplication 之前先实例化
uiLoader = QUiLoader()

class Main_Stats:
    def __init__(self):
        # main_page加载界面
        self.ui = uiLoader.load('ui/homePage.ui')
        self.ui.upload_btn.clicked.connect(self.upload_word)
        self.ui.sys_btn.clicked.connect(self.sys_word_stock)
        # self.ui.review_btn.clicked.connect(self.review_word)
        # self.ui.word_print.clicked.connect(self.prt_word)
        # self.ui.word_btn.clicked.connect(self.word_btn)
        # self.ui.gram_btn.clicked.connect(self.gram_btn)
        # self.ui.reading_btn.clicked.connect(self.reading_btn)
        # self.ui.my_btn.clicked.connect(self.my_btn)






    # main_page
    def upload_word(self):
        file_path, _ = QFileDialog.getOpenFileName(self.ui, "选择文件", "", "Excel 文件 (*.xlsx);;CSV 文件 (*.csv);;文本文件 (*.txt)")
        print(file_path)
        destination_path = "system_word_stock/"  # 替换为您实际的系统词库目录
        try:
            shutil.copy(file_path, destination_path)
        except :
            pass

    def sys_word_stock(self):
        directory = "system_word_stock/"  # 替换为您实际的系统词库目录
        file_list = os.listdir(directory)

        dialog = QDialog(self.ui)
        layout = QVBoxLayout(dialog)

        search_layout = QHBoxLayout()
        search_line_edit = QLineEdit(dialog)
        search_button = QPushButton("搜索", dialog)
        search_layout.addWidget(search_line_edit)
        search_layout.addWidget(search_button)

        list_widget = QListWidget(dialog)

        for file_name in file_list:
            list_widget.addItem(file_name)

        layout.addLayout(search_layout)
        layout.addWidget(list_widget)

        search_button.clicked.connect(lambda: self.search_files(search_line_edit.text(), list_widget,"system_word_stock/"))

        dialog.setWindowTitle("选择词库")
        dialog.setFixedSize(435, 640)  # 设置与前文所提供的 UI 界面大小一致
        dialog.exec_()

    def search_files(self, keyword, list_widget,path):
        filtered_list = [file_name for file_name in os.listdir(f"{path}") if keyword.lower() in file_name.lower()]
        list_widget.clear()
        for file_name in filtered_list:
            list_widget.addItem(file_name)

# app = QApplication(sys.argv)
# stats = Main_Stats()
# stats.stack_widget.show()
# app.exec()