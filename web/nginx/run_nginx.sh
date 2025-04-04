echo Provding nginx template config with env variables...
envsubst '${REACT_APP_API_BASE_URL}' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf
envsubst < /app/www/inject-env-template.js > /app/www/inject-env.js
echo Starting Nginx… api: ${REACT_APP_API_BASE_URL}

nginx -g "daemon off;" -c /etc/nginx/nginx.conf