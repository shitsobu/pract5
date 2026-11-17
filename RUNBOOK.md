# RUNBOOK — Инструкция по эксплуатации Attendance Service

## 1. Общие сведения

**Название приложения:** Attendance Service  
**Версия:** 0.5.0  
**Платформа:** Docker / Docker Compose  
**Порт контейнера:** 8006  
**Имя контейнера:** pract5-attendance  
**Docker-образ:** edu/attendance-service:v0.5.0  
**Сеть:** pract5-isolated  
**Том данных:** pract5-data

## 2. Назначение

Документ содержит порядок запуска, проверки, мониторинга, резервного копирования и восстановления приложения Attendance Service.

## 3. Предварительные требования

Перед запуском необходимо убедиться, что:

- Docker Desktop установлен и запущен;
- Docker Compose доступен;
- файлы проекта находятся в одной директории;
- офлайн-архив `release/attendance-v0.5.0.tar` доступен;
- файл `compose.yaml` присутствует в каталоге проекта.

## 4. Запуск приложения

Открыть CMD в каталоге проекта:

```cmd
cd /d C:\Users\Home\Desktop\pract5
```

Проверить конфигурацию:

```cmd
docker compose config
```

Загрузить образ из офлайн-архива:

```cmd
docker load -i release\attendance-v0.5.0.tar
```

Запустить приложение без обращения к внешнему реестру:

```cmd
docker compose up -d --pull never
```

Проверить состояние:

```cmd
docker compose ps
```

**Контрольная точка:** контейнер `pract5-attendance` должен иметь статус `healthy`.

## 5. Проверка работоспособности

Проверка маршрута `/health`:

```cmd
docker compose exec attendance python -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:8006/health').status)"
```

Ожидаемый результат: `200`.

Проверка маршрута `/attendance`:

```cmd
docker compose exec attendance python -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:8006/attendance').read().decode())"
```

Ожидаемый результат: JSON с информацией о посещаемости и версией приложения.

## 6. Мониторинг

Просмотр журналов:

```cmd
docker compose logs --tail=50 attendance
```

Просмотр использования ресурсов:

```cmd
docker stats --no-stream pract5-attendance
```

Проверка состояния контейнера:

```cmd
docker compose ps
```

## 7. Резервное копирование данных

Создать резервную копию файла состояния:

```cmd
docker cp pract5-attendance:/data/state.json backup\state.json
```

Проверить содержимое:

```cmd
type backup\state.json
```

Резервная копия должна находиться в каталоге `backup`.

## 8. Восстановление Docker-образа

Если локальный образ был удалён или повреждён, необходимо проверить архив:

```cmd
certutil -hashfile release\attendance-v0.5.0.tar SHA256
```

Ожидаемая контрольная сумма:

`43571636803bda705255adf4906e456c33e61147bb7cfb4597abc92ceb283d1c`

Загрузить образ:

```cmd
docker load -i release\attendance-v0.5.0.tar
```

Запустить приложение:

```cmd
docker compose up -d --pull never
```

Проверить состояние:

```cmd
docker compose ps
```

## 9. Критерии остановки и устранения неисправностей

Если контейнер не запускается:

1. Проверить состояние Docker Desktop.
2. Проверить корректность `compose.yaml`.
3. Проверить наличие образа версии `0.5.0`.
4. Изучить журналы приложения.
5. При отсутствии образа восстановить его из офлайн-архива.

Если `/health` не возвращает HTTP 200, приложение считается неисправным до устранения причины.

## 10. Остановка приложения

Для остановки и удаления контейнера с сетью:

```cmd
docker compose down
```

Docker Volume `pract5-data` при этом сохраняется.

**Не использовать `docker compose down -v`, если необходимо сохранить данные.**

## 11. Условия успешной эксплуатации

Приложение считается успешно развёрнутым, если:

- контейнер запущен;
- статус контейнера — `healthy`;
- маршрут `/health` возвращает HTTP 200;
- маршрут `/attendance` возвращает корректный JSON;
- данные сохраняются после перезапуска;
- восстановление образа из офлайн-архива выполняется успешно.