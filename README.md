# Simple Python APPIUM UI Automation Framework

A simple UI automation framework built with:
- **Python**: 3.10 - 3.12
- **pytest**: 8.3.0
- **APPIUM**: 2.6.0
- **CI**: GitHub Actions
- ENV: dynaconf

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](https://www.linkedin.com/in/dmytro-berezovskyi/)

## Features

- User-friendly UI automation framework.
- Built on popular Python libraries: pytest and APPIUM.
- Supports **iOS**, **Android**,
- Supports multiple environments: **stage**, **prod**.
- Generates **pytest reports** and **custom logs**.
- Test Data Management: Integrated with YAML files for test data storage and access.
- Logging
- Base functions: swipe, scroll, tap, click, type etc

## Getting Started

### Local Usage

1. Clone this repository:
   ```bash
   git clone <repository-url>
   ```
2. Install required dependencies:
   ```bash
   pip install poetry
   poetry shell
   poetry env info
   copy `Executable: path to virtual env` -> Add Interpreter -> Poetry Environment -> Existing environment -> add Executable -> Apply
   poetry install
   ```
   then specify your poetry env
