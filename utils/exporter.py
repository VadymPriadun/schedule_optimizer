import pandas as pd
from datetime import datetime

days = ["Понеділок", "Вівторок", "Середа", "Четвер", "Пʼятниця"]
times = ["08:30–10:05", "10:25–12:00", "12:20–13:55", "14:10–15:45", "16:00–17:35", "17:50–19:25"]

def export_to_excel(schedule, problem):
    data = {day: {time: "" for time in times} for day in days}
    df_data = []

    for (lesson, classroom, (d, p)), _ in schedule.items():
        row = {
            "День": days[d],
            "Час": times[p],
            "Предмет": lesson.subject.name,
            "Викладач": lesson.teacher.name,
            "Група": lesson.group.name,
            "Аудиторія": classroom.name
        }
        df_data.append(row)

    df = pd.DataFrame(df_data)
    df = df.sort_values(by=["День", "Час"])
    filename = f"results/schedule_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
    df.to_excel(filename, index=False)
    print(f"Розклад збережено → {filename}")

def export_to_html(schedule, problem):
    html = "<html><body><h1>Розклад занять</h1><table border='1'>"
    html += "<tr><th>День</th><th>Час</th><th>Предмет</th><th>Викладач</th><th>Група</th><th>Ауд.</th></tr>"
    for (lesson, classroom, (d, p)), _ in sorted(schedule.items(), key=lambda x: x[0][2]):
        html += f"<tr><td>{days[d]}</td><td>{times[p]}</td><td>{lesson.subject.name}</td>"
        html += f"<td>{lesson.teacher.name}</td><td>{lesson.group.name}</td><td>{classroom.name}</td></tr>"
    html += "</table></body></html>"
    with open("results/schedule.html", "w", encoding="utf-8") as f:
        f.write(html)