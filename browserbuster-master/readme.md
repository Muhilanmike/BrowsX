# Browser Password Extraction (Legacy Chromium) – Educational Demonstration

> **Disclaimer**
>
> **This project is provided strictly for educational, research, and defensive cybersecurity purposes only.**
>
> It demonstrates how **legacy Chromium-based browsers (prior to Chrome 126)** stored and protected saved credentials using Windows Data Protection API (DPAPI). It is intended to help students and security professionals understand historical browser credential storage mechanisms and their evolution.
>
> This project **does not support** browsers that implement **App-Bound Encryption**, introduced in Chrome 126 and later.
>
> The author does **not** encourage or endorse unauthorized access to systems, credential theft, or execution on devices without explicit permission.
>
> Use this project only in environments where you have explicit authorization, including:
>
> * Personal cybersecurity laboratories
> * Digital forensics exercises
> * Security research
> * Academic coursework
> * Defensive security training

---

# Browser Password Extraction (Legacy Chromium)

An educational Python project demonstrating how **legacy Chromium-based browsers** protected saved credentials before the introduction of **App-Bound Encryption**.

The project illustrates historical browser credential protection mechanisms, including:

* Windows Data Protection API (DPAPI)
* Chromium master key retrieval
* AES-GCM password decryption
* SQLite browser database structure
* Multi-profile browser enumeration

Its purpose is to help students, researchers, and defensive security practitioners understand how Chromium previously stored and protected credentials under the Windows user context.

---

## Features

* Supports legacy versions of **Google Chrome**
* Supports legacy versions of **Microsoft Edge**
* Enumerates multiple browser profiles
* Safely copies locked SQLite databases
* Retrieves Chromium master encryption keys from the Local State file
* Demonstrates DPAPI master key decryption
* Demonstrates AES-GCM password decryption
* Exports recovered credentials into a local text file

---

## Educational Objectives

This project is designed to demonstrate several Windows and Chromium security concepts, including:

* Windows Data Protection API (DPAPI)
* Chromium Local State structure
* Master key storage and retrieval
* AES-GCM encrypted credential format
* SQLite browser databases
* Browser profile organization
* Safe access to locked SQLite databases

It is intended for:

* Cybersecurity students
* Blue-team professionals
* Digital forensic analysts
* Incident responders
* Malware analysts
* Security researchers

---

## Requirements

* Python 3.9+
* Windows operating system

### Dependencies

```bash
pip install pywin32 pycryptodome
```

---

## Project Structure

```text
.
├── extract_final.py
├── passwords.txt      # Generated after execution
└── README.md
```

---

## How It Works

At a high level, the program performs the following steps:

1. Locate Chromium user data directories.
2. Read the browser's **Local State** file.
3. Obtain the encrypted browser master key.
4. Decrypt the master key using **Windows DPAPI**.
5. Enumerate browser profiles.
6. Create temporary copies of each **Login Data** SQLite database.
7. Read encrypted login records.
8. Decrypt credentials using the recovered master key.
9. Write the recovered information to a local text file.

---

## Compatibility

This project intentionally targets the **legacy Chromium credential storage model** used before the introduction of App-Bound Encryption.

| Browser Version                          | Support |
| ---------------------------------------- | ------- |
| Chrome < 126                             | ✅       |
| Chrome 126+                              | ❌       |
| Legacy Microsoft Edge (Chromium)         | ✅       |
| Edge versions using App-Bound Encryption | ❌       |

Beginning with **Chrome 126**, Chromium introduced **App-Bound Encryption**, significantly strengthening the protection of browser encryption keys by binding them more closely to the operating system and browser environment.

Supporting App-Bound Encryption is **intentionally outside the scope of this educational project**, whose objective is to demonstrate the historical DPAPI-based credential storage architecture.

---

## Output

Upon successful execution, the script generates:

```text
passwords.txt
```

The output is organized by browser and contains:

* Website URL
* Username
* Decrypted password

---

## Limitations

This educational demonstration is intentionally limited in scope.

* Windows only
* Supports legacy Chromium-based browsers only
* Requires execution under the current Windows user context
* Demonstrates only the historical DPAPI-based credential storage model
* Does **not** support Chrome 126+ or other browsers implementing App-Bound Encryption
* Does not bypass Windows authentication or browser security mechanisms

---

## Security Background

Historically, Chromium browsers protected stored credentials using:

* Windows Data Protection API (DPAPI)
* A browser-specific master encryption key
* AES-GCM encrypted passwords stored in SQLite databases

Beginning with **Chrome 126**, Chromium introduced **App-Bound Encryption**, which enhances protection of the browser's encryption keys by binding them more closely to the system environment.

This project focuses exclusively on the earlier DPAPI-based architecture for educational and historical study.

---

## Intended Use Cases

Appropriate uses include:

* Browser security education
* Digital forensics training
* Malware analysis education
* Defensive cybersecurity research
* Understanding Chromium internals
* Academic coursework
* Controlled cybersecurity laboratory exercises

---

## Ethical Use

Always obtain explicit authorization before accessing any system or user data.

Running this software against systems, accounts, or devices without permission may violate applicable laws, organizational policies, or ethical guidelines.

Users are solely responsible for ensuring that their use complies with all applicable laws and regulations.

---

## License

This repository is distributed **solely for educational, research, and defensive cybersecurity purposes**.

No warranty is provided.

The author assumes no responsibility for misuse, damages, or legal consequences resulting from the use of this software.

Users are responsible for ensuring compliance with all applicable laws, regulations, and organizational policies.
