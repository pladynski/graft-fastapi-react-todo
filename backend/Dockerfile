FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# slim has sh but not curl. Official installer unpacks ./gg into WORKDIR.
RUN apt-get update \
 && apt-get install -y --no-install-recommends curl ca-certificates \
 && rm -rf /var/lib/apt/lists/* \
 && curl -fsSL grft.dev/get/gg | sh \
 && mkdir -p /modules \
 && cp controllers.py schemas.py pyproject.toml /modules/

ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["./gg", "--modules", "/modules/", "--runtime", "python", "--port", "8000", "--corsAllowedOrigins", "*"]
