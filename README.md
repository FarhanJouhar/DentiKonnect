# DentiKonnect — Secure Patient Management System

> A prototype to bridge data between a dental lab and a clinic.

DentiKonnect is a lightweight, desktop-based Electronic Health Record (EHR) prototype designed for dental clinics. It prioritises data privacy and efficient retrieval of patient records and X-ray imagery.

# Problem

In many clinical settings, case information is shared through informal messaging tools, which can lead to confusion, missing details, and privacy concerns.

# Motivation

This project grew out of observing a gap in how patient data and radiograph images move between clinical teams and labs, often through channels with no audit trail and no encryption. DentiKonnect is an attempt to close this gap.

# Key Features

- **Encrypted Database**: XOR-based encryption for all sensitive patient data (names, ages, and X-ray BLOBs), stored as Base64-encoded strings.
- **Dual-Mode Search**: Patient lookup via Unique Patient ID (exact match) or Patient Name.
- **Integrated X-Ray Viewer**: Real-time decryption and rendering of stored radiographs and no external library dependencies. (PNG only).
- **Offline-First**: Runs entirely on SQLite3 with no internet connection needed.

> No external dependencies by design — the goal was a prototype any reviewer can run on a standard Python 3.10+ install without a pip install step.

# Security Implementation

A XOR Cipher is applied to all data before it is committed to the database.

- **Encryption at Rest:** Names and X-rays are stored as Base64-encoded ciphered strings.
- **Static Key (v1):** Uses a fixed key for demonstration. A production build would replace XOR with AES-256 and implement per-user key derivation.

# Planned Improvements

This is a working prototype. The next development priorities are:

- Replace XOR cipher with AES-256 encryption
- DICOM support for standard dental radiograph formats (replacing PNG)
- Visit-based patient records — persistent patient IDs with date-stamped visits, allowing clinicians to track a patient's history across multiple appointments

# Project Structure

```
main_gui.py              — Entry point and GUI
patient_manager.py       — DB connections, XOR encryption
Patient_Registration.py  — Registration tab for new patients(Reception or initial case history)
Radiology.py             — Radiology tab (Used by Radiology or a lab to upload X-rays as required)
Diagnosis.py             — Diagnosis tab for the clinic to edit and view patient info
Database/                — Auto-created on first save; holds DentiKonnect.db
```
