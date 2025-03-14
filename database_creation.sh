sudo -i -u postgres
psql
CREATE DATABASE agriconnect;
CREATE USER dave WITH PASSWORD 'dave@123';
GRANT ALL PRIVILEGES ON DATABASE agriconnect TO dave;
\q
exit
# \d[S+]
#   \dt[S+] [PATTERN]      list tables
#   \dT[S+] [PATTERN]      list data types
#   \l[+]   [PATTERN]      list databases
#  \password [USERNAME]   securely change the password for a user