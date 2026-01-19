Запуск:
.\.venv\Scripts\activate
uv run --env-file .env -- python main.py

В .env создать переменные:
URL=https://ip:port/login
LOGIN
PASSWORD

Создать файл profiles.json со структурой:
[
  {
    "file_name": "test.xlsx",
    "menu_type": "НЭСК" or "Географические объекты",
    "meters": ["12345678", "87654321"]
  }
]

Создать папку download.
