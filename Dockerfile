FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY api/ api/
COPY models/ models/
COPY data/clean_data.csv data/clean_data.csv
COPY monitoring/ monitoring/
COPY MODEL_CARD.md .

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
