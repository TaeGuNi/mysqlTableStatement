MySQL Table Statement
---------------------

MySQL Table Statement Report Generator tool

# Requirement

* jinja2

> pip install jinja2

* mysql.connector 1.x

> wget http://dev.mysql.com/get/Downloads/Connector-Python/mysql-connector-python-1.1.6.tar.gz
> tar zxvf mysql-connector-python-1.1.6.tar.gz
> cd mysql-connector-python-1.1.6
> python setup.py install


# Arguments

* help

> -u --user: mysql user id
> -p --password: mysql user password
> -h --host: mysql host ip address
> -D --database: database schema name
> -r --report: result output path

# run script

* Example

> report.py -u mysql_user_id -p password -h host_ip -D schema_name -r /path/to/report.html


# Report Result
---------------

## Schema Name

### Table Name

Table comment

Column | Type    | Not Null | Primary Key | Auto Increment | Default | Comment
------ | ------- | -------- | ----------- | -------------- | ------- | -------
id     | int(11) | No       | Pri         | No             | None    | index

