import unittest


class TestUnittestSetup(unittest.TestCase):
    def test_addition(self):
        """Vérifie que l'addition fonctionne correctement."""
        self.assertEqual(2 + 2, 4)

    def test_string(self):
        """Vérifie le comportement des chaînes de caractères."""
        self.assertTrue("hello".islower())
        self.assertEqual("hello".upper(), "HELLO")

    def test_list(self):
        """Vérifie les opérations sur les listes."""
        sample_list = [1, 2, 3]
        self.assertIn(2, sample_list)
        self.assertNotIn(5, sample_list)
        self.assertEqual(len(sample_list), 3)


if __name__ == "__main__":
    unittest.main()
