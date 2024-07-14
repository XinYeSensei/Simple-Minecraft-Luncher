import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt
import subprocess
import shutil
import os
import glob
import Ui_main  # 导入转换后的UI文件
import resource_rc  # 导入资源文件（如果有）

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        # 创建UI对象并将其设置到主窗口上
        self.ui = Ui_main.Ui_MainWindow()
        self.ui.setupUi(self)
        
        # 设置滑块的范围和初始值为1GB到32GB
        min_size_gb = 1
        max_size_gb = 32
        
        # 将GB转换为整数值（例如1GB就是1）
        self.ui.horizontalSlider.setMinimum(min_size_gb)
        self.ui.horizontalSlider.setMaximum(max_size_gb)
        self.ui.horizontalSlider.setValue(min_size_gb)  # 初始值设置为1GB
        
        # 设置spinBox的范围和初始值
        self.ui.spinBox.setMinimum(min_size_gb)
        self.ui.spinBox.setMaximum(max_size_gb)
        self.ui.spinBox.setValue(min_size_gb)  # 初始值设置为1GB
        
        # 将horizontalSlider的valueChanged信号连接到spinBox的setValue槽
        self.ui.horizontalSlider.valueChanged.connect(self.slider_changed)
        
        # 将spinBox的valueChanged信号连接到horizontalSlider的setValue槽
        self.ui.spinBox.valueChanged.connect(self.ui.horizontalSlider.setValue)
        
        # 连接ToolButton的点击事件到槽函数
        self.ui.toolButton.clicked.connect(self.open_folder_dialog)
        
        # 连接启动按钮的点击事件到槽函数
        self.ui.pushButton.clicked.connect(self.start_minecraft)  # 修改这里的连接方法名
        
    def slider_changed(self, value):
        # 更新spinBox显示的值
        self.ui.spinBox.setValue(value)
        
    def open_folder_dialog(self):
        # 打开文件夹对话框
        folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if folder_path:
            # 将文件夹路径显示在QLineEdit中
            self.ui.lineEdit.setText(folder_path)
            
    def start_minecraft(self):
        # 启动 Minecraft
        
        # 获取用户选择的文件夹路径
        folder_path = self.ui.lineEdit.text().strip()
        
        if not folder_path:
            QMessageBox.warning(self, "警告", "请选择有效的文件夹路径")
            return
        
        # 检查 Minecraft 文件夹完整性并启动游戏
        if not self.check_minecraft_folder(folder_path):
            return
        
        # 启动 Minecraft
        self.launch_minecraft(folder_path)
        
    def check_minecraft_folder(self, folder_path):
        # 检查 Minecraft 文件夹是否完整
        current_dir = os.getcwd()  # 获取当前工作目录
        jar_files = glob.glob(os.path.join(current_dir, '*.jar')) 

        # 示例：假设需要检查的文件是一个名为 "minecraft.jar" 的文件
        if jar_files: 
            minecraft_jar_path = os.path.join(folder_path, "*.jar")
        
        if not os.path.exists(minecraft_jar_path):
            # 文件不存在，尝试自动修复
            if not self.auto_repair_minecraft(folder_path):
                QMessageBox.critical(self, "错误", "无法找到 Minecraft 文件，请确保文件完整性。")
                return False
        
        return True
    
    def auto_repair_minecraft(self, folder_path):
        # 示例：尝试自动修复 Minecraft 文件夹中缺失的文件
        
        # 假设可以从网络下载缺失的文件，这里只是演示
        # 实际情况可能需要备份、重新下载或其他操作
        try:
            # 下载或其他自动修复操作
            # 示例：复制一个已有的备份文件
            source_file = "backup/minecraft.jar"
            target_file = os.path.join(folder_path, "minecraft.jar")
            shutil.copyfile(source_file, target_file)
            
            QMessageBox.information(self, "信息", "文件自动修复完成。")
            return True
        
        except Exception as e:
            print("自动修复错误:", str(e))
            return False
    
    def launch_minecraft(self, folder_path):
        # 启动 Minecraft
        
        # 示例：假设启动命令为 java -jar minecraft.jar
        minecraft_jar_path = os.path.join(folder_path, "minecraft.jar")
        command = ["java", "-jar", minecraft_jar_path]
        
        try:
            # 启动 Minecraft
            subprocess.Popen(command)
        
        except Exception as e:
            QMessageBox.critical(self, "错误", f"启动 Minecraft 失败：{str(e)}")
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())