from scheduler import TimeSlot

def validate_schedule(schedule, problem):
    teacher_busy = {}
    group_busy = {}
    room_busy = {}

    for (lesson, classroom, slot) in schedule:
        t_key = lesson.teacher.id
        g_key = lesson.group.id
        r_key = classroom.id

        if slot in teacher_busy.get(t_key, set()) or \
           slot in group_busy.get(g_key, set()) or \
           slot in room_busy.get(r_key, set()):
            return False

        teacher_busy.setdefault(t_key, set()).add(slot)
        group_busy.setdefault(g_key, set()).add(slot)
        room_busy.setdefault(r_key, set()).add(slot)

    return True