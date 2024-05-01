# 1 install conda
install conda.exe

# 2 สร้าง env
conda create --env envname

# 3 activate env
conda activate envname

# 4 install pip เพื่อให้ใช้คำสั่งติดตั้ง package ต่างๆ ได้
conda install pip

# 5 ติดตั้ง package ที่ต้องใช้
pip install -r requirements.txt ไม่ใช้แล้ว
pip install pillow xmltodict matplotlib shapely fiona pymeanshift requests scikit-image statistics psycopg2

# 6 ขอ token 
https://www.makewebeasy.com/th/blog/google-map-api-key-manual/

# 7 create database
CREATE DATABASE gsv;
CREATE EXTENSION postgis;
CREATE SCHEMA geodata;

# 8 create table
CREATE TABLE geodata.gsvpoint(
    gid serial not null,
    poiname text,
    greenergy numeric,
    geom geometry('POINT', 4326)
);

# 9 inser green value to table
INSERT INTO geodata.gsvpoint(
    poiname, greenergy, geom )VALUES(
    '1', 0.55, ST_GeomFromText('POINT(98.966811624563 18.801880625621166)')
)

# select
SELECT * FROM geodata.gsvpoint