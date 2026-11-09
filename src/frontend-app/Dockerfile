# Production image (development uses Dockerfile.dev).
# The build stage runs on the builder's own platform (no emulation): its output is plain files.
FROM --platform=$BUILDPLATFORM node:24.22.1-bookworm-slim AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

# nginx serves the built files and passes /api to the API. It fills in API_URL when it starts, so
# the same image runs anywhere.
FROM nginx:1.31.8-alpine
ENV API_URL=http://api-service:9000
COPY nginx.conf.template /etc/nginx/templates/default.conf.template
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
