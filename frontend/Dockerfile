FROM node:18-alpine

WORKDIR /app

COPY package.json ./
RUN npm install

COPY . .

# Expose Vite Port
EXPOSE 5174

CMD ["npm", "run", "dev", "--", "--host"]
