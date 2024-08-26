from PySide6.QtWidgets import QApplication, QStackedWidget, QMessageBox,QLineEdit,QDialog,QHBoxLayout,QVBoxLayout,QPushButton,QListWidget,QTextBrowser
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QRegularExpressionValidator,QFont
from PySide6.QtCore import QRegularExpression
import sys,os,shutil
import main_page

# 在 QApplication 之前先实例化
uiLoader = QUiLoader()

class Stats:
    def __init__(self):
        self.deleted_user_path = None
        # 加载登录界面
        self.login_page = uiLoader.load('ui/login.ui')
        # 注册按钮
        self.login_page.register_2.clicked.connect(self.register_2)
        # 登录按钮
        self.login_page.login_btn.clicked.connect(self.login_btn)
        self.login_page.Lpassword.returnPressed.connect(self.login_btn)
        # 忘记密码
        self.login_page.forggetpwd.clicked.connect(self.forggetpwd)
        # 所有用户
        self.login_page.all_user.clicked.connect(self.all_user)
        # 联系作者
        self.login_page.connectAuthor.clicked.connect(self.connectAuthor)

        # 加载注册界面
        self.register_page = uiLoader.load('ui/register.ui')
        self.register_page.returnMainPage.clicked.connect(self.returnMainPage)
        self.register_page.phoneNum_Edit.returnPressed.connect(self.FinishBtn)
        self.register_page.FinishBtn.clicked.connect(self.FinishBtn)

        # 输入格式限制
        self.regex = QRegularExpression("^1[3-9]\d{9}$")
        validator = QRegularExpressionValidator(self.regex, self.register_page.phoneNum_Edit)
        self.register_page.phoneNum_Edit.setValidator(validator)

        # 创建一个栈式布局容器
        self.stack_widget = QStackedWidget()
        self.stack_widget.resize(435, 640)
        self.stack_widget.addWidget(self.login_page)
        self.stack_widget.setWindowTitle(self.login_page.windowTitle())
        
        # 实例化main_page中的Main_Stats类
        self.Main_stats = main_page.Main_Stats()
        # 返回主页
        self.Main_stats.ui.quit_btn.clicked.connect(self.returnMainPage)
        self.Main_stats.ui.back_btn.clicked.connect(self.returnMainPage2)

    ### 登录页相关方法
    def all_user(self):
        stu_list = os.listdir("student_Info")
        dialog = QDialog(self.login_page)
        layout = QVBoxLayout(dialog)
        search_layout = QHBoxLayout()
        search_line_edit = QLineEdit(dialog)
        refresh_button = QPushButton("刷新", dialog)
        search_line_edit.setPlaceholderText("请搜索...")
        modify_button = QPushButton("修改", dialog)
        delete_button = QPushButton("删除", dialog)

        search_layout.addWidget(refresh_button)
        search_layout.addWidget(search_line_edit)
        search_layout.addWidget(modify_button)
        search_layout.addWidget(delete_button)
        
        list_widget = QListWidget(dialog)
        font = list_widget.font()
        font.setPointSize(14)
        list_widget.setFont(font)
        for stu_name in stu_list:
            list_widget.addItem(stu_name)
        layout.addLayout(search_layout)
        layout.addWidget(list_widget)
        search_line_edit.textChanged.connect(lambda: self.Main_stats.search_files(search_line_edit.text(), list_widget,"student_Info"))
        
        def handle_item_click(item):
            self.deleted_user_path = item.text()
        list_widget.itemClicked.connect(handle_item_click)
        def delete_user():
            reply = QMessageBox.question(self.register_page, "确认删除", f"确定要删除学员 {self.deleted_user_path} ？", QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                try:
                    shutil.rmtree(f"student_Info/{self.deleted_user_path}")
                    # 重新获取学生列表并更新列表框
                    new_stu_list = os.listdir("student_Info")
                    list_widget.clear()
                    for stu_name in new_stu_list:
                        list_widget.addItem(stu_name)
                except:
                    QMessageBox.warning(self.register_page, "提示", f"请选择学员！")
            else:
                pass
        delete_button.clicked.connect(delete_user)

        def modify_info():
            try:
                file_path = os.getcwd()
                os.startfile(f"{file_path}\\student_Info\\{self.deleted_user_path}\\{self.deleted_user_path}.txt")
            except:
                QMessageBox.warning(self.register_page, "提示", f"请选择学员！")
        modify_button.clicked.connect(modify_info)
        def refresh():
            try:    
                file_path = os.getcwd()
                with open(f"{file_path}\\student_Info\\{self.deleted_user_path}\\{self.deleted_user_path}.txt",'r',encoding='utf-8') as f:
                    new_name=f.readline().split(',')[1].strip()
                os.rename(f"{file_path}\\student_Info\\{self.deleted_user_path}\\{self.deleted_user_path}.txt",f"{file_path}\\student_Info\\{self.deleted_user_path}\\{new_name}.txt")
                os.rename(f"{file_path}\\student_Info\\{self.deleted_user_path}",f"{file_path}\\student_Info\\{new_name}")
                self.deleted_user_path = new_name
                new_stu_list = os.listdir("student_Info")
                list_widget.clear()
                for stu_name in new_stu_list:
                    list_widget.addItem(stu_name)
            except:
                self.deleted_user_path= None

        refresh_button.clicked.connect(refresh)

        dialog.setWindowTitle("所有学员")
        dialog.setFixedSize(435, 640)
        dialog.exec()

       
    # 联系作者
    def connectAuthor(self):
        dialog = QDialog()
        dialog.setWindowTitle("联系方式")
        layout = QVBoxLayout()
        text_browser = QTextBrowser()
        font = QFont()
        font.setPointSize(14)
        text_browser.setFont(font)
        text_browser.setHtml(f"QQ：916994565<br>VX：SHEN_2199")

        text_browser.setFixedWidth(200)  # 设置宽度
        text_browser.setFixedHeight(60)  # 设置高度

        layout.addWidget(text_browser)
        dialog.setLayout(layout)
        dialog.exec()

    # 忘记密码
    def forggetpwd(self):
        user_name=self.login_page.Lusername.text()
        try:
            with open(f"student_Info/{user_name}/{user_name}.txt",'r',encoding='utf-8') as f:
                pwd = f.readlines()[1].split(',')[1]
                QMessageBox.warning(self.register_page, "提示", f"{user_name}的密码:{pwd}")
        except:
            all_Info = os.listdir('student_Info')
            if user_name not in all_Info and user_name:
                QMessageBox.warning(self.register_page, "警告", "用户不存在，请注册！")
            else:
                QMessageBox.warning(self.register_page, "警告", "请输入用户名！")
            

    def login_btn(self):
        user_name=self.login_page.Lusername.text()
        pwd = self.login_page.Lpassword.text()
        # 所有用户信息
        all_Info = os.listdir("student_Info")
        if user_name in all_Info:
            with open(f"student_Info/{user_name}/{user_name}.txt",'r',encoding='utf-8') as f:
                ppwd = f.readlines()[1].split(",")[1].strip()
                if ppwd == pwd:
                    self.stack_widget.addWidget(self.Main_stats.ui)
                    self.stack_widget.setWindowTitle(self.Main_stats.ui.windowTitle())
                    self.stack_widget.setCurrentWidget(self.Main_stats.ui)
                    self.Main_stats.ui.welcome_label.setText(f"欢迎您，{user_name}!")
                else:
                    QMessageBox.warning(self.register_page, "提示", "密码错误！")
        else:
            QMessageBox.warning(self.register_page, "提示", "用户不存在！")

    def register_2(self):
        # 将注册页面添加到栈式布局容器中
        self.stack_widget.addWidget(self.register_page)
        # 切换到注册页面
        self.stack_widget.setCurrentWidget(self.register_page)
        # 隐藏登录页面的内容
        self.login_page.setEnabled(False)
        # 设置窗口标题为注册页面的标题
        self.stack_widget.setWindowTitle(self.register_page.windowTitle())

    ### 注册页相关方法
    def FinishBtn(self):
        name_text = self.register_page.name_Edit.text()
        user_pwd = self.register_page.newPwd_Edit.text()
        re_pwd = self.register_page.rePwd_Edit.text()
        stu_grade = self.register_page.grade_Edit.text()
        school_name = self.register_page.school_Edit.text()
        phone_num = self.register_page.phoneNum_Edit.text()
        match = self.regex.match(phone_num)
        all_Info = os.listdir("student_Info")
        if user_pwd:
            if name_text not in all_Info:
                if user_pwd==re_pwd:
                    if  match.hasMatch():
                        os.mkdir(f"student_Info/{name_text}")
                        with open(f"student_Info/{name_text}/{name_text}.txt","w+",encoding='utf-8') as f:
                                f.write(f"姓名,{name_text}\n")
                                f.write(f"密码,{user_pwd}\n")
                                if stu_grade:
                                    f.write(f"年级,{stu_grade}\n")
                                else:
                                    f.write(f"年级,未知\n")
                                if school_name:
                                    f.write(f"学校,{school_name}\n")
                                else:
                                    f.write(f"学校,未知\n")
                                f.write(f"电话,{phone_num}\n")
                                QMessageBox.warning(self.register_page, "提示", "注册完成！")
                                self.clear_page()
                                self.returnMainPage()
                    else:
                        QMessageBox.warning(self.register_page, "错误提示", "请输入正确手机号码！")
                else:
                    QMessageBox.warning(self.register_page, "警告", "请确认密码！")
            else:
                QMessageBox.warning(self.register_page, "警告", "用户已存在！")
        else:
            QMessageBox.warning(self.register_page, "警告", "密码不能为空！")

    def returnMainPage(self):
        self.clear_page()
        self.stack_widget.setCurrentWidget(self.login_page)
        self.login_page.setEnabled(True)
        self.stack_widget.setWindowTitle(self.login_page.windowTitle())
    def returnMainPage2(self):
        self.stack_widget.setCurrentWidget(self.login_page)
        self.login_page.setEnabled(True)
        self.stack_widget.setWindowTitle(self.login_page.windowTitle())
    # 清除文本
    def clear_page(self):
        # 获取注册页面上的所有 QLineEdit
        widgets1 = self.register_page.findChildren(QLineEdit)
        for widget in widgets1:
            widget.clear()

        widgets2 = self.login_page.findChildren(QLineEdit)
        for widget in widgets2:
            widget.clear()

app = QApplication(sys.argv)
stats = Stats()
stats.stack_widget.show()
app.exec()
