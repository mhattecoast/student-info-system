"""
Student Model Module.
Defines the Student entity with strict data validation.
"""

import re
import xml.etree.ElementTree as ET
from typing import Dict, Any

class Student:
    """Represents a student entity with field validations."""
    
    def __init__(self, student_id: str, name: str, age: int, email: str, major: str, gpa: float):
        self.student_id = self.validate_student_id(student_id)
        self.name = self.validate_name(name)
        self.age = self.validate_age(age)
        self.email = self.validate_email(email)
        self.major = self.validate_major(major)
        self.gpa = self.validate_gpa(gpa)

    # --- Data Validation Methods (Bonus Feature) ---
    @staticmethod
    def validate_student_id(student_id: str) -> str:
        student_id = str(student_id).strip()
        if not student_id or not student_id.isalnum():
            raise ValueError("Student ID must be a non-empty alphanumeric string.")
        return student_id

    @staticmethod
    def validate_name(name: str) -> str:
        name = str(name).strip()
        if not name or len(name) < 2:
            raise ValueError("Name must be at least 2 characters long.")
        return name

    @staticmethod
    def validate_age(age: int) -> int:
        try:
            age = int(age)
        except (ValueError, TypeError):
            raise ValueError("Age must be an integer.")
        if not (16 <= age <= 100):
            raise ValueError("Age must be between 16 and 100.")
        return age

    @staticmethod
    def validate_email(email: str) -> str:
        email = str(email).strip()
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(pattern, email):
            raise ValueError("Invalid email address format.")
        return email

    @staticmethod
    def validate_major(major: str) -> str:
        major = str(major).strip()
        if not major:
            raise ValueError("Major cannot be empty.")
        return major

    @staticmethod
    def validate_gpa(gpa: float) -> float:
        try:
            gpa = float(gpa)
        except (ValueError, TypeError):
            raise ValueError("GPA must be a valid float value.")
        if not (0.0 <= gpa <= 4.0):
            raise ValueError("GPA must be between 0.0 and 4.0.")
        return round(gpa, 2)

    # --- Serialization Helpers ---
    def to_dict(self) -> Dict[str, Any]:
        """Convert Student object to dictionary for JSON persistence."""
        return {
            "student_id": self.student_id,
            "name": self.name,
            "age": self.age,
            "email": self.email,
            "major": self.major,
            "gpa": self.gpa
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Student":
        """Instantiate a Student object from a dictionary."""
        return cls(
            student_id=data["student_id"],
            name=data["name"],
            age=data["age"],
            email=data["email"],
            major=data["major"],
            gpa=data["gpa"]
        )

    def to_xml_element(self) -> ET.Element:
        """Convert Student object to XML Element for export."""
        elem = ET.Element("Student")
        for key, val in self.to_dict().items():
            child = ET.SubElement(elem, key)
            child.text = str(val)
        return elem