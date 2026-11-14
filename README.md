# ScheduleOptimizer --- University Course Timetabling System

A desktop application and combinatorial optimization framework that
solves the post-enrolment **University Course Timetabling Problem
(UCTP)**. Given a JSON teaching plan (groups, teachers, classrooms,
subjects, and weekly hours), the system assigns lessons to conflict-free
`(classroom, timeslot)` pairs using three distinct algorithmic engines,
validates hard constraints, and exports schedules to Excel and HTML.

> Developed as a Course Project at the Department of Computer Science
> and Cybersecurity, Lesya Ukrainka Volyn National University.

------------------------------------------------------------------------

## Table of Contents

-   [Key Features](#key-features)
-   [How It Works](#how-it-works)
-   [Tech Stack](#tech-stack)
-   [Project Structure](#project-structure)
-   [Getting Started](#getting-started)
-   [Input Data Format](#input-data-format)
-   [Running the Project](#running-the-project)
-   [Testing](#testing)
-   [Benchmark](#benchmark)
-   [Limitations](#limitations)
-   [Roadmap](#roadmap)
-   [License](#license)

------------------------------------------------------------------------

## Key Features

-   **Three optimization engines.** Compare a heuristic Greedy
    scheduler, an exact Branch-and-Bound solver, and a bipartite graph
    Hopcroft--Karp matching algorithm side by side.
-   **Hard-constraint enforcement.** Prevents double-booked teachers,
    student groups, and classrooms, and respects classroom seating
    capacities (`group size <= classroom capacity`).
-   **Interactive Tkinter GUI.** JSON loading, algorithm execution,
    progress display, and formatted schedule preview.
-   **Automated conflict validator.** Independently verifies generated
    timetables against the scheduling constraints.
-   **Multi-format export.** Generates timestamped `.xlsx` spreadsheets
    (`pandas` + `openpyxl`) and styled `.html` timetables (`Jinja2`) in
    the `results/` directory.
-   **Built-in datasets.** Includes `simple.json`, `medium.json`, and
    `complex.json` for testing and benchmarking.

------------------------------------------------------------------------

## How It Works

``` text
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

The weekly grid consists of (\|TS\| = 30) timeslots (5 days × 6
periods). The resource space is the Cartesian product (R = C
`\times `{=tex}TS) (classrooms × timeslots). Each lesson instance (l_i =
(s, t, g) `\in `{=tex}L) represents one weekly hour of subject (s),
taught by teacher (t) to group (g).

A partial assignment (f: L `\to `{=tex}R) is valid when all of the
following constraints are satisfied:

1.  **Teacher exclusivity:** A teacher cannot teach more than one lesson
    in the same timeslot.
2.  **Group exclusivity:** A student group cannot attend more than one
    lesson in the same timeslot.
3.  **Classroom exclusivity:** A classroom can host at most one lesson
    in a timeslot.
4.  **Capacity constraint:** (`\text{size}`{=tex}(g)
    `\le `{=tex}`\text{capacity}`{=tex}(c)).

### Algorithms

  --------------------------------------------------------------------------------------------
  Algorithm                                   Complexity               Implementation Details
  ------------------------------------------- ------------------------ -----------------------
  **Greedy Scheduler**                        (O(                      L
  (`algorithms/greedy.py`)                                             

  **Branch and Bound**                        Exponential worst-case;  Uses recursive
  (`algorithms/branch_and_bound.py`)          time-bounded             backtracking over
                                                                       prioritized lessons.
                                                                       Prunes branches when
                                                                       the best possible
                                                                       remaining assignment
                                                                       cannot improve the
                                                                       current solution or
                                                                       when the execution time
                                                                       limit is reached.

  **Hopcroft--Karp**                          (O(E`\sqrt{V}`{=tex}))   Builds a bipartite
  (`algorithms/hopcroft_karp_scheduler.py`)   for matching             graph based on
                                                                       classroom capacity,
                                                                       finds a maximum
                                                                       matching using BFS and
                                                                       DFS, and applies a
                                                                       post-matching filter
                                                                       for teacher/group
                                                                       timeslot conflicts.
  --------------------------------------------------------------------------------------------

------------------------------------------------------------------------

## Tech Stack

  -----------------------------------------------------------------------
  Layer                               Technology
  ----------------------------------- -----------------------------------
  Language                            Python 3.9+ (Python 3.13
                                      recommended)

  GUI                                 `tkinter`, `ttk` (standard library)

  Data & Excel Export                 `pandas`, `openpyxl`

  HTML Templating                     `Jinja2`

  Core Data Structures                `collections.deque`, `typing`,
                                      native hash sets

  Testing                             `unittest` (standard library)
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## Project Structure

``` text
schedule_optimizer/
├── algorithms/
│   ├── branch_and_bound.py         # Exact backtracking solver with upper-bound pruning
│   ├── greedy.py                   # Priority-based greedy heuristic with slot randomization
│   └── hopcroft_karp_scheduler.py  # Bipartite matching (BFS/DFS) and conflict filter
├── data/
│   ├── simple.json                 # Basic test dataset
│   ├── medium.json                 # Medium-size dataset
│   └── complex.json                # High-load dataset
├── results/                        # Generated Excel and HTML schedules (not tracked by Git)
├── tests/
│   └── test_scheduler.py           # Automated unit and integration tests
├── utils/
│   ├── exporter.py                 # Excel and HTML export utilities
│   └── validator.py                # Hard-constraint verification module
├── .gitignore
├── requirements.txt                # Python package dependencies
├── gui.py                          # Desktop GUI application entry point
├── scheduler.py                    # Core domain models and scheduling logic
└── visualization.py                # Formatted console/log timetable renderer
```

------------------------------------------------------------------------

## Getting Started

### Prerequisites

  Tool               Version
  ------------------ --------------------------------
  Operating System   macOS, Linux, or Windows 10/11
  Python             3.9+ (Python 3.13 recommended)
  `pip`              Recent version

### Installation

1.  Clone the repository and open its directory:

    ``` bash
    git clone https://github.com/<your-username>/schedule_optimizer.git
    cd schedule_optimizer
    ```

2.  Create and activate a virtual environment:

    **macOS / Linux**

    ``` bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

    **Windows (PowerShell)**

    ``` powershell
    py -m venv .venv
    .venv\Scripts\Activate.ps1
    ```

3.  Install the project dependencies:

    ``` bash
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    ```

    The `requirements.txt` file should contain:

    ``` text
    pandas
    openpyxl
    jinja2
    ```

    These packages are required for Excel data processing/export and
    HTML timetable generation.

------------------------------------------------------------------------

## Input Data Format

Input files are stored in JSON format in the `data/` directory and
require five top-level keys: `classrooms`, `teachers`, `groups`,
`subjects`, and `teaching_plan`.

``` json
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

------------------------------------------------------------------------

## Running the Project

Activate the virtual environment, if it is not already active, and
launch the graphical interface from the project root:

``` bash
python gui.py
```

1.  Click **«Вибрати JSON-файл»** and select a dataset from the `data/`
    directory (for example, `data/complex.json`).
2.  Select an optimization algorithm:
    -   **«Жадібний алгоритм»** (Greedy)
    -   **«Перебір з відсіченням»** (Branch and Bound)
    -   **«Хопкрофт--Карп»** (Hopcroft--Karp)
3.  Inspect the execution time, placement rate, validation status, and
    timetable in the application log.
4.  Find generated files in the `results/` directory.

Generated schedule files are local outputs and are excluded from version
control by `.gitignore`. They are created when the application or export
functions run.

------------------------------------------------------------------------

## Testing

Run the automated test suite from the project root with the virtual
environment activated:

``` bash
python -m unittest discover -s tests -v
```

The `unittest` framework is included with Python, so it does not need to
be installed separately. The tests cover:

-   JSON parsing and model instantiation (`test_load_from_json`)
-   Assignment capacity validation (`test_is_valid_assignment`)
-   Full-schedule conflict detection (`test_validate_schedule`)
-   The three scheduling algorithms (`test_greedy_schedule`,
    `test_branch_and_bound_schedule`, `test_hopcroft_karp_schedule`)
-   Excel and HTML export pipelines (`test_export_to_excel`,
    `test_export_to_html`)

The export tests require the third-party dependencies listed in
`requirements.txt`. If you see
`ModuleNotFoundError: No module named 'pandas'`, make sure the virtual
environment is activated and install the dependencies:

``` bash
python -m pip install -r requirements.txt
```

------------------------------------------------------------------------

## Benchmark

Evaluated across three datasets of increasing constraint density on
Python 3.13:

  -----------------------------------------------------------------------------
  Dataset                 Greedy (Time /    Branch & Bound    Hopcroft--Karp
                          Placed)           (Time / Placed)   (Time / Placed)
  ----------------------- ----------------- ----------------- -----------------
  **Simple**              `0.0002 s` /      `0.0010 s` /      `0.0004 s` /
  (`data/simple.json`)    **100%**          **100%**          **100%**

  **Medium**              `0.0006 s` /      `0.0059 s` /      `0.0015 s` /
  (`data/medium.json`)    **98--100%**      **100%**          **80.0%**

  **Complex**             `0.0013 s` /      `0.0013–8.0 s` /  `0.0028 s` /
  (`data/complex.json`)   **94--100%**      **99.3%**         **69.4%**
  -----------------------------------------------------------------------------

### Key Findings

-   **Greedy Scheduler** delivers a strong practical trade-off for these
    datasets, achieving up to 100% placement in under `1.5 ms` through
    heuristic sorting and randomized slot exploration.
-   **Branch and Bound** can find exact or near-exact solutions on small
    and medium instances, but requires a time limit on heavily
    constrained inputs because its search tree can grow exponentially.
-   **Hopcroft--Karp** runs in polynomial time for the matching stage,
    but the bipartite model does not directly encode cross-edge
    constraints such as teacher/group collisions in the same timeslot.
    The post-matching conflict filter can therefore reduce placement
    density.

------------------------------------------------------------------------

## Limitations

-   **Hard constraints only.** Soft constraints (teacher day-off
    preferences, minimizing student gaps/"windows" between classes, and
    building-to-building travel time) are not currently scored.
-   **Single-group lessons.** Combined lectures for multiple student
    streams require manual grouping in the JSON input.
-   **Bipartite model coupling.** The Hopcroft--Karp formulation models
    classroom capacity on graph edges and relies on a secondary greedy
    pass to resolve teacher/group timeslot collisions.

------------------------------------------------------------------------

## Roadmap

-   Hybrid solver combining Greedy initialization with Simulated
    Annealing / Tabu Search for local improvement.
-   Soft-constraint penalty function (teacher time preferences and
    compact student schedules).
-   Web interface and REST API (FastAPI / Flask) for multi-user
    department access.
-   Support for multi-group lecture streams and specialized room types
    (labs vs. lecture halls).

------------------------------------------------------------------------

## License

Educational project developed by **Vadym Priadun** (Lesya Ukrainka Volyn
National University). Free to use and modify under the MIT License.
