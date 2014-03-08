MySQL Table Statement
---------------------

MySQL Table Statement Report Generator tool

# Requirement

* jinja2
> pip install jinja

* mysql.connector 1.x
> python setup.py


# Arguments

* help
> -u --user: mysql user id
>
> -p --password: mysql user password
>
> -h --host: mysql host ip address
>
> -D --database: database schema name
>
> -r --report: result output path

# run script

* Example
> report.py -u mysql_user_id -p password -h host_ip -D schema_name -r /path/to/report.html
>


# Report Result
---------------

## Schema Name

### Table Name

Table comment

Column | Type    | Not Null | Primary Key | Auto Increment | Default | Comment
------ | ------- | -------- | ----------- | -------------- | ------- | -------
id     | int(11) | No       | Pri         | No             | None    | index

