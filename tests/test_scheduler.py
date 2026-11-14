import unittest
import os
import json
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)
import shutil
from datetime import datetime
from scheduler import ScheduleProblem, Classroom, Teacher, Group, Subject, Lesson
from utils.validator import validate_schedule
from algorithms.greedy import greedy_schedule
from algorithms.branch_and_bound import branch_and_bound_schedule
from algorithms.hopcroft_karp_scheduler import hopcroft_karp_schedule
from utils.exporter import export_to_excel, export_to_html


class TestScheduleProblem(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        os.makedirs("tests/data", exist_ok=True)
        cls.test_json = "tests/data/test_input.json"
        
        test_data = {
            "classrooms": [
                {"id": 1, "capacity": 30, "name": "Ауд. 101"},
                {"id": 2, "capacity": 50, "name": "Ауд. 202"}
            ],
            "teachers": [
                {"id": 1, "name": "Іванов І.І."},
                {"id": 2, "name": "Петренко П.П."}
            ],
            "groups": [
                {"id": 1, "name": "ІПЗ-21", "size": 25},
                {"id": 2, "name": "КН-21", "size": 40}
            ],
            "subjects": [
                {"id": 1, "name": "Програмування", "hours_per_week": 2},
                {"id": 2, "name": "Математика", "hours_per_week": 1}
            ],
            "teaching_plan": [
                {"subject_id": 1, "teacher_id": 1, "groups": [1]},
                {"subject_id": 1, "teacher_id": 2, "groups": [2]},
                {"subject_id": 2, "teacher_id": 1, "groups": [1, 2]}
            ]
        }

        with open(cls.test_json, "w", encoding="utf-8") as f:
            json.dump(test_data, f, ensure_ascii=False, indent=2)


        os.makedirs("results", exist_ok=True)

    @classmethod
    def tearDownClass(cls):

        if os.path.exists("tests/data"):
            shutil.rmtree("tests/data")

        for file in os.listdir("results"):
            if file.startswith("schedule_"):
                os.remove(os.path.join("results", file))

    def setUp(self):
        self.problem = ScheduleProblem()
        self.problem.load_from_json(self.test_json)

    def test_load_from_json(self):
        self.assertEqual(len(self.problem.classrooms), 2)
        self.assertEqual(len(self.problem.teachers), 2)
        self.assertEqual(len(self.problem.groups), 2)
        self.assertEqual(len(self.problem.subjects), 2)
    
   
        self.assertEqual(len(self.problem.lessons), 6)

    def test_is_valid_assignment(self):
        lesson = self.problem.lessons[0]  
        small_room = self.problem.classrooms[0]  
        big_room = self.problem.classrooms[1]  

        self.assertTrue(self.problem.is_valid_assignment(lesson, small_room, (0, 0)))
        self.assertTrue(self.problem.is_valid_assignment(lesson, big_room, (0, 0)))


        big_group = Group(id=3, name="Тест", size=60)
        big_lesson = Lesson(self.problem.subjects[0], self.problem.teachers[0], big_group)
        
        self.assertFalse(self.problem.is_valid_assignment(big_lesson, small_room, (0, 0)))
        self.assertFalse(self.problem.is_valid_assignment(big_lesson, big_room, (0, 0)))

    def test_validate_schedule(self):
        schedule = {}

    
        lesson1 = self.problem.lessons[0]  
        lesson2 = Lesson(self.problem.subjects[1], self.problem.teachers[0], self.problem.groups[1]) 

        classroom = self.problem.classrooms[0]
        slot = (0, 0)

        schedule[(lesson1, classroom, slot)] = None
        schedule[(lesson2, classroom, slot)] = None

        self.assertFalse(validate_schedule(schedule, self.problem))

    def test_greedy_schedule(self):
        schedule = greedy_schedule(self.problem)
        self.assertTrue(validate_schedule(schedule, self.problem))
        self.assertGreaterEqual(len(schedule), 2) 

    def test_branch_and_bound_schedule(self):
        schedule = branch_and_bound_schedule(self.problem, time_limit_sec=10)
        self.assertTrue(validate_schedule(schedule, self.problem))
        placed = len(schedule)
        self.assertGreaterEqual(placed, 2)

    def test_hopcroft_karp_schedule(self):
        schedule = hopcroft_karp_schedule(self.problem)
        self.assertTrue(validate_schedule(schedule, self.problem))
        self.assertGreaterEqual(len(schedule), 1)

    def test_export_to_excel(self):
        schedule = greedy_schedule(self.problem)
        export_to_excel(schedule, self.problem)

        files = [f for f in os.listdir("results") if f.endswith(".xlsx")]
        self.assertGreater(len(files), 0)


        import pandas as pd
        df = pd.read_excel(os.path.join("results", files[0]))
        self.assertIn("Предмет", df.columns)
        self.assertIn("Група", df.columns)
        self.assertGreater(len(df), 0)

    def test_export_to_html(self):
        schedule = greedy_schedule(self.problem)
        export_to_html(schedule, self.problem)

        html_path = "results/schedule.html"
        self.assertTrue(os.path.exists(html_path))

        with open(html_path, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("<table", content)
            self.assertIn("Програмування", content) or self.assertIn("Математика", content)


if __name__ == "__main__":
    unittest.main(verbosity=2)