CREATE USER IF NOT EXISTS 'readonly'@'%' IDENTIFIED BY 'readonlypass';
CREATE USER IF NOT EXISTS 'readonly'@'localhost' IDENTIFIED BY 'readonlypass';

-- We'll run GRANT later manually
FLUSH PRIVILEGES;
