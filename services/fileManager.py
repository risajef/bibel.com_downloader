import os

from database.models import Translation, Chapter, Book



class FileManager:
    def __init__(self):
        self.base_path = os.path.join(os.getcwd(), "data")
    def get_path(self, translation: Translation, book: Book, chapter_index: int):
        return os.path.join(self.base_path, translation.website.value, translation.name, book.name, f"{chapter_index}.html")
    def write_data_to_file(self, data, translation: Translation, book: Book, chapter_index: int):
        path = self.get_path(translation, book, chapter_index)
        if self.file_exists(translation, book, chapter_index):
            return "File already exists"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(data)
        return f"File written to {path}"
    def file_exists(self, translation: Translation, book: Book, chapter_index: int):
        path = self.get_path(translation, book, chapter_index)
        return os.path.isfile(path)
    def read_file(self, translation: Translation, book: Book, chapter_index: int) -> str:
        with open(self.get_path(translation, book, chapter_index), "r") as f:
            return f.read()