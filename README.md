# 🚀 Tech Interview Prep

My personal repository documenting solutions to Data Structures & Algorithms problems and System Design case studies. This repo serves as both a learning journal and quick reference guide.

## 📊 Progress Tracker

### DSA Problems Solved: 1/150
- **Easy:** 3
- **Medium:** 0
- **Hard:** 0

### System Designs Completed: 0

Last Updated: January 2, 2026

---

## 🗂️ Repository Structure

```
tech-interview-prep/
├── dsa/
│   └── arrays_and_hashing/
│       └── contains-any-duplicate/
│           ├── contains-duplicate.md
│           └── contains-duplicate.py
└── README.md
```

---

## 🎯 Problems Solved

### Arrays & Hashing
- ✅ [Contains Duplicate](dsa/arrays_and_hashing/contains-any-duplicate/contains-duplicate.md) - Easy

### Coming Soon
- Two Sum
- Valid Anagram
- Group Anagrams
- Top K Frequent Elements

---

## 🚀 Getting Started

### Prerequisites
- Git installed on your machine
- Python 3.8+ (or Java JDK 11+, depending on your language)
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
- Each topic has its own folder (e.g., `arrays_and_hashing/`)
- Each problem has its own subfolder with `.md` notes and `.py` code

### How to Use This Repo

1. **Browse by Topic**: Navigate to specific folders
   ```bash
   cd dsa/arrays_and_hashing/
   ```

2. **Read Solutions**: Each problem has a detailed `.md` file with:
   - Problem statement
   - Multiple approaches
   - Complexity analysis
   - Key learnings

3. **Run Code**: Execute solutions directly:
   ```bash
   python3 dsa/arrays_and_hashing/contains-any-duplicate/contains-duplicate.py
   ```

4. **Add Your Own**: Follow the existing structure to add new solutions
   ```bash
   mkdir -p dsa/arrays_and_hashing/two-sum
   touch dsa/arrays_and_hashing/two-sum/two-sum.md
   touch dsa/arrays_and_hashing/two-sum/two-sum.py
   ```

### Making Changes

```bash
# Check current status
git status

# Add your changes
git add .

# Commit with a clear message
git commit -m "Add: Two Sum solution with hash map approach"

# Push to GitHub
git push origin main
```

---

## 📝 Solution Format

Each DSA problem follows this structure:

### Markdown File (`.md`)
- **Problem Statement** - Clear description with examples
- **Thought Process** - Initial approach and reasoning
- **Multiple Solutions** - Brute force, optimal, and alternatives
- **Complexity Analysis** - Time and space for each approach
- **Walkthroughs** - Step-by-step execution traces
- **Key Learnings** - Patterns and takeaways
- **Related Problems** - Similar questions to practice
- **Common Mistakes** - Pitfalls to avoid

### Code File (`.py`)
- Clean, commented implementation
- Multiple approaches in separate functions
- Test cases in `if __name__ == "__main__":` block
- Type hints for clarity

---

## 🛠️ Languages Used
- Primary: Python 3.11+
- Secondary: (Coming soon - Java, C++)

---

## 🎓 Learning Resources

### Books
- *Cracking the Coding Interview* by Gayle Laakmann McDowell
- *Designing Data-Intensive Applications* by Martin Kleppmann
- *System Design Interview* by Alex Xu

### Online Platforms
- LeetCode
- NeetCode
- System Design Primer (GitHub)

### Helpful Links
- [Big-O Cheat Sheet](https://www.bigocheatsheet.com/)
- [Visualizing Data Structures](https://visualgo.net/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)

---

## 📈 Study Plan

### Current Focus
- Building strong foundations in arrays and hashing
- Understanding time-space complexity trade-offs
- Recognizing common patterns

### Weekly Goals
- Solve 5-10 DSA problems
- Document learnings thoroughly
- Review and optimize previous solutions

---

## 💡 Problem-Solving Patterns

Key patterns I'm learning:
1. **Hash Set/Map** - Tracking "seen" elements (Contains Duplicate, Two Sum)
2. **Two Pointers** - Sorted array problems, palindromes
3. **Sliding Window** - Substring/subarray problems
4. **Fast & Slow Pointers** - Cycle detection
5. **Modified Binary Search** - Rotated arrays
6. **Top K Elements** - Heap usage
7. **Backtracking** - Permutations, combinations
8. **Dynamic Programming** - Overlapping subproblems

---

## 🏷️ Problem Categories

### Planned Topics
- ✅ Arrays & Hashing (1 problem)
- ⏳ Two Pointers
- ⏳ Sliding Window
- ⏳ Stack
- ⏳ Binary Search
- ⏳ Linked Lists
- ⏳ Trees
- ⏳ Tries
- ⏳ Heap / Priority Queue
- ⏳ Backtracking
- ⏳ Graphs
- ⏳ Dynamic Programming
- ⏳ Greedy
- ⏳ Intervals
- ⏳ Math & Geometry
- ⏳ Bit Manipulation

---

## 📋 Quick Commands

```bash
# Keep your local repo up to date
git pull origin main

# View your changes
git status
git diff

# Add a new solution
git add dsa/arrays_and_hashing/new-problem/
git commit -m "Add: new problem solution"
git push origin main

# Create a new branch for practice
git checkout -b week-1-practice

# Switch back to main
git checkout main
```

---

## 🤝 Contributing

This is primarily a personal learning repository, but feedback is welcome!

- Feel free to open issues for incorrect solutions or suggestions
- PRs for optimizations are appreciated
- Please include complexity analysis with any code suggestions

---

## 📫 Contact

- GitHub: [@suleimanodetoro](https://github.com/suleimanodetoro)
- LinkedIn: [\[Profile\]](https://www.linkedin.com/in/suleiman-odetoro/)
- Email: hey@suleimanodetoro.com

---

## ⭐ Acknowledgments

Thanks to the following resources that have been invaluable in my preparation:
- NeetCode for problem patterns and explanations
- LeetCode community for diverse solution approaches
- The tech community for support and motivation

---

## 📌 Notes

- This repository represents my learning journey
- Solutions may evolve as I discover better approaches
- Feedback and suggestions are always welcome!
- All solutions are tested and include complexity analysis

---

**Last Updated:** January 3, 2026  
**Current Streak:** 3 day 🔥