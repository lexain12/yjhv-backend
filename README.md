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