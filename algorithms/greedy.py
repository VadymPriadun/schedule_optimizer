import random
from typing import Dict
from scheduler import ScheduleProblem, Lesson, Classroom, TimeSlot

def greedy_schedule(problem: ScheduleProblem) -> Dict[tuple, None]:
    schedule = {}
    lessons = sorted(problem.lessons, key=lambda l: (-l.group.size, -l.subject.hours_per_week))

    teacher_busy = {t.id: set() for t in problem.teachers}
    group_busy   = {g.id: set() for g in problem.groups}
    room_busy    = {c.id: set() for c in problem.classrooms}

    for lesson in lessons:
        random.shuffle(problem.timeslots)
        placed = False
        for slot in problem.timeslots:
            random.shuffle(problem.classrooms)
            for classroom in problem.classrooms:
                if not problem.is_valid_assignment(lesson, classroom, slot):
                    continue
                if (slot in teacher_busy[lesson.teacher.id] or
                    slot in group_busy[lesson.group.id] or
                    slot in room_busy[classroom.id]):
                    continue

                schedule[(lesson, classroom, slot)] = None
                teacher_busy[lesson.teacher.id].add(slot)
                group_busy[lesson.group.id].add(slot)
                room_busy[classroom.id].add(slot)
                placed = True
                break
            if placed:
                break
    return schedule