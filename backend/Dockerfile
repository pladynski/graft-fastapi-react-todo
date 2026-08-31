FROM python:3.11-bookworm

WORKDIR /usr/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY todoservice/ /usr/app/todoservice/

RUN apt-get update \
 && apt-get install -y --no-install-recommends wget ca-certificates \
 && ARCH=$(dpkg --print-architecture) \
 && wget -q -O /usr/app/gg.deb "https://github.com/grft-dev/graftcode-gateway/releases/latest/download/gg_linux_${ARCH}.deb" \
 && dpkg -i /usr/app/gg.deb \
 && rm /usr/app/gg.deb \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

EXPOSE 8000

# Do not pass --projectKey unless you have a real key from portal.graftcode.com.
CMD ["gg", "--modules", "./todoservice/", "--port", "8000", "--corsAllowedOrigins", "*"]
