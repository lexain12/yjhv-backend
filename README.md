# yjhv-backend

Here's implementation of backend for our project for university load of public places

Virtual env:
```
python3 -m venv myenv
source myevn/bin/activate
```

Запуск мок докера:
```
colima start
```

Запуска приложения
```
cd src
docker-compose up --build
```

Для примера получения результата в отдельной консольке надо прописать
```
curl localhost:8080/rooms/0
```

Ендпоинты на данный момент:

"/schemes" - получение всех схем(этажи здания)

"/scheme/<int:scheme_id>" - получение конкретной схемы

"/schedule/<int:course_id>" - получение расписания аудитории

"/rooms/<int:scheme_id>" - получение информации обо всех комнатах в схеме