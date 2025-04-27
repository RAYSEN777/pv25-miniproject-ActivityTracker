import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QSpinBox, QCheckBox, QListWidget, QMessageBox, QListWidgetItem
from PyQt5.QtCore import Qt, pyqtSignal

class TaskTracker(QWidget):
    def __init__(self):
        super().__init__()

        self.loadQss("style.qss")

        self.setWindowTitle("TaskTracker")
        self.setGeometry(100, 100, 800, 700)
        
        self.identitas = QLabel("Name: Teguh Dwi Julyanto\nNIM: F1D022098")
        self.identitas.setAlignment(Qt.AlignCenter) 
        
        self.task = QLineEdit(self)
        self.task.setPlaceholderText("Masukan Tugas Anda")
        
        self.priority = QComboBox(self)
        self.priority.addItems(["Rendah", "Sedang", "Tinggi"])
        
        self.addBut = QPushButton("Tambah Tugas", self)
        self.addBut.clicked.connect(self.addTask)

        self.delBut = QPushButton("Hapus Tugas", self)
        self.delBut.clicked.connect(self.delTask)
        
        self.taskList = CustomListWidget(self, "taskList")
        
        self.completedTask = CustomListWidget(self, "completedTask")
        
        self.taskList.itemDropped.connect(self.dropItem)
        self.completedTask.itemDropped.connect(self.dropItem)
        
        self.taskList.itemDoubleClicked.connect(self.completedMove)
        self.completedTask.itemDoubleClicked.connect(self.taskMove)
        
        taskLayout = QVBoxLayout()
        taskLayout.addWidget(self.identitas)
        taskLayout.addWidget(self.task)
        taskLayout.addWidget(QLabel("Prioritas :"))
        taskLayout.addWidget(self.priority)
        taskLayout.addWidget(self.addBut)
        taskLayout.addWidget(self.delBut)
        taskLayout.addWidget(QLabel("List Tugas:"))
        taskLayout.addWidget(self.taskList)

        completedLayout = QVBoxLayout()
        completedLayout.addWidget(QLabel("Selesai"))
        completedLayout.addWidget(self.completedTask)

        mainLayout = QHBoxLayout()
        mainLayout.addLayout(taskLayout, 2)
        mainLayout.addLayout(completedLayout, 1)

        self.setLayout(mainLayout)

    def loadQss(self, path):
            try:
                with open(path, "r") as f:
                    self.setStyleSheet(f.read())
            except Exception as e:
                print("Failed Qss", e)

    def addTask(self):
        task_name = self.task.text()
        if not task_name:
            self.erorrMess("Nama Tugas Tidak Boleh Kosong")
            return
        
        priority = self.priority.currentText()
        completed = "Pending" 
        
        task_details = f"{task_name} | Priority: {priority} | Status: {completed}"
        
        self.taskList.addItem(task_details)
        
        self.task.clear()
        self.priority.setCurrentIndex(0)


    def delTask(self):
        selected_item = self.taskList.currentItem()
        if selected_item:
            self.taskList.takeItem(self.taskList.row(selected_item))
        else:
            self.erorrMess("Tidak Ada Tugas")

    def erorrMess(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(message)
        msg.setWindowTitle("Error")
        msg.exec_()

    def completedMove(self, item):
        
        item_text = item.text()
        
        if "Status: Pending" in item_text:
            item_text = item_text.replace("Status: Pending", "Status: Completed")

        self.completedTask.addItem(item_text)
        
        self.taskList.takeItem(self.taskList.row(item))

    def taskMove(self, item):
        item_text = item.text()
        
        if "Status: Completed" in item_text:
            item_text = item_text.replace("Status: Completed", "Status: Pending")
        
        self.taskList.addItem(item_text)
        
        self.completedTask.takeItem(self.completedTask.row(item))
    
    def dropItem(self, source_list_name, target_list_name, item_text, source_item_row):
        if source_list_name == "taskList" and target_list_name == "completedTask":
            
            if "Status: Pending" in item_text:
                item_text = item_text.replace("Status: Pending", "Status: Completed")
            
            items = [self.completedTask.item(i).text() for i in range(self.completedTask.count())]
            if item_text not in items:
                self.completedTask.addItem(item_text)
            
            self.taskList.takeItem(source_item_row)
        
        elif source_list_name == "completedTask" and target_list_name == "taskList":
            
            if "Status: Completed" in item_text:
                item_text = item_text.replace("Status: Completed", "Status: Pending")
            
            items = [self.taskList.item(i).text() for i in range(self.taskList.count())]
            if item_text not in items:
                self.taskList.addItem(item_text)
            
            self.completedTask.takeItem(source_item_row)


class CustomListWidget(QListWidget):
    itemDropped = pyqtSignal(str, str, str, int)
    
    def __init__(self, parent, list_name):
        super().__init__(parent)
        self.list_name = list_name
        self.parent = parent
          
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setSelectionMode(QListWidget.SingleSelection)

        self.setDragDropMode(QListWidget.DragDrop)
    
    def dragEnterEvent(self, event):
        source = event.source()

        if not source:
            event.ignore()
            return

        source_list_name = source.list_name if hasattr(source, 'list_name') else "unknown"

        if source_list_name == self.list_name:
            event.ignore()
        else:
            
            event.accept()
    
    def dragMoveEvent(self, event):
        source = event.source()
 
        if not source:
            event.ignore()
            return

        source_list_name = source.list_name if hasattr(source, 'list_name') else "unknown"

        if source_list_name == self.list_name:
            event.ignore()
        else:
            
            event.accept()
    
    def dropEvent(self, event):
        source = event.source()

        if not source:
            event.ignore()
            return

        source_list_name = source.list_name if hasattr(source, 'list_name') else "unknown"

        if source_list_name == self.list_name:
            event.ignore()
            return

        if source and source.currentItem():
            item_text = source.currentItem().text()
            source_item_row = source.currentRow()
 
            self.itemDropped.emit(source_list_name, self.list_name, item_text, source_item_row)

            event.accept()
        else:
            event.ignore()

def main():
    app = QApplication(sys.argv)
    window = TaskTracker()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()