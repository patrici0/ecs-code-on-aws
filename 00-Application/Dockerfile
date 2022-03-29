FROM node:14.19.1-alpine
COPY app/ /app
WORKDIR /app
RUN npm install --global gulp && npm install gulp
RUN npm install
RUN gulp
ENTRYPOINT ["node"]
EXPOSE 80
CMD ["server.js"]
