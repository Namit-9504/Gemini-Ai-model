
```markdown
# ATS System - Modified Version

## Introduction

This repository contains the modified version of our Applicant Tracking System (ATS). In this update, we have addressed the dependency on Poppler Windows, specifically required by the `pdf2image` package in the previous ATS system.

## Changes Made

In the original ATS system, we encountered a dependency issue with the `pdf2image` package, which required Poppler Windows to be pre-installed on the system. This posed challenges for users as it introduced an additional requirement for running the application.

To enhance the user experience and make the ATS system more accessible across different environments, we have made the following modifications:

### Updated Dependency

We have replaced the `pdf2image` package with the `PyPDF2` package. This change eliminates the need for Poppler Windows, allowing the ATS system to run seamlessly on any system without special requirements.

## Installation Guide

Follow the steps below to set up and run the modified ATS system:

1. Clone the repository:
   ```bash
   git clone https://github.com/Namit-9504/Gemini-Ai-model.git
   ```

2. Navigate to the project directory:
   ```bash
   cd ats-system
   ```

3. Install project dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the ATS system:
   ```bash
   python main.py
   ```

## Additional Notes

- The `PyPDF2` package handles PDF processing without the need for Poppler Windows.
- Feel free to explore and customize the system based on your specific requirements.

If you have any questions or encounter issues during the setup, please don't hesitate to reach out for assistance.
```

