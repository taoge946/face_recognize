# from PySide2.QtWidgets import QApplication,QMainWindow,QPushButton,QPlainTextEdit,QMessageBox
# def text():
#     info=textEdit.toPlainText()
#     QMessageBox.about(window,'题目',info)

# app=QApplication([])
# window=QMainWindow()
# window.resize(500,400)#resize就是决定大小
# window.move(300,310)#窗口出现在显示器屏幕的什么位置（以显示器左上角为原点(x,y)),不设置就默认在中间
# window.setWindowTitle('测试')

# textEdit=QPlainTextEdit(window)
# textEdit.setPlaceholderText('请输入')#提示文本
# textEdit.move(10,25)
# textEdit.resize(300,350)

# button=QPushButton('点我试试~',window)
# button.move(350,100)
# button.clicked.connect(text)  #按钮被点击后的事件，跳转到指定函数

# window.show()#通过最上层的控件呈现出来
# app.exec_()#进入了事件处理循环，没有这个的话窗口就一闪而过了
from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton,  QPlainTextEdit,QMessageBox

class Stats():
    def __init__(self):
        self.window = QMainWindow()
        self.window.resize(500, 400)
        self.window.move(300, 300)
        self.window.setWindowTitle('薪资统计')

        self.textEdit = QPlainTextEdit(self.window)
        self.textEdit.setPlaceholderText("请输入薪资表")
        self.textEdit.move(10, 25)
        self.textEdit.resize(300, 350)

        self.button = QPushButton('统计', self.window)
        self.button.move(380, 80)

        self.button.clicked.connect(self.handleCalc)


    def handleCalc(self):
        info = self.textEdit.toPlainText()

        # 薪资20000 以上 和 以下 的人员名单
        salary_above_20k = ''
        salary_below_20k = ''
        for line in info.splitlines():
            if not line.strip():
                continue
            parts = line.split(' ')
            # 去掉列表中的空字符串内容
            parts = [p for p in parts if p]
            name,salary,age = parts
            if int(salary) >= 20000:
                salary_above_20k += name + '\n'
            else:
                salary_below_20k += name + '\n'

        QMessageBox.about(self.window,
                    '统计结果',
                    f'''薪资20000 以上的有：\n{salary_above_20k}
                    \n薪资20000 以下的有：\n{salary_below_20k}'''
                    )

app = QApplication([])
stats = Stats()
stats.window.show()
app.exec_()


