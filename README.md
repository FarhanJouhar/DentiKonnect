# DentiKonnect - Secure Patient Management System

--A prototype to bridge data between a lab and a clinic--

DentiKonnect is a lightweight, desktop-based Electronic Health Record (EHR) prototype designed for dental clinics. It prioritizes data privacy and efficient retrieval of patient records and X-ray imagery.

Key Features
Encrypted Database: Implements a custom XOR-based encryption layer for all sensitive patient data (Names, Ages, and X-ray BLOBs).

Dual-Mode Search: Supports rapid patient lookup via Unique Patient ID (exact match) or Patient Name .

Integrated X-Ray Viewer: Real-time decryption and rendering of patient X-rays without any external Libraries(Only PNGs).

Scalable Architecture: Built on SQLite3 for high-speed data management and persistence.

Technical Stack
Language: Python 3.10+

Database: SQLite3

Libraries:

sqlite3: Local data persistence.

base64: Encoding for encrypted binary data.

tkinter: GUI development.

Security Implementation
To ensure basic data privacy in this prototype, a XOR Cipher is applied to data before it is committed to the database.

Encryption at Rest: Names and X-rays are stored as Base64-encoded ciphered strings.

Static Key Management: (Current Version) Utilizes a static key for demonstration.

Project Structure
main_gui.py: The entry point for the GUI and user interaction.

patient_manager.py: Core logic for database connections, encryption, and search algorithms.

/Database/: Contains the encrypted DentiKonnect.db file(Created upon running main_gui.py and saving a patient)