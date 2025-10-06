FROM node:20-alpine
WORKDIR /app
COPY package.json package-lock.json* yarn.lock* pnpm-lock.yaml* ./
RUN if [ -f yarn.lock ]; then yarn --frozen-lockfile; elif [ -f pnpm-lock.yaml ]; then npm i -g pnpm && pnpm i --frozen-lockfile; elif [ -f package-lock.json ]; then npm ci; else npm install; fi
COPY . .
ENV PORT=3000
EXPOSE 3000
CMD ["npm", "run", "dev"]
