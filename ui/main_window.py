import sys
import webbrowser
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QGridLayout, QLabel, QPushButton, 
                             QMessageBox, QInputDialog)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

from models.deck import Deck
from widgets.card_group import CardGroupWidget

class PokerTracker(QMainWindow):
    """斗地主记牌器主窗口"""
    
    def __init__(self):
        super().__init__()
        self.deck = Deck()
        self.card_groups = []
        
        self.setup_ui()
        self.setup_timer()
    
    def setup_ui(self):
        """设置UI"""
        self.setWindowTitle("斗地主记牌器")
        self.setFixedSize(800, 700)
        
        # 中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # 添加组件
        self.setup_title(main_layout)
        self.setup_card_groups(main_layout)
        self.setup_controls(main_layout)
        self.setup_status(main_layout)
        
        self.update_display()
    
    def setup_title(self, layout):
        """设置标题"""
        title_label = QLabel("斗地主记牌器")
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont("Arial", 20, QFont.Bold)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
    
    def setup_card_groups(self, layout):
        """设置牌组显示"""
        # 普通牌组
        ordinary_order = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2']
        ordinary_group = CardGroupWidget("普通牌", ordinary_order, self.deck)
        self.card_groups.append(ordinary_group)
        layout.addWidget(ordinary_group)
        
        # 王牌组
        joker_order = ['小王', '大王']
        joker_group = CardGroupWidget("王牌", joker_order, self.deck)
        self.card_groups.append(joker_group)
        layout.addWidget(joker_group)
    
    def setup_controls(self, layout):
        """设置控制区域"""
        control_layout = QHBoxLayout()
        layout.addLayout(control_layout)
        
        # 出牌按钮区域
        self.setup_play_buttons(control_layout)
        
        # 功能按钮区域
        self.setup_function_buttons(control_layout)
    
    def setup_play_buttons(self, layout):
        """设置出牌按钮"""
        play_card_layout = QVBoxLayout()
        layout.addLayout(play_card_layout)
        
        play_card_label = QLabel("快速出牌:")
        play_card_label.setFont(QFont("Arial", 12))
        play_card_layout.addWidget(play_card_label)
        
        # 创建常用牌按钮
        common_cards = ['3', '4', '5', '6', '7', '8', '9', '10', 
                       'J', 'Q', 'K', 'A', '2', '小王', '大王']
        
        common_cards_layout = QGridLayout()
        play_card_layout.addLayout(common_cards_layout)
        
        row, col = 0, 0
        for card_str in common_cards:
            button = QPushButton(card_str)
            button.clicked.connect(lambda checked, c=card_str: self.play_single_card(c))
            common_cards_layout.addWidget(button, row, col)
            col += 1
            if col >= 5:
                col = 0
                row += 1
    
    def setup_function_buttons(self, layout):
        """设置功能按钮"""
        function_layout = QVBoxLayout()
        layout.addLayout(function_layout)
        
        # 重置按钮
        reset_button = QPushButton("重置牌局")
        reset_button.clicked.connect(self.reset_deck)
        reset_button.setFont(QFont("Arial", 12))
        function_layout.addWidget(reset_button)
        
        # 自定义出牌按钮
        custom_play_button = QPushButton("自定义出牌")
        custom_play_button.clicked.connect(self.custom_play_cards)
        custom_play_button.setFont(QFont("Arial", 12))
        function_layout.addWidget(custom_play_button)
        
        # 作者主页按钮
        author_button = QPushButton("作者主页")
        author_button.clicked.connect(self.open_author_page)
        author_button.setFont(QFont("Arial", 12))
        function_layout.addWidget(author_button)
    
    def setup_status(self, layout):
        """设置状态显示"""
        status_layout = QHBoxLayout()
        layout.addLayout(status_layout)
        
        self.remaining_label = QLabel()
        self.remaining_label.setFont(QFont("Arial", 14))
        status_layout.addWidget(self.remaining_label)
    
    def setup_timer(self):
        """设置定时器"""
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_display)
        self.timer.start(100)  # 每100毫秒更新一次
    
    def play_single_card(self, card_str):
        """出一张牌"""
        success = self.deck.play_card(card_str)
        if not success:
            QMessageBox.warning(self, "出牌失败", f"无法出牌 {card_str}，可能牌已出完或不存在")
    
    def custom_play_cards(self):
        """自定义出多张牌，由空格分隔"""
        cards_input, ok = QInputDialog.getText(self, "自定义出牌", 
                                              "请输入要出的牌（多张牌用空格分隔）:\n例如: 3 3 3 或 小王 大王")
        if ok and cards_input:
            # 分割输入字符串
            card_list = cards_input.strip().split()
            if not card_list:
                QMessageBox.warning(self, "输入错误", "请输入至少一张牌")
                return
            
            # 出多张牌
            success, message = self.deck.play_cards(card_list)
            if not success:
                QMessageBox.warning(self, "出牌失败", message)
    
    def reset_deck(self):
        """重置牌堆"""
        reply = QMessageBox.question(self, "确认重置", "确定要重置所有牌吗？", 
                                    QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.deck.reset()
    
    def open_author_page(self):
        """打开作者主页"""
        author_url = "https://space.bilibili.com/1808878049"
        webbrowser.open(author_url)
    
    def update_display(self):
        """更新显示"""
        total_remaining = self.deck.get_total_remaining()
        self.remaining_label.setText(f"剩余牌数: {total_remaining}")
        
        for group in self.card_groups:
            group.update_display()