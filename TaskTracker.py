import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QSpinBox, QCheckBox, QListWidget, QMessageBox, QListWidgetItem
from PyQt5.QtCore import Qt, pyqtSignal

class ToDoApp(QWidget):
    def __init__(self):
        super().__init__()

        self.load_stylesheet("style.qss")

        self.setWindowTitle("To-Do List App")
        self.setGeometry(100, 100, 800, 700)
        
        self.student_label = QLabel("Name: Teguh Dwi Julyanto\nNIM: F1D022098")
        self.student_label.setAlignment(Qt.AlignCenter) 
        
        self.task_input = QLineEdit(self)
        self.task_input.setPlaceholderText("Enter task here...")
        
        self.priority_input = QComboBox(self)
        self.priority_input.addItems(["Low", "Medium", "High"])
        
        self.duration_input = QSpinBox(self)
        self.duration_input.setRange(1, 24)  
        
        self.completed_checkbox = QCheckBox("Completed", self)
        
        self.add_button = QPushButton("Add Task", self)
        self.add_button.clicked.connect(self.add_task)

        self.remove_button = QPushButton("Remove Task", self)
        self.remove_button.clicked.connect(self.remove_task)
        
        self.task_list = CustomListWidget(self, "task_list")
        
        self.completed_list = CustomListWidget(self, "completed_list")
        
        self.task_list.itemDropped.connect(self.on_item_dropped)
        self.completed_list.itemDropped.connect(self.on_item_dropped)
        
        self.task_list.itemDoubleClicked.connect(self.move_to_completed)
        self.completed_list.itemDoubleClicked.connect(self.move_to_task)
        
        task_layout = QVBoxLayout()
        task_layout.addWidget(self.student_label)
        task_layout.addWidget(self.task_input)
        task_layout.addWidget(QLabel("Priority:"))
        task_layout.addWidget(self.priority_input)
        task_layout.addWidget(QLabel("Duration (hours):"))
        task_layout.addWidget(self.duration_input)
        task_layout.addWidget(self.completed_checkbox)
        task_layout.addWidget(self.add_button)
        task_layout.addWidget(self.remove_button)
        task_layout.addWidget(QLabel("Tasks:"))
        task_layout.addWidget(self.task_list)

        completed_layout = QVBoxLayout()
        completed_layout.addWidget(QLabel("Completed Tasks"))
        completed_layout.addWidget(self.completed_list)

        main_layout = QHBoxLayout()
        main_layout.addLayout(task_layout, 2)
        main_layout.addLayout(completed_layout, 1)

        self.setLayout(main_layout)

    def load_stylesheet(self, path):
            try:
                with open(path, "r") as f:
                    self.setStyleSheet(f.read())
            except Exception as e:
                print("Failed to load stylesheet:", e)

    def add_task(self):
        task_name = self.task_input.text()
        if not task_name:
            self.show_error_message("Task name cannot be empty!")
            return
        
        priority = self.priority_input.currentText()
        duration = self.duration_input.value()
        completed = "Completed" if self.completed_checkbox.isChecked() else "Pending"
        
        task_details = f"{task_name} | Priority: {priority} | Duration: {duration} hours | Status: {completed}"
        
        self.task_list.addItem(task_details)
        
        self.task_input.clear()
        self.priority_input.setCurrentIndex(0)
        self.duration_input.setValue(1)
        self.completed_checkbox.setChecked(False)

    def remove_task(self):
        selected_item = self.task_list.currentItem()
        if selected_item:
            self.task_list.takeItem(self.task_list.row(selected_item))
        else:
            self.show_error_message("No task selected to remove!")

    def show_error_message(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(message)
        msg.setWindowTitle("Error")
        msg.exec_()

    def move_to_completed(self, item):
        
        item_text = item.text()
        
        if "Status: Pending" in item_text:
            item_text = item_text.replace("Status: Pending", "Status: Completed")

        self.completed_list.addItem(item_text)
        
        self.task_list.takeItem(self.task_list.row(item))

    def move_to_task(self, item):
        item_text = item.text()
        
        if "Status: Completed" in item_text:
            item_text = item_text.replace("Status: Completed", "Status: Pending")
        
        self.task_list.addItem(item_text)
        
        self.completed_list.takeItem(self.completed_list.row(item))
    
    def on_item_dropped(self, source_list_name, target_list_name, item_text, source_item_row):
        if source_list_name == "task_list" and target_list_name == "completed_list":
            
            if "Status: Pending" in item_text:
                item_text = item_text.replace("Status: Pending", "Status: Completed")
            
            items = [self.completed_list.item(i).text() for i in range(self.completed_list.count())]
            if item_text not in items:
                self.completed_list.addItem(item_text)
            
            self.task_list.takeItem(source_item_row)
        
        elif source_list_name == "completed_list" and target_list_name == "task_list":
            
            if "Status: Completed" in item_text:
                item_text = item_text.replace("Status: Completed", "Status: Pending")
            
            items = [self.task_list.item(i).text() for i in range(self.task_list.count())]
            if item_text not in items:
                self.task_list.addItem(item_text)
            
            self.completed_list.takeItem(source_item_row)


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
    window = ToDoApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()