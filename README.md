# veeva

Exercise

## login to db

sudo mysql -u root

## create initital db

CREATE DATABASE veeva_vault;
CREATE USER 'veeva'@'localhost' IDENTIFIED BY 'veeva';
GRANT ALL PRIVILEGES ON veeva_vault.* TO 'veeva'@'localhost';
FLUSH PRIVILEGES;

## if data in vault not allready set to ready_for_depl, set it this way

UPDATE deployment_data SET build_status__c = 'ready_for_deployment__c';
SELECT id FROM deployment_data WHERE build_status__c = "ready_for_deployment__c";
SELECT id FROM deployment_data WHERE build_status__c = "complete__c";

## Workflow

- create database
- run the file create_and_populate_table.py with both functions uncommented
- if records suceffuly populated, try the read_and_update_task1 file

- check are there any duplcate entryes for build_version__c in db
SELECT build_version__c, COUNT(*) FROM deployment_data GROUP BY build_version__c HAVING COUNT(*) > 1;

- if so, remove them
DELETE t1 FROM deployment_data t1 JOIN deployment_data t2  ON t1.build_version__c = t2.build_version__c  AND t1.id > t2.id;

- set that field to unique
ALTER TABLE deployment_data ADD UNIQUE (build_version__c);

- try the create_new_rec_task2.py
