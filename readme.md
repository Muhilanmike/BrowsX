# 🔐 Browser Password Extractor - Educational Tool

> **⚠️ IMPORTANT DISCLAIMER**: This tool is designed **SOLELY** for educational purposes, authorized security testing, and cybersecurity research. Unauthorized use on systems without explicit permission is **illegal** and **unethical**. The author assumes no responsibility for misuse.

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Educational-red.svg)](LICENSE)
[![Windows](https://img.shields.io/badge/platform-Windows-0078D6.svg)](https://www.microsoft.com/windows)

---

## 📖 Table of Contents

- [Overview](#overview)
- [Educational Objectives](#educational-objectives)
- [How It Works](#how-it-works)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Browser Compatibility](#browser-compatibility)
- [Output Format](#output-format)
- [Security Background](#security-background)
- [Ethical Guidelines](#ethical-guidelines)
- [Project Structure](#project-structure)
- [License](#license)
- [Disclaimer](#disclaimer)

---

##  Overview

This project demonstrates how **legacy Chromium-based browsers** (Chrome, Edge) stored and protected saved credentials using **Windows Data Protection API (DPAPI)** before the introduction of **App-Bound Encryption**.

It serves as an educational resource for:
- Cybersecurity students
- Digital forensics professionals
- Security researchers
- Incident responders
- Penetration testers (authorized)

### What This Tool Does
1. Locates Chromium browser data directories
2. Extracts the browser's master encryption key
3. Decrypts saved passwords using DPAPI and AES-GCM
4. Exports credentials to a readable text file

---

## Educational Objectives

This project is designed to demonstrate several key security concepts:

| Concept | Description |
|---------|-------------|
| **Windows DPAPI** | Understanding how Windows protects user data |
| **Chromium Security** | How browsers store credentials locally |
| **Encryption Methods** | AES-GCM encryption in practice |
| **SQLite Databases** | Browser data storage structure |
| **Master Key Management** | Key extraction and decryption process |
| **Browser Evolution** | Security improvements over time |

---

## ⚙️ How It Works

```mermaid
graph TD
    A[Start] --> B[Find Browsers]
    B --> C[Read Local State File]
    C --> D[Extract Encrypted Key]
    D --> E[Decrypt with DPAPI]
    E --> F[Copy Login Database]
    F --> G[Read SQLite Database]
    G --> H[Decrypt Passwords with AES-GCM]
    H --> I[Export to Text File]
    I --> J[Done]
