# Use an official Node.js runtime as a parent image
FROM node:19-bullseye-slim as builder

# Set the working directory to /app
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package.json package-lock.json ./

# Install dependencies
RUN npm ci

# Copy the rest of the application code to the working directory
COPY . /app

# Build the application for production
RUN npm run build

# Use an official Nginx runtime as a parent image
FROM nginxinc/nginx-unprivileged:1.23.3-alpine-slim

WORKDIR /app
# Copy the build output from the previous step to Nginx's default public directory
COPY --from=builder /app/build  /usr/share/nginx/html
COPY nginx/nginx.conf.template /etc/nginx/nginx.conf.template
COPY nginx/run_nginx.sh ./server/run_nginx.sh
COPY inject-env-template.js /app/www/inject-env-template.js
# Copy Nginx configuration file

USER 0
# Ensure nginx user has required permissions
RUN chown -R nginx /etc/nginx \
    && chown -R nginx /app \
    && chown -R nginx /var/run/ \
    # Ensure run script is executable and have correct format
    && chmod +x ./server/run_nginx.sh \
    && dos2unix ./server/run_nginx.sh
EXPOSE 5173
# Run start script as nginx user (UID=101)
USER 101
# Start Nginx in the foreground
# CMD ["nginx", "-g", "daemon off;"]
CMD /bin/sh -c "./server/run_nginx.sh"