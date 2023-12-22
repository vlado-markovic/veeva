# veeva

Exercise

sudo mysql -u root

CREATE DATABASE veeva_vault;
CREATE USER 'veeva'@'localhost' IDENTIFIED BY 'veeva';
GRANT ALL PRIVILEGES ON veeva_vault.* TO 'veeva'@'localhost';
FLUSH PRIVILEGES;
