# API-BASE
> Fast business model based on fastapi


##　Infrastructure
```markdown
- fastapi
- sqlalchemy[pg]
- redis-py
- fastapi-cache2
```

##　Directory
```markdown
├── app   # project root
│   ├── __init__.py
│   ├── api           # api routers object
│   ├── ctx.py        # context
│   ├── dao           # data access object
│   ├── db.py         # database info
│   ├── exception.py  # exception
│   ├── main.py       # app entry 
│   ├── midware.py    # middleware
│   ├── model      　 # sqlalchemy base model
│   ├── schema        # pydantic schemas
│   ├── service       # logic handle
│   ├── settings.py   # app settings
│   └── utils         # utils
├── logs
│   └── app_dev_2024-10-27.log
├── poetry.lock
├── pyproject.toml    # project config
├── startup.py        # app boot
```