# ScheduleOptimizer — University Course Timetabling System

A desktop application and combinatorial optimization framework that solves the post-enrolment **University Course Timetabling Problem (UCTP)**[cite: 3]. Given a JSON teaching plan (groups, teachers, classrooms, subjects, and weekly hours), the system assigns lessons to conflict-free `(classroom, timeslot)` pairs using three distinct algorithmic engines, validates hard constraints, and exports ready-to-publish schedules to Excel and HTML[cite: 3].

> Developed as a Course Project at the Department of Computer Science and Cybersecurity, Lesya Ukrainka Volyn National University[cite: 3].

---

## Table of Contents

- [Key Features](#key-features)
- [How It Works](#how-it-works)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Input Data Format](#input-data-format)
- [Running the Project](#running-the-project)
- [Testing](#testing)
- [Benchmark](#benchmark)
- [Limitations](#limitations)
- [Roadmap](#roadmap)
- [License](#license)

---

## Key Features

- **Three optimization engines.** Compare a heuristic Greedy scheduler, an exact Branch-and-Bound solver, and a bipartite graph Hopcroft–Karp matching algorithm side by side[cite: 3].
- **Strict hard-constraint enforcement.** Guarantees no double-booked teachers, student groups, or classrooms, and strictly respects classroom seating capacities (`|group| <= capacity`)[cite: 3].
- **Interactive Tkinter GUI.** One-click JSON loading, algorithm execution, real-time progress bar, and formatted console schedule preview[cite: 3].
- **Automated conflict validator.** Independent post-scheduling verification module that audits generated timetables against all domain constraints[cite: 3].
- **Multi-format export.** Automatically generates timestamped `.xlsx` spreadsheets (`pandas` + `openpyxl`) and styled `.html` timetables (`Jinja2`) in the `results/` directory[cite: 2, 3].
- **Built-in datasets.** Includes synthetic and faculty-scale datasets (`simple.json`, `medium.json`, `complex.json`) for immediate benchmarking[cite: 2, 3].

---

## How It Works

```
JSON Input (groups, teachers, classrooms, subjects, teaching_plan)
       │
       ▼
ScheduleProblem Loader (scheduler.py) ──► Lesson Expansion (30 weekly slots: 5 days × 6 periods)
                                                   │
       ┌───────────────────────────────────────────┼───────────────────────────────────────────┐
       ▼                                           ▼                                           ▼
Greedy Engine                             Branch-and-Bound                           Hopcroft–Karp Engine
(priority sort + randomized slots)        (backtracking + upper-bound pruning)       (bipartite matching O(E√V) + filter)
       └───────────────────────────────────────────┼───────────────────────────────────────────┘
                                                   ▼
                                    Conflict Validator (utils/validator.py)
                                                   │
                                      ┌────────────┴────────────┐
                                      ▼                         ▼
                           Tkinter GUI Preview       Exporter (.xlsx & .html)
```

### Mathematical Model & Hard Constraints

The weekly grid consists of $\vert{}TS\vert{} = 30$ timeslots (5 days $\times$ 6 periods)[cite: 3]. The resource space is the Cartesian product $R = C \times TS$ (classrooms $\times$ timeslots)[cite: 3]. Each lesson instance $l_i = (s, t, g) \in L$ represents one weekly hour of subject $s$ taught by teacher $t$ to group $g$[cite: 3].

An injective partial mapping $f: L \to R$ is valid if and only if[cite: 3]:
1. **Teacher exclusivity:** No teacher is assigned to more than one classroom in the same timeslot[cite: 3].
2. **Group exclusivity:** No student group attends more than one lesson in the same timeslot[cite: 3].
3. **Classroom exclusivity:** Each $(c_j, ts_k)$ pair hosts at most one lesson[cite: 3].
4. **Capacity constraint:** $\text{size}(g) \le \text{capacity}(c_j)$[cite: 3].

### Algorithms

| Algorithm | Complexity | Implementation Details |
|---|---|---|
| **Greedy Scheduler** (`algorithms/greedy.py`) | $O(\Vert{}L\Vert{} \log \Vert{}L\Vert{} + \Vert{}L\Vert{} \cdot \Vert{}R\Vert{})$ | Sorts lessons by descending group size and weekly hours (`(-l.group.size, -l.subject.hours_per_week)`), shuffles available timeslots/classrooms to escape local optima, and assigns the first conflict-free resource using $O(1)$ set lookups[cite: 3]. |
| **Branch and Bound** (`algorithms/branch_and_bound.py`) | Exponential worst-case (time-bounded) | Recursive backtracking over prioritized lessons. Prunes search subtrees whenever `len(current) + remaining_lessons <= best_count` or when the execution time limit is reached[cite: 3]. |
| **Hopcroft–Karp** (`algorithms/hopcroft_karp_scheduler.py`) | $O(E\sqrt{V})$ | Constructs a bipartite graph $G = (L \cup R, E)$ based on classroom capacity, finds maximum cardinality matching via layered BFS and augmenting-path DFS, and applies a post-matching greedy filter to eliminate teacher/group timeslot collisions[cite: 3]. |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.9+ (developed and tested on Python 3.13)[cite: 2, 3] |
| GUI | `tkinter`, `ttk` (standard library)[cite: 3] |
| Data & Excel Export | `pandas`, `openpyxl`[cite: 3] |
| HTML Templating | `Jinja2`[cite: 3] |
| Core Data Structures | `collections.deque`, `typing`, native hash sets[cite: 3] |
| Testing | `unittest` (standard library)[cite: 3] |

---

## Project Structure

```
schedule_optimizer/
├── algorithms/
│   ├── branch_and_bound.py         # Exact backtracking solver with upper-bound pruning
│   ├── greedy.py                   # Priority-based greedy heuristic with slot randomization
│   └── hopcroft_karp_scheduler.py  # Bipartite graph maximum matching (BFS/DFS) + conflict filter
├── data/
│   ├── simple.json                 # Basic test dataset (20 lessons, 2 groups, 3 teachers, 4 rooms)
│   ├── medium.json                 # Faculty-level dataset (68–80 lessons, 4 groups, 8 teachers, 6 rooms)
│   └── complex.json                # High-load dataset (96–134 lessons, 5 groups, 12 teachers, 8 rooms)
├── results/                        # Auto-generated Excel (.xlsx) and HTML (.html) schedules
├── tests/
│   └── test_scheduler.py           # Automated unit and integration tests (8 test cases)
├── utils/
│   ├── exporter.py                 # Excel (pandas/openpyxl) and HTML (Jinja2) export utilities
│   └── validator.py                # Hard-constraint verification module
├── gui.py                          # Desktop GUI application entry point (Tkinter)
├── scheduler.py                    # Core domain models (Classroom, Teacher, Group, Subject, Lesson)
└── visualization.py                # Formatted console/log timetable renderer
```

---

## Getting Started

### Prerequisites

| Tool | Version |
|---|---|
| OS | macOS, Linux, or Windows 10/11[cite: 3] |
| Python | 3.9+ (3.13 recommended)[cite: 3] |
| `pip` | Latest |

### Installation

```bash
git clone [https://github.com/](https://github.com/)<your-username>/schedule_optimizer.git
cd schedule_optimizer

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate        # On Windows: .venv\Scripts\activate

# Install required dependencies
pip install pandas openpyxl jinja2
```

---

## Input Data Format

Input files are stored in JSON format (`data/*.json`) and require five top-level keys: `classrooms`, `teachers`, `groups`, `subjects`, and `teaching_plan`[cite: 2, 3].

```json
{
  "classrooms": [
    { "id": 1, "name": "Ауд. 101", "capacity": 30 }
  ],
  "teachers": [
    { "id": 1, "name": "Іванов І.І." }
  ],
  "groups": [
    { "id": 1, "name": "КН-31", "size": 25 }
  ],
  "subjects": [
    { "id": 1, "name": "Теорія алгоритмів", "hours_per_week": 2 }
  ],
  "teaching_plan": [
    { "subject_id": 1, "teacher_id": 1, "group_id": 1 }
  ]
}
```

---

## Running the Project

Launch the graphical interface from the project root[cite: 3]:

```bash
python3 gui.py
```

1. Click **«Вибрати JSON-файл»** and select a dataset from the `data/` folder (e.g., `data/complex.json`)[cite: 3].
2. Select an optimization algorithm[cite: 3]:
   - **«Жадібний алгоритм»** (Greedy)
   - **«Перебір з відсіченням»** (Branch and Bound)
   - **«Хопкрофт–Карп»** (Hopcroft–Karp)
3. Inspect the execution time, placement rate, validation status, and text timetable directly in the application log[cite: 3].
4. Find the exported files in `results/schedule_YYYYMMDD_HHMM.xlsx` and `results/schedule.html`[cite: 2, 3].

---

## Testing

Run the automated test suite using Python's built-in `unittest` runner[cite: 3]:

```bash
python3 -m unittest discover -s tests
```

The suite executes **8 unit tests** (~0.24s) covering[cite: 3]:
- JSON parsing and model instantiation (`test_load_from_json`)[cite: 3]
- Single-assignment capacity validation (`test_is_valid_assignment`)[cite: 3]
- Full-schedule conflict detection (`test_validate_schedule`)[cite: 3]
- All three scheduling algorithms (`test_greedy_schedule`, `test_branch_and_bound_schedule`, `test_hopcroft_karp_schedule`)[cite: 3]
- Excel and HTML export pipelines (`test_export_to_excel`, `test_export_to_html`)[cite: 3]

---

## Benchmark

Evaluated across three datasets of increasing constraint density on Python 3.13[cite: 3]:

| Dataset | Greedy (Time / Placed) | Branch & Bound (Time / Placed) | Hopcroft–Karp (Time / Placed) |
|---|---|---|---|
| **Simple** (`data/simple.json`) | `0.0002 s` / **100%** | `0.0010 s` / **100%** | `0.0004 s` / **100%** |
| **Medium** (`data/medium.json`) | `0.0006 s` / **98–100%** | `0.0059 s` / **100%** | `0.0015 s` / **80.0%** |
| **Complex** (`data/complex.json`) | `0.0013 s` / **94–100%** | `0.0013–8.0 s` / **99.3%** | `0.0028 s` / **69.4%** |

### Key Findings

- **Greedy Scheduler** delivers the best practical trade-off for university departments, achieving up to 100% placement in under `1.5 ms` by combining degree-based heuristic sorting with randomized slot exploration[cite: 3].
- **Branch and Bound** guarantees exact or near-exact solutions on small and medium instances, but requires time-bounding on heavily constrained inputs due to exponential tree growth[cite: 3].
- **Hopcroft–Karp** executes in polynomial time ($O(E\sqrt{V})$), but pure bipartite matching between `Lessons` and `(Classroom, TimeSlot)` cannot natively encode cross-edge mutex constraints (e.g., the same teacher or group assigned to different classrooms in the same timeslot). Post-matching conflict filtering reduces placement density on complex datasets to `69.4%`[cite: 3].

---

## Limitations

- **Hard constraints only.** Soft constraints (teacher day-off preferences, minimizing student gaps/"windows" between classes, building-to-building travel time) are not yet scored[cite: 3].
- **Single-group lessons.** Combined lectures for multiple student streams require manual grouping in the JSON input.
- **Bipartite model coupling.** The Hopcroft–Karp formulation models capacity constraints on edges but relies on a secondary greedy pass to resolve teacher/group timeslot collisions[cite: 3].

---

## Roadmap

- Hybrid solver combining Greedy initialization with Simulated Annealing / Tabu Search for local improvement[cite: 3].
- Soft-constraint penalty function (teacher time preferences, compact student schedules)[cite: 3].
- Web interface and REST API (FastAPI / Flask) for multi-user department access[cite: 3].
- Support for multi-group lecture streams and specialized room types (labs vs. lecture halls).

---

## License

Educational project developed by **Vadym Priadun** (Group KNIT-33, Lesya Ukrainka Volyn National University)[cite: 3]. Free to use and modify under the MIT License.