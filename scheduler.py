from typing import List, Tuple, Dict
import json

class Classroom:
    def __init__(self, id: int, capacity: int, name: str = ""):
        self.id = id
        self.capacity = capacity
        self.name = name or f"Ауд. {id}"

class Teacher:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

class Group:
    def __init__(self, id: int, name: str, size: int):
        self.id = id
        self.name = name
        self.size = size

class Subject:
    def __init__(self, id: int, name: str, hours_per_week: int):
        self.id = id
        self.name = name
        self.hours_per_week = hours_per_week

class Lesson:
    def __init__(self, subject: Subject, teacher: Teacher, group: Group):
        self.subject = subject
        self.teacher = teacher
        self.group = group
        self.id = f"L{subject.id}_{teacher.id}_{group.id}"

    def __repr__(self):
        return f"{self.subject.name} ({self.teacher.name} → {self.group.name})"

TimeSlot = Tuple[int, int]  # (день 0–4, пара 0–5)

class ScheduleProblem:
    def __init__(self):
        self.classrooms: List[Classroom] = []
        self.teachers: List[Teacher] = []
        self.groups: List[Group] = []
        self.subjects: List[Subject] = []
        self.lessons: List[Lesson] = []
        self.timeslots: List[TimeSlot] = [(d, p) for d in range(5) for p in range(6)]

    def load_from_json(self, path: str = "data/input.json"):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.classrooms = [Classroom(**c) for c in data["classrooms"]]
        self.teachers   = [Teacher(**t) for t in data["teachers"]]
        self.groups     = [Group(**g) for g in data["groups"]]
        self.subjects   = [Subject(**s) for s in data["subjects"]]

        self.lessons.clear()
        for plan in data["teaching_plan"]:
            subject = next(s for s in self.subjects if s.id == plan["subject_id"])
            teacher = next(t for t in self.teachers if t.id == plan["teacher_id"])
            for group_id in plan["groups"]:
                group = next(g for g in self.groups if g.id == group_id)
                for _ in range(subject.hours_per_week):
                    self.lessons.append(Lesson(subject, teacher, group))

    def is_valid_assignment(self, lesson: Lesson, classroom: Classroom, slot: TimeSlot) -> bool:
        return classroom.capacity >= lesson.group.size