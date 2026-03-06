FROM python:3.11-slim

WORKDIR /minesweeperapp

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/
COPY tests/ tests/
COPY web/ web/

CMD ["python", "web/app.py"]


