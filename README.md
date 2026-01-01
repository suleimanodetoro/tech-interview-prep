## Getting Started :)

### Prerequisites
- Git installed on your machine
- Python 3.8+ (or Java JDK 11+, etc depending on your language)
- A code editor (VS Code, PyCharm, IntelliJ, etc.)

### Clone the Repository
```bash
# Clone the repo
git clone https://github.com/suleimanodetoro/tech-interview-prep.git

# Navigate to the directory
cd tech-interview-prep

# (Optional) Create a virtual environment for Python
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# (Optional) Install any dependencies
pip install -r requirements.txt  # if you have one
```

### Repository Structure

Once cloned, you'll see:
- `dsa/` - All DSA solutions organized by topic
- `system-design/` - System design notes and case studies
- `resources/` - Additional learning materials

### How to Use This Repo

1. **Browse by Topic**: Navigate to specific folders (e.g., `dsa/arrays/`)
2. **Read Solutions**: Each problem has a `.md` file with explanation and a code file
3. **Run Code**: Execute solutions directly:
```bash
   python dsa/arrays/two-sum.py
```
4. **Add Your Own**: Follow the existing structure to add new solutions

### Making Changes
```bash
# Create a new branch for your work
git checkout -b solving-new-problems

# After solving problems, commit your work
git add .
git commit -m "Add: solved merge intervals problem"
git push origin solving-new-problems
```