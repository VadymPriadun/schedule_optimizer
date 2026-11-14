import time
from scheduler import ScheduleProblem
from .greedy import greedy_schedule

def branch_and_bound_schedule(problem: ScheduleProblem, time_limit_sec=10.0):
    lessons = problem.lessons
    if not lessons:
        return {}

    if len(lessons) > 25:
        return greedy_schedule(problem)

    best = {}
    best_count = 0
    start_time = time.time()

    teacher_busy = {t.id: set() for t in problem.teachers}
    group_busy   = {g.id: set() for g in problem.groups}
    room_busy    = {c.id: set() for c in problem.classrooms}

    def backtrack(idx, current):
        nonlocal best, best_count, start_time

 
        if time.time() - start_time > time_limit_sec:
            return True 

        if idx == len(lessons):
            if len(current) > best_count:
                best_count = len(current)
                best = current.copy()
            return False

       
        if len(current) + (len(lessons) - idx) <= best_count:
            return False

        lesson = lessons[idx]


        for slot in problem.timeslots:
            for classroom in problem.classrooms:
                if not problem.is_valid_assignment(lesson, classroom, slot):
                    continue
                if (slot in teacher_busy[lesson.teacher.id] or
                    slot in group_busy[lesson.group.id] or
                    slot in room_busy[classroom.id]):
                    continue

               
                teacher_busy[lesson.teacher.id].add(slot)
                group_busy[lesson.group.id].add(slot)
                room_busy[classroom.id].add(slot)
                current[(lesson, classroom, slot)] = None

                should_stop = backtrack(idx + 1, current)
                if should_stop:
                    
                    del current[(lesson, classroom, slot)]
                    teacher_busy[lesson.teacher.id].remove(slot)
                    group_busy[lesson.group.id].remove(slot)
                    room_busy[classroom.id].remove(slot)
                    return True

                del current[(lesson, classroom, slot)]
                teacher_busy[lesson.teacher.id].remove(slot)
                group_busy[lesson.group.id].remove(slot)
                room_busy[classroom.id].remove(slot)

     
        return backtrack(idx + 1, current)

    try:
        backtrack(0, {})
    except RecursionError:
        pass 

    return best