
# ScheduleOptimizer — University Course Timetabling System

A desktop application and combinatorial optimization framework that solves the post-enrolment **University Course Timetabling Problem (UCTP)**. Given a JSON teaching plan (groups, teachers, classrooms, subjects, and weekly hours), the system assigns lessons to conflict-free `(classroom, timeslot)` pairs using three distinct algorithmic engines, validates hard constraints, and exports ready-to-use schedules to Excel and HTML.

> Developed as a Course Project at the Department of Computer Science and Cybersecurity, Lesya Ukrainka Volyn National University.

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

- **Three optimization engines.** Compare a heuristic Greedy scheduler, an exact Branch-and-Bound solver, and a bipartite graph Hopcroft–Karp matching algorithm side by side.
- **Strict hard-constraint enforcement.** Prevents double-booked teachers, student groups, and classrooms, and respects classroom seating capacities (`group size <= classroom capacity`).
- **Interactive Tkinter GUI.** One-click JSON loading, algorithm execution, progress display, and formatted schedule preview.
- **Automated conflict validator.** Independent post-scheduling verification module that audits generated timetables against all domain constraints.
- **Multi-format export.** Automatically generates timestamped `.xlsx` spreadsheets (`pandas` + `openpyxl`) and styled `.html` timetables (`Jinja2`) in the `results/` directory.
- **Built-in datasets.** Includes synthetic and faculty-scale datasets (`simple.json`, `medium.json`, `complex.json`) for testing and benchmarking.

---

## How It Works

```text
JSON Input (groups, teachers, classrooms, subjects, teaching_plan)
        |
        v
ScheduleProblem Loader (scheduler.py)
        |
        v
Lesson Expansion (30 weekly slots: 5 days x 6 periods)
        |
        +----------------------+-------------------------+
        |                      |                         |
        v                      v                         v
   Greedy Engine       Branch-and-Bound          Hopcroft–Karp Engine
(priority sort and    (backtracking and          (bipartite matching
 slot randomization)   upper-bound pruning)       plus conflict filter)
        |                      |                         |
        +----------------------+-------------------------+
                               |
                               v
                Conflict Validator (utils/validator.py)
                               |
                  +------------+------------+
                  |                         |
                  v                         v
             Tkinter GUI              Exporter (.xlsx/.html)
```

### Mathematical Model & Hard Constraints

The weekly grid consists of:

- `|TS| = 30` timeslots (5 days × 6 periods).
- The resource space is the Cartesian product `R = C × TS` (classrooms × timeslots).
- Each lesson instance `l_i = (s, t, g) ∈ L` represents one weekly hour of subject `s`, taught by teacher `t` to group `g`.

A partial assignment `f: L → R` is valid if and only if all the following constraints are satisfied:

1. **Teacher exclusivity:** No teacher is assigned to more than one classroom in the same timeslot.
2. **Group exclusivity:** No student group attends more than one lesson in the same timeslot.
3. **Classroom exclusivity:** Each classroom can host at most one lesson in a timeslot.
4. **Capacity constraint:** `size(g) <= capacity(c)`.

### Algorithms

| Algorithm | Complexity | Implementation Details |
|---|---|---|
| **Greedy Scheduler** (`algorithms/greedy.py`) | `O(|L| log |L| + |L| · |R|)` | Sorts lessons by descending group size and weekly hours, shuffles available timeslots and classrooms to escape local optima, and assigns the first conflict-free resource using set lookups. |
| **Branch and Bound** (`algorithms/branch_and_bound.py`) | Exponential worst-case (time-bounded) | Recursive backtracking over prioritized lessons. Prunes search subtrees whenever the best possible remaining assignment cannot improve the current solution or when the execution time limit is reached. |
| **Hopcroft–Karp** (`algorithms/hopcroft_karp_scheduler.py`) | `O(E√V)` for matching | Constructs a bipartite graph based on classroom capacity, finds maximum cardinality matching via layered BFS and augmenting-path DFS, and applies a post-matching greedy filter to eliminate teacher/group timeslot collisions. |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.9+ (Python 3.13 recommended) |
| GUI | `tkinter`, `ttk` (standard library) |
| Data & Excel Export | `pandas`, `openpyxl` |
| HTML Templating | `Jinja2` |
| Core Data Structures | `collections.deque`, `typing`, native hash sets |
| Testing | `unittest` (standard library) |

---

## Project Structure

```text
schedule_optimizer/
├── algorithms/
│   ├── branch_and_bound.py         # Exact backtracking solver with upper-bound pruning
│   ├── greedy.py                   # Priority-based greedy heuristic with slot randomization
│   └── hopcroft_karp_scheduler.py  # Bipartite matching (BFS/DFS) + conflict filter
├── data/
│   ├── simple.json                 # Basic test dataset
│   ├── medium.json                 # Faculty-level dataset
│   └── complex.json                # High-load dataset
├── results/                        # Generated Excel and HTML schedules (not tracked by Git)
├── tests/
│   ├── results/                    # Generated test outputs (not tracked by Git)
│   └── test_scheduler.py           # Automated unit and integration tests
├── utils/
│   ├── exporter.py                 # Excel and HTML export utilities
│   └── validator.py                # Hard-constraint verification module
├── .gitignore
├── requirements.txt                # Python package dependencies
├── gui.py                          # Desktop GUI application entry point (Tkinter)
├── scheduler.py                    # Core domain models and scheduling logic
└── visualization.py                # Formatted console/log timetable renderer
```

