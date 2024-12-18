from abc import ABC, abstractmethod


class FileSelectorInterface(ABC):

    @abstractmethod
    def load_directory_contents(self, directory_path):
        pass

    @abstractmethod
    def select_files_by_indices(self, indices, directory_path):
        pass

    @abstractmethod
    def get_selected_files(self):
        pass

    @abstractmethod
    def clear_selection(self):
        pass
