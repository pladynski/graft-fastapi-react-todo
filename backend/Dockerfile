FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# slim has sh but not curl. Official installer unpacks ./gg, except on Debian
# it only writes gg.deb — extract that binary (do not dpkg -i).
RUN apt-get update \
 && apt-get install -y --no-install-recommends curl ca-certificates \
 && rm -rf /var/lib/apt/lists/* \
 && curl -fsSL grft.dev/get/gg | sh \
 && if [ ! -x ./gg ] && [ -f ./gg.deb ]; then \
      dpkg-deb -x ./gg.deb /tmp/gg-unpack \
      && find /tmp/gg-unpack -type f -name gg -exec cp {} ./gg \; \
      && chmod +x ./gg \
      && rm -rf /tmp/gg-unpack ./gg.deb; \
    fi \
 && mkdir -p /modules \
 && cp controllers.py schemas.py pyproject.toml /modules/

ENV PYTHONPATH=/app

EXPOSE 8000

# Shell form so DEVELOPMENT_ORIGINS expands at runtime (JSON exec form would not).
CMD ./gg --modules /modules/ --runtime python --port 8000 --corsAllowedOrigins "${DEVELOPMENT_ORIGINS:-http://localhost:5173,http://localhost:5174,http://localhost:3000}"
