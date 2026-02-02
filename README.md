# Algorithms and Data Structures (MSCS532)

## Overview
This repository contains coursework and assignments for the Algorithms and Data Structures course (MSCS532) at the University of Cumberlands. The repository demonstrates implementations of various algorithms and data structures with comprehensive testing and performance analysis.

## Python Setup Instructions

### Requirements
- **Python Version**: 3.8 or higher (recommended: 3.12)
- **Operating Systems**: macOS and Linux

### Installation

#### macOS
**Using Homebrew** (recommended):
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3.12
brew install python@3.12

# Verify installation
python3 --version
```

#### Linux (Ubuntu/Debian)
```bash
# Update package list
sudo apt update

# Install Python 3.12
sudo apt install python3.12 python3.12-venv python3-pip

# Verify installation
python3.12 --version
```


### Setting Up Virtual Environment
```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate

# Install dependencies (if requirements.txt exists)
pip install -r requirements.txt
```

## Repository Structure

```
UC_MSCS532/
│
├── README.md                          # This file
│
├── Assignment1/                       # Insertion Sort Implementation
│   └── ...
│
└── Assignment2/                       # Sorting Algorithms Comparison
    └── ...
```