# Основа API для проекта с кормушкой в приютах

Данный проект является основой API для проекта с кормушкой в приютах для управления всеми сущностями.
___
## Описание проекта

В предметной области проекта есть следующие сущности: устройства, модели устройств, предприятия, филиалы предприятий, список заданий, периодичность выполнения заданий и конфигурации системы. В проекте реализованы ORM модели, CRUD операции над всеми сущностями, модели Pydantic, а также стандартные эндпоинты на основе каждого CRUD'а.
___
## Используемые технологии

* Python 3.10+
* FastAPI
* JWT
* Pydantic
* MySQL
* Git
* Docker
* Docker-compose
___
## Функциональные возможности

* Аутентификация пользователей
* Просмотр, добавление, редактирование и удаление данных из всех таблиц
___
## Установка

### Для пользователей:

#### Предварительные требования:

* Docker версии 20.10+
* Docker Compose версии 1.29+

### Шаги установки:

1.  Создайте и перейдите в директорию приложения:
    ```bash
    mkdir app
    cd app
    ```

2. Создайте файл docker-compose.yml
    ```bash
    nano docker-compose.yml
    ```

3. Вставьте в этот файл следующее содержимое:
    ```
   services:
      app:
        image: shachenkovan/feeder_api:latest
        ports:
          - "8000:8000"
        depends_on:
          db:
            condition: service_healthy
        env_file:
          - .env
        environment:
          - DB_HOST=db
    
    
      db:
        image: mysql:8.0
        environment:
          MYSQL_ROOT_PASSWORD: ${DB_PASSWORD}
          MYSQL_DATABASE: ${DB_NAME}
          MYSQL_DEFAULT_AUTHENTICATION_PLUGIN: mysql_native_password
        command: --default-authentication-plugin=mysql_native_password
        volumes:
          - ./mysql-init/:/docker-entrypoint-initdb.d/
        healthcheck:
          test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
          interval: 5s
          timeout: 10s
          retries: 10
   ```

4. Создайте файл .env:
    ```bash
   nano .env
    ```

5. Вставьте в него следующее содержимое предварительно изменив данные на свои:
    ```
    DB_USER=root
    DB_PASSWORD=your_password # изменить
    DB_HOST=localhost
    DB_NAME=feeder_api_db
    DB_PORT=3306
    
    LOCAL_JWT_KEY=your_jwt_key # изменить
   ```

6. Запустите приложение с помощью следующих команд:
    ```bash
   # Запуск контейнеров в фоновом режиме
    docker-compose up -d
    
    # Просмотр статуса запуска приложения и базы данных
    docker-compose ps
   ```
   
7. Перейдите по ссылке для просмотра документации и тестирования api:
    ```
   http://localhost:8000/docs
   ```

8. Основные команды для управления приложением:
    ```bash
        # Просмотр статуса сервисов
        docker-compose ps
        
        # Просмотр логов приложения
        docker-compose logs app
        
        # Просмотр логов базы данных
        docker-compose logs db
        
        # Остановка приложения
        docker-compose down
        
        # Перезапуск приложения
        docker-compose restart
        
        # Обновление до последней версии
        docker-compose pull
        docker-compose up -d
    ```

___
## Учетная запись

Администратор:

    Логин: admin
    Пароль: admin

___
## Поддержка

Для вопросов по установке и использованию, а также с предложениями по исправлению или улучшению проекта обращайтесь:

    Email: nastya.nba888@gmail.com
    Telegram: @shachenkovan