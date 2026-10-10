"""
Student Service Module.
Handles CRUD business logic, JSON storage persistence, search, and XML exports.
"""

import os
import json
import csv
import xml.etree.ElementTree as ET
from typing import List, Optional, Dict, Any

from src.models.student import Student
from src.utils.logger import setup_logger, load_config

class StudentService:
    """Business logic service managing student data operations."""

    def __init__(self, config_path: str = "config/config.json"):
        self.config = load_config(config_path)
        self.logger = setup_logger("StudentService")
        self.data_file = self.config.get("data_file", "data/students.json")
        self.export_dir = self.config.get("export_dir", "exports")
        
        self._ensure_directories()
        self.students: Dict[str, Student] = {}
        self.load_data()

    def _ensure_directories(self):
        """Create necessary data and export directories if they do not exist."""
        data_dir = os.path.dirname(self.data_file)
        if data_dir and not os.path.exists(data_dir):
            os.makedirs(data_dir, exist_ok=True)
        if not os.path.exists(self.export_dir):
            os.makedirs(self.export_dir, exist_ok=True)

    def load_data(self):
        """Loads student data from the JSON file into memory."""
        if not os.path.exists(self.data_file):
            self.logger.warning(f"Data file '{self.data_file}' not found. Initializing empty dataset.")
            self.save_data()
            return

        try:
            with open(self.data_file, "r") as f:
                data = json.load(f)
                self.students = {}
                for item in data:
                    student = Student.from_dict(item)
                    self.students[student.student_id] = student
            self.logger.info(f"Loaded {len(self.students)} student record(s) from {self.data_file}.")
        except Exception as e:
            self.logger.error(f"Failed to read data file '{self.data_file}': {e}")
            self.students = {}

    def save_data(self):
        """Persists memory data to the JSON storage file."""
        try:
            data = [student.to_dict() for student in self.students.values()]
            with open(self.data_file, "w") as f:
                json.dump(data, f, indent=4)
            self.logger.info(f"Persisted {len(data)} record(s) to storage.")
        except Exception as e:
            self.logger.error(f"Error saving data to '{self.data_file}': {e}")
            raise IOError("Cloud persistence operation failed.") from e

    # --- CRUD Operations ---
    def create_student(self, student_data: Dict[str, Any]) -> Student:
        """Create and store a new student record."""
        student = Student(**student_data)
        if student.student_id in self.students:
            raise ValueError(f"Student ID '{student.student_id}' already exists.")
        
        self.students[student.student_id] = student
        self.save_data()
        self.logger.info(f"Created student record ID: {student.student_id}")
        return student

    def get_all_students(self) -> List[Student]:
        """Return all student records."""
        return list(self.students.values())

    def get_student_by_id(self, student_id: str) -> Optional[Student]:
        """Fetch a single student record by ID."""
        return self.students.get(str(student_id).strip())

    def update_student(self, student_id: str, updates: Dict[str, Any]) -> Student:
        """Update fields of an existing student record."""
        student = self.get_student_by_id(student_id)
        if not student:
            raise KeyError(f"Student ID '{student_id}' not found.")

        current_data = student.to_dict()
        current_data.update(updates)
        
        # Re-validate by creating a fresh object
        updated_student = Student(**current_data)
        self.students[student_id] = updated_student
        self.save_data()
        self.logger.info(f"Updated student record ID: {student_id}")
        return updated_student

    def delete_student(self, student_id: str) -> bool:
        """Delete a student record by ID."""
        if student_id not in self.students:
            raise KeyError(f"Student ID '{student_id}' not found.")
        
        del self.students[student_id]
        self.save_data()
        self.logger.info(f"Deleted student record ID: {student_id}")
        return True

    # --- Bonus Features: Search & Multi-format Export ---
    def search_students(self, query: str) -> List[Student]:
        """Search students matching query against ID, Name, or Major."""
        query = query.strip().lower()
        matches = []
        for s in self.students.values():
            if (query in s.student_id.lower() or 
                query in s.name.lower() or 
                query in s.major.lower()):
                matches.append(s)
        return matches

    def export_to_xml(self, filename: str = "students_export.xml") -> str:
        """Export all current records to XML format."""
        filepath = os.path.join(self.export_dir, filename)
        root = ET.Element("StudentInformationSystem")
        for student in self.students.values():
            root.append(student.to_xml_element())
        
        tree = ET.ElementTree(root)
        tree.write(filepath, encoding="utf-8", xml_declaration=True)
        self.logger.info(f"Exported records to XML: {filepath}")
        return filepath

    def export_to_csv(self, filename: str = "students_export.csv") -> str:
        """Export all current records to CSV format."""
        filepath = os.path.join(self.export_dir, filename)
        if not self.students:
            raise ValueError("No records available to export.")

        fieldnames = ["student_id", "name", "age", "email", "major", "gpa"]
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for s in self.students.values():
                writer.writerow(s.to_dict())

        self.logger.info(f"Exported records to CSV: {filepath}")
        return filepath