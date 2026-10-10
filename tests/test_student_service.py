"""
Automated Unit Tests for StudentService and Student Model.
Run with: python -m unittest discover -s tests
"""

import os
import unittest
import tempfile
import json
from src.services.student_service import StudentService
from src.models.student import Student

class TestStudentInformationSystem(unittest.TestCase):

    def setUp(self):
        """Create temporary configuration and data files for test isolation."""
        self.test_dir = tempfile.TemporaryDirectory()
        self.data_file = os.path.join(self.test_dir.name, "students.json")
        self.config_file = os.path.join(self.test_dir.name, "config.json")

        config_data = {
            "data_file": self.data_file,
            "log_file": os.path.join(self.test_dir.name, "test.log"),
            "export_dir": os.path.join(self.test_dir.name, "exports")
        }
        with open(self.config_file, "w") as f:
            json.dump(config_data, f)

        self.service = StudentService(config_path=self.config_file)

    def tearDown(self):
        """Cleanup temporary files."""
        self.test_dir.cleanup()

    def test_create_and_get_student(self):
        sample_data = {
            "student_id": "ST101",
            "name": "Jane Doe",
            "age": 20,
            "email": "jane@example.com",
            "major": "Computer Science",
            "gpa": 3.8
        }
        student = self.service.create_student(sample_data)
        self.assertEqual(student.student_id, "ST101")
        
        retrieved = self.service.get_student_by_id("ST101")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.name, "Jane Doe")

    def test_invalid_email_validation(self):
        sample_data = {
            "student_id": "ST102",
            "name": "John Smith",
            "age": 22,
            "email": "invalid-email-format",
            "major": "IT",
            "gpa": 3.2
        }
        with self.assertRaises(ValueError):
            self.service.create_student(sample_data)

    def test_update_student(self):
        sample_data = {
            "student_id": "ST103",
            "name": "Alice Green",
            "age": 21,
            "email": "alice@example.com",
            "major": "Engineering",
            "gpa": 3.5
        }
        self.service.create_student(sample_data)
        updated = self.service.update_student("ST103", {"gpa": 3.9})
        self.assertEqual(updated.gpa, 3.9)

    def test_delete_student(self):
        sample_data = {
            "student_id": "ST104",
            "name": "Bob Brown",
            "age": 23,
            "email": "bob@example.com",
            "major": "Mathematics",
            "gpa": 3.1
        }
        self.service.create_student(sample_data)
        self.assertTrue(self.service.delete_student("ST104"))
        self.assertIsNone(self.service.get_student_by_id("ST104"))

if __name__ == "__main__":
    unittest.main()