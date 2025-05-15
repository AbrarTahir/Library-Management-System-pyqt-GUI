# gui_app_qt.py (PyQt5 version)
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QLabel,
    QPushButton, QListWidget, QMessageBox, QCheckBox
)
from book_library import Book, EBook, Library, BookNotAvailableError
import sys

class LibraryApp(QWidget):
    def __init__(self):
        super().__init__()
        self.library = Library()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Library Management System")
        self.setGeometry(100, 100, 600, 600)

        layout = QVBoxLayout()

        self.title_entry = QLineEdit()
        layout.addWidget(QLabel("Title:"))
        layout.addWidget(self.title_entry)

        self.author_entry = QLineEdit()
        layout.addWidget(QLabel("Author:"))
        layout.addWidget(self.author_entry)

        self.isbn_entry = QLineEdit()
        layout.addWidget(QLabel("ISBN:"))
        layout.addWidget(self.isbn_entry)

        self.ebook_checkbox = QCheckBox("eBook?")
        self.ebook_checkbox.stateChanged.connect(self.toggle_size_entry)
        layout.addWidget(self.ebook_checkbox)

        self.size_entry = QLineEdit()
        self.size_entry.setPlaceholderText("Download Size (MB)")
        self.size_entry.setEnabled(False)
        layout.addWidget(self.size_entry)

        self.add_button = QPushButton("Add Book")
        self.add_button.clicked.connect(self.add_book)
        layout.addWidget(self.add_button)

        self.list_widget = QListWidget()
        layout.addWidget(QLabel("Library Inventory:"))
        layout.addWidget(self.list_widget)

        self.setLayout(layout)
        self.update_book_list()

    def toggle_size_entry(self):
        self.size_entry.setEnabled(self.ebook_checkbox.isChecked())
        if not self.ebook_checkbox.isChecked():
            self.size_entry.clear()

    def add_book(self):
        title = self.title_entry.text()
        author = self.author_entry.text()
        isbn = self.isbn_entry.text()
        is_ebook = self.ebook_checkbox.isChecked()
        size = self.size_entry.text()

        if not title or not author or not isbn:
            QMessageBox.warning(self, "Error", "Title, Author, and ISBN are required.")
            return

        if is_ebook:
            if not size:
                QMessageBox.warning(self, "Error", "Download size required for eBooks.")
                return
            if not size.isdigit():
                QMessageBox.warning(self, "Error", "Download size must be a number.")
                return
            book = EBook(title, author, isbn, size)
        else:
            book = Book(title, author, isbn)

        self.library.add_book(book)
        QMessageBox.information(self, "Success", f"Book '{title}' added to the library.")
        self.update_book_list()

    def update_book_list(self):
        self.list_widget.clear()
        self.list_widget.addItem("Available Books:")
        for book in self.library:
            self.list_widget.addItem(str(book))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LibraryApp()
    window.show()
    sys.exit(app.exec_())
