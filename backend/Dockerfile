FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Host the existing controller with Graftcode Gateway (replaces uvicorn).
# --modules is only the public surface so GMA does not scan peewee models.
RUN apt-get update \
 && apt-get install -y --no-install-recommends wget ca-certificates \
 && ARCH=$(dpkg --print-architecture) \
 && wget -q -O /tmp/gg.deb "https://github.com/grft-dev/graftcode-gateway/releases/latest/download/gg_linux_${ARCH}.deb" \
 && dpkg -i /tmp/gg.deb \
 && rm /tmp/gg.deb \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/* \
 && mkdir -p /modules \
 && cp controllers.py schemas.py pyproject.toml /modules/

ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["gg", "--modules", "/modules/", "--runtime", "python", "--port", "8000", "--corsAllowedOrigins", "*"]
