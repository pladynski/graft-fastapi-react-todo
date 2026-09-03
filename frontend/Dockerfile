FROM node:22-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 5173

# Install the current graft from Gateway /npm, then start Vite (original CMD).
CMD ["sh", "-c", "until wget -qO- \"$GRAFT_NPM_URL\" 2>/dev/null | grep -q 'npm install'; do sleep 2; done; eval \"$(wget -qO- \"$GRAFT_NPM_URL\")\"; npm run dev -- --host"]
