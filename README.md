# fastapi

[Edit in StackBlitz next generation editor ⚡️](https://stackblitz.com/~/github.com/zinxon/fastapi)

```bash
python3 -m venv fastapi
source fastapi/bin/activate
pip install -r requirements.txt
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
python3 src/main.py
```
