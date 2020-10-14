# Sparkify database and pipeline
***
This project will include the files to create and define tables for a database with a star schema by data modeling, and also to build an ETL pipeline for a database in Redshift which will allow the client to access and analyze the information that they have been collecting. The transformation of this data extracted from JSON logs that the clients have been collecting over some time and from S3 buckets in AWS, will allow them to **analyze** and to **extract new relevant information** which can help their decision-making process on future options regarding marketing, store availability...  
Having this information available with queries is a powerful tool that will give the client plenty of flexibility.

The files that include this project are:

* create_tables.py
* sql_queries.py
* etl.py
* dwh.cfg
* Redshift_Management.ipynb

## create_tables.py
***
This file creates the connection to the Redshift cluster previously created and it creates a set of dimensional tables that will contain the information for their analytics team to obtain information about which songs their users are listening to. 

## sql_queries.py
***
This file contains the functions imported by the file <em>create_tables.py</em>  
which will allow to create the set of dimensional tables with a star schema.
This functions will allow to <em>Drop</em> old tables, <em>Create</em> new ones and also, to <em>Insert</em> data into them.  

## etl.py
***
With this file we will copy the data from the S3 buckets to some staging tables and subsequently process the data to load it into the fact and dimensional tables.   

## dwh.cfg
***
This configuration file contains the parameters to create and to access and modify the Redshift cluster and the IAM Role.

## Redshift_Management.ipynb
***
This file will allow us to create the Redshift cluster if it hasn't been created yet and the IAM role that will be used. It requires the _access key_ and _secret access key_ of the AWS user.
This code will also return the ENDPOINT (HOST) and ARN that need to be in the _dwh.cfg_ file to access the cluster when creating the tables. 
At the end of the code this file contains the commands to delete the Redshift cluster and the role created.

