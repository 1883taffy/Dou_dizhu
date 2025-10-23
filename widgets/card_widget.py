from PyQt5.QtWidgets import QLabel, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class CardWidget(QLabel):
    """单张牌的显示组件"""
    
    def __init__(self, card_name, count, parent=None):
        super().__init__(parent)
        self.card_name = card_name
        self.count = count
        self.setup_ui()
    
    def setup_ui(self):
        """设置UI"""
        self.setFixedSize(80, 100)
        self.setAlignment(Qt.AlignCenter)
        self.setFrameStyle(QFrame.Box)
        self.setLineWidth(2)
        
        # 设置字体
        font = QFont("Arial", 12)
        self.setFont(font)
        
        self.update_display()
    
    def update_display(self, count=None):
        """更新显示"""
        if count is not None:
            self.count = count
            
        if self.count > 0:
            self.setText(f"{self.card_name}\n剩余:{self.count}")
            self.setStyleSheet("background-color: white; color: black; border: 2px solid black;")
        else:
            self.setText(f"{self.card_name}\n已出完")
            self.setStyleSheet("background-color: lightgray; color: gray; border: 2px solid gray;")