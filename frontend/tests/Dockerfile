FROM cypress/base:12.4.0

WORKDIR /e2e

COPY package*.json ./

RUN npm install

COPY . .

CMD ["./entrypoint.sh"]
