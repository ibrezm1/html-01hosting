sudo apt install postgresql postgresql-contrib

sudo systemctl start postgresql
sudo -i -u postgres

psql
CREATE DATABASE testdb;
\c testdb
\i /DML.sql
\q


psql -U postgres -d my_database -f /home/user/scripts/my_sql_script.sql

sudo -u postgres psql


sudo -u postgres psql
CREATE USER myuser WITH PASSWORD 'mypassword';
ALTER USER myuser CREATEDB;
CREATE DATABASE mydb OWNER myuser;
\q
psql -U myuser -d mydb -f /home/user/myfile.sql



sudo nano /etc/postgresql/14/main/pg_hba.conf
local   all             all                                     md5

sudo systemctl restart postgresql
psql -U myuser -d mydb
