# Student Information System (Cloud-Ready)

A modular, cloud-ready Python application designed to manage student records with strict data validation, JSON persistence, multi-format export capabilities, and structured logging.

## Features
- **Full CRUD Operations**: Create, Read, Update, and Delete student records.
- **Data Validation**: Strict runtime validation on IDs, Email formats, GPA limits, and Age constraints.
- **Cloud Architecture**:
  - Centralized JSON configuration (`config/config.json`).
  - Dual-logger system outputting to console and persistent log files (`logs/app.log`).
  - Decoupled model-service architecture.
- **Bonus Capabilities**:
  - Search engine for student filtering by ID, Name, or Major.
  - Export system supporting CSV and XML formats.
  - Full automated Unit Test suite (`unittest`).

## Repository Architecture
```text
student-info-system/
├── config/             # Environment configuration settings
├── data/               # Persistent JSON storage directory
├── logs/               # Application audit log storage
├── src/
│   ├── models/         # Entity definitions and input validation
│   ├── services/       # Core business logic & persistence handling
│   ├── utils/          # Shared utilities (logging)
│   └── main.py         # Application CLI interface
├── tests/              # Unit testing suite
├── README.md           # Documentation
└── requirements.txt    # Project dependencies