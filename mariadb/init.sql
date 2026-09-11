CREATE DATABASE IF NOT EXISTS nebula;

USE nebula;

CREATE TABLE IF NOT EXISTS servers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    region VARCHAR(60),
    state VARCHAR(20),
    flavor VARCHAR(60),
    ip VARCHAR(50),
    vcpu INT
);

CREATE TABLE IF NOT EXISTS regions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(60),
    code VARCHAR(30),
    servers INT,
    utilization INT
);

CREATE TABLE IF NOT EXISTS networks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100)
);

INSERT INTO servers (name, region, state, flavor, ip, vcpu)
VALUES
    ('api-gateway-01', 'Dhaka', 'ACTIVE', 'g2.medium', '10.30.10.11', 4),
    ('compute-web-01', 'Dhaka', 'ACTIVE', 'g2.large', '10.30.10.21', 8),
    ('analytics-01', 'Singapore', 'ACTIVE', 'g2.xlarge', '10.30.20.13', 16),
    ('worker-queue-02', 'Frankfurt', 'ACTIVE', 'g2.medium', '10.30.30.44', 4),
    ('legacy-report-01', 'Frankfurt', 'STOPPED', 'g1.small', '10.30.30.51', 2);

INSERT INTO regions (name, code, servers, utilization)
VALUES
    ('Dhaka', 'ap-south-1', 2, 64),
    ('Singapore', 'ap-southeast-1', 1, 48),
    ('Frankfurt', 'eu-central-1', 2, 77);

INSERT INTO networks (name)
VALUES
    ('frontend-net'),
    ('backend-net'),
    ('storage-net');
