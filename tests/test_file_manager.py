import unittest, os, shutil
from unittest.mock import MagicMock, patch, call
from correction.futils import FileManager, FileSelection, FileSystem
from correction.ui import UserInterface


class TestFileManager(unittest.TestCase):
    def setUp(self):
        """
        Cette méthode est appelée avant chaque test.
        Elle crée un répertoire 'destination' dans le répertoire 'tests' pour les tests.
        """
        # Création du répertoire de destination avant chaque test
        self.test_dir = os.path.join(
            os.path.dirname(__file__), ""
        )  # répertoire des tests
        self.destination_dir = os.path.join(self.test_dir, "destination")

        # Si le répertoire existe déjà, on le supprime pour repartir sur une base propre
        if os.path.exists(self.destination_dir):
            shutil.rmtree(self.destination_dir)

        os.makedirs(self.destination_dir)

        # Mocks pour les dépendances
        self.file_selection = MagicMock(spec=FileSelection)
        self.file_system = MagicMock(spec=FileSystem)
        self.ui = MagicMock(spec=UserInterface)

        # Instance de FileManager avec des mocks
        self.file_manager = FileManager(
            sel=self.file_selection,
            fs=self.file_system,
            ui=self.ui,
            destination=self.destination_dir,  # Passer le répertoire de destination
        )

    def tearDown(self):
        """
        Cette méthode est appelée après chaque test.
        Elle supprime le répertoire 'destination' après chaque test pour s'assurer que l'environnement est propre.
        """
        if os.path.exists(self.destination_dir):
            shutil.rmtree(self.destination_dir)

    @patch("os.path.exists", return_value=True)
    def test_copy_files_success(self, mock_exists):
        """
        Teste le cas où tous les fichiers sélectionnés sont copiés avec succès.
        - Configure deux fichiers sélectionnés.
        - Vérifie que les fichiers sont copiés et que la méthode `copy` est appelée correctement.
        - Vérifie que la méthode `get_and_reset` est appelée une fois.
        """
        self.file_selection.get_and_reset.return_value = ["file1.txt", "file2.txt"]
        destination = "/destination/"

        count = self.file_manager.copy_files(destination)

        self.assertEqual(count, 2)
        self.file_system.copy.assert_has_calls(
            [call("file1.txt", destination), call("file2.txt", destination)]
        )
        self.file_selection.get_and_reset.assert_called_once()

    def test_move_files_success(self):
        """
        Teste le cas où tous les fichiers sélectionnés sont déplacés avec succès.
        - Configure deux fichiers sélectionnés.
        - Vérifie que les fichiers sont déplacés et que la méthode `move` est appelée correctement.
        - Vérifie que la méthode `get_and_reset` est appelée une fois.
        """
        self.file_selection.get_and_reset.return_value = ["file1.txt", "file2.txt"]
        destination = "/destination/"

        count = self.file_manager.move_files(destination)

        self.assertEqual(count, 2)
        self.file_system.move.assert_has_calls(
            [call("file1.txt", destination), call("file2.txt", destination)]
        )
        self.file_selection.get_and_reset.assert_called_once()

    def test_delete_files_success(self):
        """
        Teste le cas où tous les fichiers sélectionnés sont supprimés avec succès.
        - Configure deux fichiers sélectionnés (un fichier simple et un dossier).
        - Vérifie que les fichiers sont supprimés et que la méthode `delete` est appelée correctement.
        - Vérifie que la méthode `get_and_reset` est appelée une fois.
        """
        self.file_selection.get_and_reset.return_value = ["file1.txt", "folder1/"]

        count = self.file_manager.delete_files()

        self.assertEqual(count, 2)
        self.file_system.delete.assert_has_calls([call("file1.txt"), call("folder1/")])
        self.file_selection.get_and_reset.assert_called_once()

    def test_copy_files_empty_selection(self):
        """
        Teste le cas où aucun fichier n'est sélectionné pour la copie.
        - Vérifie que la méthode `copy` n'est pas appelée.
        - Vérifie que le compteur retourne 0.
        """
        self.file_selection.get_and_reset.return_value = []
        destination = "/destination/"

        count = self.file_manager.copy_files(destination)

        self.assertEqual(count, 0)
        self.file_system.copy.assert_not_called()

    def test_copy_files_with_error(self):
        """
        Teste le cas où une erreur survient pendant la copie d'un des fichiers.
        - Configure deux fichiers sélectionnés.
        - Simule une erreur pour l'un des fichiers.
        - Vérifie que le compteur retourne 1 pour le fichier copié avec succès.
        - Vérifie que l'erreur est correctement loggée via l'interface utilisateur.
        """
        self.file_selection.get_and_reset.return_value = ["file1.txt", "file2.txt"]
        destination = "/destination/"

        self.file_system.copy.side_effect = [None, Exception("Copy failed")]

        count = self.file_manager.copy_files(destination)

        self.assertEqual(count, 0)
        self.ui.error.assert_called_with("Destination path does not exist")

    def test_delete_files_with_error(self):
        """
        Teste le cas où une erreur survient pendant la suppression d'un des fichiers.
        - Configure deux fichiers sélectionnés.
        - Simule une erreur pour l'un des fichiers.
        - Vérifie que le compteur retourne 1 pour le fichier supprimé avec succès.
        - Vérifie que l'erreur est correctement loggée via l'interface utilisateur.
        """
        self.file_selection.get_and_reset.return_value = ["file1.txt", "folder1/"]

        self.file_system.delete.side_effect = [None, Exception("Delete failed")]

        count = self.file_manager.delete_files()

        self.assertEqual(count, 1)
        self.ui.error.assert_called_with("Delete: Delete failed")

    def test_move_files_with_error(self):
        """
        Teste le cas où une erreur survient pendant le déplacement d'un des fichiers.
        - Configure deux fichiers sélectionnés.
        - Simule une erreur pour l'un des fichiers.
        - Vérifie que le compteur retourne 1 pour le fichier déplacé avec succès.
        - Vérifie que l'erreur est correctement loggée via l'interface utilisateur.
        """
        self.file_selection.get_and_reset.return_value = ["file1.txt", "file2.txt"]
        destination = "/destination/"

        self.file_system.move.side_effect = [Exception("Move failed"), None]

        count = self.file_manager.move_files(destination)

        self.assertEqual(count, 1)
        self.ui.error.assert_called_with("Move: Move failed")

    def test_copy_files_no_selection(self):
        """
        Test: Aucun fichier n'est sélectionné pour la copie.
        Vérifie que la méthode retourne 0 et qu'aucune opération de copie n'est effectuée.
        """
        self.file_selection.get_and_reset.return_value = []
        destination = "/destination/"

        count = self.file_manager.copy_files(destination)

        self.assertEqual(count, 0)
        self.file_system.copy.assert_not_called()

    def test_copy_files_invalid_destination(self):
        """
        Test: La destination est invalide ou inaccessible.
        Vérifie que la méthode gère correctement une exception pour une destination non valide.
        """
        self.file_selection.get_and_reset.return_value = ["file1.txt"]
        destination = "/invalid/destination/"

        self.file_system.copy.side_effect = Exception("Invalid destination")

        count = self.file_manager.copy_files(destination)

        self.assertEqual(count, 0)
        self.ui.error.assert_called_once_with("Destination path does not exist")

    def test_copy_files_existing_file(self):
        """
        Test: Un fichier avec le même nom existe déjà dans la destination.
        Vérifie que la méthode gère correctement une exception "File exists".
        """
        self.file_selection.get_and_reset.return_value = ["file1.txt"]
        destination = "/destination/"

        self.file_system.copy.side_effect = Exception("File exists")

        count = self.file_manager.copy_files(destination)

        self.assertEqual(count, 0)
        self.ui.error.assert_called_once_with("Destination path does not exist")

    def test_copy_files_multiple_success(self):
        """
        Test: Tous les fichiers sont copiés avec succès.
        Vérifie que la méthode retourne le bon nombre de fichiers copiés
        et que chaque fichier est traité.
        """
        self.file_selection.get_and_reset.return_value = [
            "file1.txt",
            "file2.txt",
            "file3.txt",
        ]
        destination = "/destination/"

        self.file_system.copy.side_effect = [None, None, None]

        count = self.file_manager.copy_files(destination)
        print("*" * 20)
        print(count)
        print("*" * 20)

        self.assertEqual(count, 3)
        self.file_system.copy.assert_has_calls(
            [
                unittest.mock.call("file1.txt", destination),
                unittest.mock.call("file2.txt", destination),
                unittest.mock.call("file3.txt", destination),
            ],
            any_order=False,
        )

    def test_copy_files_partial_success(self):
        """
        Test: Certains fichiers sont copiés avec succès, mais d'autres échouent.
        Vérifie que la méthode retourne le nombre correct de fichiers copiés
        et affiche une erreur pour chaque fichier ayant échoué.
        """
        self.file_selection.get_and_reset.return_value = [
            "file1.txt",
            "file2.txt",
            "file3.txt",
        ]
        destination = "/destination/"

        self.file_system.copy.side_effect = [None, Exception("Copy failed"), None]

        count = self.file_manager.copy_files(destination)

        self.assertEqual(count, 2)
        self.ui.error.assert_called_once_with("Copy: Copy failed")

    def test_copy_files_all_fail(self):
        """
        Test: Tous les fichiers échouent à être copiés.
        Vérifie que la méthode retourne 0, affiche une erreur pour chaque fichier,
        et ne compte aucun fichier comme réussi.
        """
        self.file_selection.get_and_reset.return_value = ["file1.txt", "file2.txt"]
        destination = "/destination/"

        self.file_system.copy.side_effect = Exception("Copy failed")

        count = self.file_manager.copy_files(destination)

        self.assertEqual(count, 0)
        self.ui.error.assert_called_with("Destination path does not exist")
        self.assertEqual(self.ui.error.call_count, 2)

    @patch("os.path.exists", return_value=False)
    def test_copy_files_destination_does_not_exist(self, mock_exists):
        """
        Teste le cas où le chemin de destination pour la copie n'existe pas.
        - Vérifie que le système logge une erreur via l'interface utilisateur.
        - Vérifie qu'aucun fichier n'est copié.
        """
        self.file_selection.get_and_reset.return_value = ["file1.txt"]
        destination = "/nonexistent_destination/"

        count = self.file_manager.copy_files(destination)

        # Vérifie que le compte est 0 car la destination n'existe pas
        self.assertEqual(count, 0)
        # Vérifie que l'erreur a été loggée
        self.ui.error.assert_called_with("Destination path does not exist")
        # Vérifie que la méthode copy n'a pas été appelée
        self.file_system.copy.assert_not_called()

    def test_delete_files_empty_selection(self):
        """
        Teste le cas où aucun fichier n'est sélectionné pour suppression.
        - Vérifie que la méthode `delete` n'est pas appelée.
        - Vérifie que le compteur retourne 0.
        """
        self.file_selection.get_and_reset.return_value = []

        count = self.file_manager.delete_files()

        self.assertEqual(count, 0)
        self.file_system.delete.assert_not_called()

    def test_copy_large_number_of_files(self):
        """
        Teste le cas où un grand nombre de fichiers est copié.
        - Simule une sélection de 1000 fichiers.
        - Vérifie que tous les fichiers sont copiés avec succès.
        """
        files = [f"file{i}.txt" for i in range(1000)]
        self.file_selection.get_and_reset.return_value = files
        destination = "/destination/"

        count = self.file_manager.copy_files(destination)

        self.assertEqual(count, 1000)
        self.file_system.copy.assert_has_calls(
            [call(file, destination) for file in files], any_order=True
        )

    def test_delete_files_permission_error(self):
        """
        Teste le cas où une erreur de permission survient pendant la suppression.
        - Simule une erreur de permission pour un des fichiers.
        - Vérifie que l'erreur est correctement loggée.
        - Vérifie que les autres fichiers sont supprimés correctement.
        """
        self.file_selection.get_and_reset.return_value = ["file1.txt", "file2.txt"]
        self.file_system.delete.side_effect = [
            PermissionError("Permission denied"),
            None,
        ]

        count = self.file_manager.delete_files()

        self.assertEqual(count, 1)
        self.ui.error.assert_called_with("Delete: Permission denied")

    def test_copy_files_invalid_destination_path(self):
        """
        Teste le cas où le chemin de destination est invalide.
        - Simule un chemin avec des caractères interdits.
        - Vérifie que la méthode `copy` n'est pas appelée.
        - Vérifie que l'erreur est loggée.
        """
        self.file_selection.get_and_reset.return_value = ["file1.txt"]
        destination = "/invalid<>path/"

        count = self.file_manager.copy_files(destination)

        self.assertEqual(count, 0)
        self.ui.error.assert_called_with("Destination path does not exist")
        self.file_system.copy.assert_not_called()

    def test_move_files_locked_file(self):
        """
        Teste le cas où un fichier verrouillé est déplacé.
        - Simule une erreur de verrouillage pour un fichier.
        - Vérifie que l'erreur est loggée.
        - Vérifie que les autres fichiers sont déplacés correctement.
        """
        self.file_selection.get_and_reset.return_value = ["file1.txt", "file2.txt"]
        destination = "/destination/"
        self.file_system.move.side_effect = [OSError("File is locked"), None]

        count = self.file_manager.move_files(destination)

        self.assertEqual(count, 1)
        self.ui.error.assert_called_with("Move: File is locked")

    @patch("os.path.exists", side_effect=[True, False])
    def test_copy_files_file_not_found(self, mock_exists):
        """
        Teste le cas où un fichier sélectionné n'existe plus.
        - Vérifie que l'erreur est loggée.
        - Vérifie que les autres fichiers sont copiés.
        """
        self.file_selection.get_and_reset.return_value = ["file1.txt", "file2.txt"]
        destination = "/destination/"

        count = self.file_manager.copy_files(destination)

        self.assertEqual(count, 1)
        self.ui.error.assert_called_with("Copy: File not found")


if __name__ == "__main__":
    unittest.main()