---

## Getting Started

### Prerequisites

| Tool | Version |
|---|---|
| Operating System | macOS, Linux, or Windows 10/11 |
| Python | 3.9+ (Python 3.13 recommended) |
| `pip` | Latest version |

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/<your-username>/schedule_optimizer.git
cd schedule_optimizer
```

**2. Create and activate a virtual environment**

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows (PowerShell):

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

**3. Install dependencies**

Update pip and install the required packages:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

The `requirements.txt` file should contain:

```text
pandas
openpyxl
jinja2
```

These dependencies are required for Excel data processing/export and HTML timetable generation.

---

## Input Data Format

Input files are stored in JSON format in the `data/` directory and require five top-level keys:

- `classrooms`
- `teachers`
- `groups`
- `subjects`
- `teaching_plan`

Example:

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

Activate the virtual environment, if it is not already active, and launch the graphical interface from the project root:

```bash
python gui.py
```

1. Click **«Вибрати JSON-файл»** and select a dataset from the `data/` directory (e.g., `data/complex.json`).
2. Select an optimization algorithm:
   - **«Жадібний алгоритм»** (Greedy)
   - **«Перебір з відсіченням»** (Branch and Bound)
   - **«Хопкрофт–Карп»** (Hopcroft–Karp)
3. Inspect the execution time, placement rate, validation status, and timetable directly in the application log.
4. Find the exported files in the `results/` directory.

Generated schedule files are local outputs and are excluded from version control by `.gitignore`. They are created automatically when the application or export functions run.

---

## Testing

Run the automated test suite using Python's built-in `unittest` framework.

Make sure the virtual environment is activated:

```bash
python -m unittest discover -s tests -v
```

The suite includes **8 unit tests** covering:

- JSON parsing and model instantiation (`test_load_from_json`).
- Single-assignment capacity validation (`test_is_valid_assignment`).
- Full-schedule conflict detection (`test_validate_schedule`).
- All three scheduling algorithms:
  - `test_greedy_schedule`
  - `test_branch_and_bound_schedule`
  - `test_hopcroft_karp_schedule`
- Excel and HTML export pipelines:
  - `test_export_to_excel`
  - `test_export_to_html`

The `unittest` framework is included with Python and does not need to be installed separately.

The export tests require the third-party dependencies listed in `requirements.txt`.

If you encounter the following error:

```text
ModuleNotFoundError: No module named 'pandas'
```

Make sure that the virtual environment is activated and install the dependencies:

```bash
python -m pip install -r requirements.txt
```

---

## Benchmark

Evaluated across three datasets of increasing constraint density on Python 3.13:

| Dataset | Greedy (Time / Placed) | Branch & Bound (Time / Placed) | Hopcroft–Karp (Time / Placed) |
|---|---|---|---|
| **Simple** (`data/simple.json`) | `0.0002 s` / **100%** | `0.0010 s` / **100%** | `0.0004 s` / **100%** |
| **Medium** (`data/medium.json`) | `0.0006 s` / **98–100%** | `0.0059 s` / **100%** | `0.0015 s` / **80.0%** |
| **Complex** (`data/complex.json`) | `0.0013 s` / **94–100%** | `0.0013–8.0 s` / **99.3%** | `0.0028 s` / **69.4%** |

### Key Findings

- **Greedy Scheduler** delivers the best practical trade-off for university departments, achieving up to 100% placement in under `1.5 ms` by combining heuristic sorting with randomized slot exploration.
- **Branch and Bound** finds exact or near-exact solutions on small and medium instances, but requires time-bounding on heavily constrained inputs due to exponential search tree growth.
- **Hopcroft–Karp** executes in polynomial time (`O(E√V)`), but pure bipartite matching between `Lessons` and `(Classroom, TimeSlot)` cannot natively encode cross-edge mutex constraints (e.g., the same teacher or group assigned to different classrooms in the same timeslot). Post-matching conflict filtering reduces placement density on complex datasets to `69.4%`.

---

## Limitations

- **Hard constraints only.** Soft constraints (teacher day-off preferences, minimizing student gaps/"windows" between classes, and building-to-building travel time) are not yet scored.
- **Single-group lessons.** Combined lectures for multiple student streams require manual grouping in the JSON input.
- **Bipartite model coupling.** The Hopcroft–Karp formulation models capacity constraints on edges but relies on a secondary greedy pass to resolve teacher/group timeslot collisions.

---

## Roadmap

- Hybrid solver combining Greedy initialization with Simulated Annealing / Tabu Search for local improvement.
- Soft-constraint penalty function (teacher time preferences and compact student schedules).
- Web interface and REST API (FastAPI / Flask) for multi-user department access.
- Support for multi-group lecture streams and specialized room types (labs vs. lecture halls).

---

## License

Educational project developed by **Vadym Priadun** (Lesya Ukrainka Volyn National University). Free to use and modify under the MIT License.
