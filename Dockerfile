FROM mysql:latest
ENV MYSQL_ROOT_PASSWORD mat22sql
ENV MYSQL_DATABASE matnet_db
ENV MYSQL_USER cho
ENV MYSQL_PASSWORD 1234
ADD base.sql /docker-entrypoint-initdb.d
EXPOSE 3306