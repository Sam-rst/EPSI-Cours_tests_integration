from app.components.fileSystem.file_manager import FileManager

class Menu:
    def __init__(self):
        self.file_manager = FileManager()
        self.commands = [
            "Display Directory",
            "Navigate",
            "Go to Parent Directory",
            "Select Files",
            "Copy",
            "Move",
            "Delete",
            "Quit",
            ]
        self.choice = None

    def display_commands(self):
        message = "\n--- File Explorer ---\n"
        message += ''.join([f"{i}. {str(self.commands[i])}\n" for i in range(len(self.commands))])
        print(message)

    def ask_choice(self, message_input) -> int:
        choice = input(f"{message_input}")
        try:
            self.choice = int(choice)
            return self.choice
        except ValueError:
            print("Input not valid !")
            self.choice = -1
            return self.ask_choice(message_input)

    def update(self):
        try:
            match self.choice:
                case 0:
                    self.file_manager.file_explorer.display_directory_contents()
                    return True

                case 1:
                    index = self.ask_choice("Enter navigation index: ")
                    self.file_manager.file_explorer.navigate(index)
                    return True

                case 2:
                    self.file_manager.file_explorer.go_to_parent_directory()
                    return True

                case 3:
                    self.file_manager.file_explorer.display_directory_contents()
                    indices = input("Enter file indices to select (comma-separated): ")
                    self.file_manager.file_selector.select_files_by_indices(indices, self.file_manager.file_explorer.current_path)
                    return True

                case 4:
                    dest = input("Enter destination path for copying: ")
                    self.file_manager.copy_files(dest)
                    return True

                case 5:
                    dest = input("Enter destination path for moving: ")
                    self.file_manager.move_files(dest)
                    return True

                case 6:
                    self.file_manager.delete_files()
                    return True

                case 7:
                    print("Goodbye!")
                    return False

        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def engine(self):
        while True:
            self.file_manager.file_explorer.display_directory_contents()
            self.display_commands()
            self.ask_choice("Choice : ")
            if not self.update():
                break