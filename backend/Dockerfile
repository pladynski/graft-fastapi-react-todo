FROM python:3.11-bookworm

WORKDIR /usr/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Existing layers stay in WORKDIR. gg --modules must be a small sibling
# directory: only the public facade + the original response schema. If
# models.py (peewee) is inside --modules, GMA fails on Todo.DoesNotExist.
COPY services.py repositories.py models.py schemas.py /usr/app/
COPY config /usr/app/config
COPY controllers.py schemas.py pyproject.toml /usr/app/controller/

RUN apt-get update \
 && apt-get install -y --no-install-recommends wget ca-certificates \
 && ARCH=$(dpkg --print-architecture) \
 && wget -q -O /usr/app/gg.deb "https://github.com/grft-dev/graftcode-gateway/releases/latest/download/gg_linux_${ARCH}.deb" \
 && dpkg -i /usr/app/gg.deb \
 && rm /usr/app/gg.deb \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

ENV PYTHONPATH=/usr/app

EXPOSE 8000

# Do not pass --projectKey unless you have a real key from portal.graftcode.com.
CMD ["gg", "--modules", "./controller/", "--runtime", "python", "--port", "8000", "--corsAllowedOrigins", "*"]
