from abc import ABC, abstractmethod


class FileManagerInterface(ABC):

    @abstractmethod
    def copy_files(self, destination):
        pass

    @abstractmethod
    def move_files(self, destination):
        pass

    @abstractmethod
    def delete_files(self):
        pass