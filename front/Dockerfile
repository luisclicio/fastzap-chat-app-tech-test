FROM node:22-slim AS base
WORKDIR /app

FROM base AS dependencies
COPY package.json package-lock.json ./
RUN npm install
COPY . .

FROM dependencies AS development
CMD ["npm", "run", "dev"]

FROM dependencies AS build
RUN npm run build

FROM base AS production
COPY --from=build /app/.output /app/
EXPOSE 3000
CMD ["node", "server/index.mjs"]
