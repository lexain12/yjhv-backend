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

//---------------------------//

For running photo service:
```
curl -X PUT -F "file=@test.jpg" http://localhost:32000/upload
```

For running server:
```
docker-compose up --build
```

For running photoService:
```
docker run --net yjhv --hostname people_counter --name people_counter -it --rm -p 32000:32000 -v $(pwd)/images:/app/images -v $(pwd)/results:/app/results people-counter
```

Example:
```
curl localhost:8080/rooms/0
```


(For some fixes, outdated)
For curl requests:
```
docker exec -it 3f5cd90c3bad /bin/bash
curl people_counter:32000/count/people
```