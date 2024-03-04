Alter user 'root'@'%' IDENTIFIED WITH mysql_native_password BY 'Chengyan#251';
GRANT ALL PRIVILEGES ON hello.* TO 'root'@'%';
FLUSH PRIVILEGES;