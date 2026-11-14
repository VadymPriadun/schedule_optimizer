days = ["Пн", "Вт", "Ср", "Чт", "Пт"]
times = ["08:30", "10:25", "12:20", "14:10", "16:00", "17:50"]

def print_pretty_schedule(schedule, problem):
    print("\n" + "="*100)
    print("                            РОЗКЛАД ЗАНЯТЬ".center(100))
    print("="*100)

    for day in range(5):
        print(f"\n{days[day]:^100}")
        for pair in range(6):
            slot = (day, pair)
            entries = [f"{l.subject.name[:25]:25} | {l.teacher.name[:15]:15} | {c.name} | {l.group.name}"
                       for (l, c, s) in schedule.keys() if s == slot]
            print(f"{times[pair]:8} │ {entries[0] if entries else '—':<80}")
            for extra in entries[1:]:
                print(" " * 10 + "│ " + extra)