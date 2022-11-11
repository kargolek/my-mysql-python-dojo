DROP TABLE IF EXISTS ExampleTable;

USE Northwind;

CREATE TABLE ExampleTable (
  exId INT AUTO_INCREMENT NOT NULL
  ,exName VARCHAR(15) NOT NULL
  ,exDescription TEXT NULL
  ,PRIMARY KEY (exId)
  ) ENGINE=INNODB;

INSERT INTO ExampleTable(exId, exName, exDescription) VALUES(1, 'TestName', 'TestDescription');