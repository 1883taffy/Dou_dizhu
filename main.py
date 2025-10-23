import sys
import os

# 添加当前目录到Python路径，以便可以导入模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from ui.main_window import PokerTracker

def main():
    """程序主函数"""
    app = QApplication(sys.argv)
    
    # 设置应用样式
    app.setStyle("Fusion")
    
    # 创建并显示主窗口
    tracker = PokerTracker()
    tracker.show()
    
    # 运行应用
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()