# MSCS532_Assignment1: Getting Started

I have set up the Python development environment and Visual Studio Code before. This document served as a prove and demonstrate on how I set up and implement the Insertion Sort algorithm.

##  Install Python

### Using Homebrew (macOS/Linux)

I'm using macOS/Linux. Below are the commands I used:

1. **Install Homebrew** (if you haven't already):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Install the latest version of Python**:
   ```bash
   brew install python
   ```

3. **To install a specific version** (e.g., Python 3.12):
   ```bash
   brew install python@3.12
   ```


### Alternative: Direct Download

If you prefer not to use Homebrew, you can download Python directly from the [official website](https://www.python.org/downloads). When running the installer, be sure to check the option **'Add Python to PATH'**.

---

## Install Visual Studio Code (VS Code)

### Using Homebrew (macOS)

Homebrew is like Linux's package manager. I also download VSCode with Homebrew:

1. **Install VS Code using Homebrew**:
   ```bash
   brew install --cask visual-studio-code
   ```

### Alternative: Direct Download

You can also download VS Code for Windows, macOS, or Linux directly from their website: https://code.visualstudio.com/


---

## GitHub Account

* Github: https://github.com/SammySheu
* Repo page: ![Image](./Screenshot%202026-01-16%20at%209.33.52 PM.png)


## Git Commands I used

### `git add`

```bash
# Add a specific file
git add insertion_sort.py

```

### `git commit`

Saves your staged changes to the local repository with a descriptive message:

```bash
# Commit with a message
git commit -m "feat: add insertion sort"
```

### `git push`

Uploads your local commits to the remote repository on GitHub:

```bash
# Push for the first time and set upstream
git push -u origin main
```

## Running the Program

To run the insertion sort program:

```bash
python3 insertion_sort.py
```

## Testing the script

```bash
python3 test_insertion.py
```


## Resources

- [Python Official Website](https://www.python.org/downloads)
- [Visual Studio Code](https://code.visualstudio.com/)
- [GitHub](https://github.com/)
- [Homebrew](https://brew.sh/)
- [Git Documentation](https://git-scm.com/doc)
- [Insertion Sort Algorithm - GeeksforGeeks](https://www.geeksforgeeks.org/dsa/insertion-sort-algorithm/)
- [Bubble Sort - GeeksforGeeks](https://www.geeksforgeeks.org/dsa/bubble-sort-algorithm/)
---

