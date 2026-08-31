FROM node:22-bookworm-slim

WORKDIR /app

RUN apt-get update \
 && apt-get install -y --no-install-recommends curl ca-certificates \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

COPY package*.json ./
RUN npm install --no-fund --no-audit

COPY . .
RUN chmod +x /app/docker-entrypoint.sh /app/scripts/install-graft.sh

EXPOSE 5173

ENTRYPOINT ["/app/docker-entrypoint.sh"]
