from collections import deque
from scheduler import ScheduleProblem

INF = 10**9

def hopcroft_karp_schedule(problem: ScheduleProblem):
    lessons = problem.lessons
    if not lessons:
        return {}

    time_slots = problem.timeslots
    classrooms = problem.classrooms

    slot_to_idx = {}
    idx_to_slot = []
    idx = 0
    for classroom in classrooms:
        for slot in time_slots:
            key = (classroom.id, slot)
            slot_to_idx[key] = idx
            idx_to_slot.append((classroom, slot))
            idx += 1

    n_left = len(lessons)
    n_right = len(idx_to_slot)

    graph = [[] for _ in range(n_left)]
    for i, lesson in enumerate(lessons):
        for classroom in classrooms:
            if classroom.capacity < lesson.group.size:
                continue
            for slot in time_slots:
                j = slot_to_idx[(classroom.id, slot)]
                graph[i].append(j)

    pair_u = [-1] * n_left 
    pair_v = [-1] * n_right   
    dist = [0] * (n_left + 1)   

    def bfs():
        queue = deque()
        for u in range(n_left):
            if pair_u[u] == -1:
                dist[u] = 0
                queue.append(u)
            else:
                dist[u] = INF
        dist[n_left] = INF  
        while queue:
            u = queue.popleft()
            if dist[u] < dist[n_left]:
                for v in graph[u]:
                    if pair_v[v] == -1:
                        dist[n_left] = dist[u] + 1
                    else:
                        if dist[pair_v[v]] == INF:
                            dist[pair_v[v]] = dist[u] + 1
                            queue.append(pair_v[v])
        return dist[n_left] != INF

    def dfs(u):
        for v in graph[u]:
            if pair_v[v] == -1 or (dist[pair_v[v]] == dist[u] + 1 and dfs(pair_v[v])):
                pair_u[u] = v
                pair_v[v] = u
                return True
        dist[u] = INF
        return False

    matching = 0
    while bfs():
        for u in range(n_left):
            if pair_u[u] == -1:
                if dfs(u):
                    matching += 1


    schedule = {}
    teacher_busy = {t.id: set() for t in problem.teachers}
    group_busy = {g.id: set() for g in problem.groups}
    room_busy = {c.id: set() for c in problem.classrooms}


    lesson_order = sorted(range(n_left), key=lambda i: -lessons[i].group.size)

    for u in lesson_order:
        v = pair_u[u]
        if v == -1:
            continue  
        classroom, slot = idx_to_slot[v]
        lesson = lessons[u]


        if (slot in teacher_busy[lesson.teacher.id] or
            slot in group_busy[lesson.group.id] or
            slot in room_busy[classroom.id]):
            continue  


        schedule[(lesson, classroom, slot)] = None
        teacher_busy[lesson.teacher.id].add(slot)
        group_busy[lesson.group.id].add(slot)
        room_busy[classroom.id].add(slot)

    return schedule