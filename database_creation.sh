sudo -i -u postgres
psql
CREATE DATABASE agriconnect;
CREATE USER dave WITH PASSWORD 'dave@123';
GRANT ALL PRIVILEGES ON DATABASE agriconnect TO dave;
\q
exit
