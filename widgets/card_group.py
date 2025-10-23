from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from widgets.card_widget import CardWidget

class CardGroupWidget(QWidget):
    """一组牌的显示组件"""
    
    def __init__(self, title, card_order, deck, parent=None):
        super().__init__(parent)
        self.title = title
        self.card_order = card_order
        self.deck = deck
        self.card_widgets = {}
        
        self.setup_ui()
        self.initialize_cards()
    
    def setup_ui(self):
        """设置UI"""
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        # 标题
        title_label = QLabel(self.title)
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont("Arial", 14, QFont.Bold)
        title_label.setFont(title_font)
        self.layout.addWidget(title_label)
        
        # 牌组容器
        self.card_layout = QGridLayout()
        self.card_container = QWidget()
        self.card_container.setLayout(self.card_layout)
        self.layout.addWidget(self.card_container)
    
    def initialize_cards(self):
        """初始化牌组件"""
        row, col = 0, 0
        for card_name in self.card_order:
            count = self.deck.cards.get(card_name, 0)
            card_widget = CardWidget(card_name, count)
            self.card_layout.addWidget(card_widget, row, col)
            self.card_widgets[card_name] = card_widget
            col += 1
            if col >= 6:  # 每行最多6张牌
                col = 0
                row += 1
    
    def update_display(self):
        """更新显示"""
        for card_name, widget in self.card_widgets.items():
            count = self.deck.cards.get(card_name, 0)
            widget.update_display(count)