CREATE DATABASE IF NOT EXISTS ejercicios_flask;
USE ejercicios_flask;

CREATE TABLE IF NOT EXISTS par_impar (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero INT NOT NULL,
    resultado VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS multiplicacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero INT NOT NULL,
    resultado TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS adivina (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero_secreto INT NOT NULL,
    intento INT NOT NULL,
    cantidad_intentos INT NOT NULL,
    resultado VARCHAR(100) NOT NULL
);
