drop database mifostenant;
create database mifostenant;
use mifostenant;

CREATE TABLE IF NOT EXISTS m_category
(
	id INT NOT NULL AUTO_INCREMENT,
	category VARCHAR(20) NOT NULL UNIQUE,
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS m_feature 
(
	id INT NOT NULL AUTO_INCREMENT,
	feature VARCHAR(20) NOT NULL UNIQUE,
	value VARCHAR(10) DEFAULT 'Ratio',
	data VARCHAR(10) DEFAULT 'Char',
	category VARCHAR(20) NOT NULL,
	status VARCHAR(20) NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (category) REFERENCES m_category(category)
);

insert into m_category values (1, 'Individual');
insert into m_category values (2, 'Organisation');
insert into m_category values (3, 'Country');
insert into m_category values (4, 'CreditHistory');
insert into m_category values (5, 'Loan');


CREATE TABLE IF NOT EXISTS m_configuration
(
	id INT(11) NOT NULL AUTO_INCREMENT,
	product VARCHAR(20) NOT NULL,
	feature VARCHAR(20) NOT NULL UNIQUE,
	category VARCHAR(20) NOT NULL,
	weightage FLOAT(6,5) NOT NULL,
	greenmin VARCHAR(20) NOT NULL,
	greenmax VARCHAR(20) NOT NULL,
	ambermin VARCHAR(20) NOT NULL,
	ambermax VARCHAR(20) NOT NULL,
	redmin VARCHAR(20) NOT NULL,
	redmax VARCHAR(20) NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (category) REFERENCES m_category(category),
	FOREIGN KEY (feature) REFERENCES m_feature(feature)
);

CREATE TABLE IF NOT EXISTS m_criteria
(
	id INT(11) NOT NULL AUTO_INCREMENT,
	feature VARCHAR(20) NOT NULL UNIQUE,
	product VARCHAR(20) NOT NULL,
	category VARCHAR(20) NOT NULL,
	datasource VARCHAR(20) NOT NULL,
	sqlapi VARCHAR(200) NOT NULL,
	keyvalue VARCHAR(100) NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (feature) REFERENCES m_feature(feature)
);

CREATE TABLE IF NOT EXISTS m_criteriascore
(
	id INT(11) NOT NULL AUTO_INCREMENT,
	cscriteriatableid INT NOT NULL,
	criteria VARCHAR(20) NOT NULL,
	score VARCHAR(20) NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (cscriteriatableid) REFERENCES m_criteria(id)
);

CREATE TABLE IF NOT EXISTS Scorecard
(
	Scorecard_id INT(11) NOT NULL AUTO_INCREMENT,
	Loan_id INT(11) NOT NULL,
	Model VARCHAR(20) NOT NULL,
	Saved_Model_Data JSON,
	PRIMARY KEY (Scorecard_id)
);

CREATE TABLE IF NOT EXISTS m_loan
(
	id INT(11) NOT NULL AUTO_INCREMENT,
	feature1 VARCHAR(20),
	feature2 VARCHAR(20),
	feature3 VARCHAR(20),
	PRIMARY KEY (id)
);

