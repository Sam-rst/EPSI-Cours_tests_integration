from abc import ABC, abstractmethod


class FileExplorerInterface(ABC):

    @abstractmethod
    def display_directory_contents(self):
        pass

    @abstractmethod
    def navigate(self, index):
        pass

    @abstractmethod
    def go_to_parent_directory(self):
        pass
