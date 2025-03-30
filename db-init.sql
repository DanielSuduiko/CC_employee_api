CREATE USER IF NOT EXISTS 'readonly'@'%' IDENTIFIED BY 'readonlypass';
CREATE USER IF NOT EXISTS 'readonly'@'localhost' IDENTIFIED BY 'readonlypass';

FLUSH PRIVILEGES;
