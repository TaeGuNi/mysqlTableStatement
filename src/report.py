#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import os.path
import codecs
import getopt
import mysql.connector
from mysql.connector import errorcode
from jinja2 import Template


html_head = Template('<!DOCTYPE html>\n'
                     '<html lang="ko">\n'
                     '<head>\n'
                     '<title>Database Schema Report</title>\n'
                     '<style>\n'
                     'body {font-size: 11px}\n'
                     'th {background: #eee}\n'
                     'th, td {border: 1px solid #000}\n'
                     '</style>\n'
                     '</head>\n'
                     '<body>\n')
schema_name = Template('<h1>{{ name }}</h1>\n')
table_title = Template('<h2>{{ name }}</h2>\n'
                       '<p>{{ comment }}</p>')
table_head = Template('<table>\n'
                      '<colgroup width="960">\n'
                      '<col width="150" />\n'
                      '<col width="100" />\n'
                      '<col width="100" />\n'
                      '<col width="100" />\n'
                      '<col width="100" />\n'
                      '<col width="150" />\n'
                      '<col width="100" />\n'
                      '<col width="*" />\n'
                      '</colgroup>\n'
                      '<tr>\n'
                      '<th>Column</th>\n'
                      '<th>Type</th>\n'
                      '<th>Not Null</th>\n'
                      '<th>Primary Key</th>\n'
                      '<th>Auto Increment</th>\n'
                      '<th>Default</th>\n'
                      '<th>Comment</th>\n'
                      '</tr>\n')
table_body = Template('<tr>\n'
                      '<td>{{ name }}</td>\n'
                      '<td>{{ type }}</td>\n'
                      '<td>{{ null }}</td>\n'
                      '<td>{{ key }}</td>\n'
                      '<td>{{ extra }}</td>\n'
                      '<td>{{ default }}</td>\n'
                      '<td>{{ comment }}</td>\n'
                      '</tr>\n')
table_tail = Template('</table>\n')
html_tail = Template('</body>\n'
                     '<html>')


def execute(connect, query, args):
    try:
        cursor = connect.cursor()
        cursor.execute(query, args)
        return cursor.fetchall()
    except mysql.connector.Error as error:
        print(error)
    else:
        cursor.close()


def getDatabases(connect):
    query = 'select schema_name ' \
            'from information_schema.schemata ' \
            'where schema_name not in (%s, %s, %s)'
    args = ('information_schema', 'performance_schema', 'mysql')
    return execute(connect, query, args)


def getTables(connect, db):
    query = 'select table_name, table_comment ' \
            'from information_schema.tables ' \
            'where table_schema = %s'
    return execute(connect, query, db)


def geSchema(connect, args):
    query = 'select column_name, column_type, is_nullable, column_key, extra, column_default, column_comment ' \
            'from information_schema.columns ' \
            'where table_schema = %s and table_name = %s'
    return execute(connect, query, args)


def setReport(connect, db):
    if os.path.isfile(report):
        os.remove(report)
    report_file = codecs.open(report, 'a', 'utf-8')
    report_file.write(html_head.render())
    report_file.write(schema_name.render(name=db[0]))
    for tb in getTables(connect, db):
        args = db + tb
        report_file.write(table_title.render(name=tb[0], comment=tb[1]))
        report_file.write(table_head.render())
        for col in geSchema(connect, args[0:2]):
            report_file.write(table_body.render(name=col[0], type=col[1], null=col[2], key=col[3], extra=col[4], default=col[5], comment=col[6]))
        report_file.write(table_tail.render())
    report_file.write(html_tail.render())
    report_file.close()


if __name__ == '__main__':
    options, args = getopt.getopt(sys.argv[1:], 'u:p:h:D:r:', ['user=', 'password=', 'host=', 'database=', 'report='])
    for opt, arg in options:
        if opt in ('-u', '--user'):
            user = arg
        elif opt in ('-p', '--password'):
            password = arg
        elif opt in ('-h', '--host'):
            host = arg
        elif opt in ('-D', '--database'):
            database = arg
        elif opt in ('-r', '--report'):
            report = arg
    if user is not None and password is not None and host is not None and report is not None:
        try:
            config = {
                'user': user,
                'password': password,
                'host': host,
                'charset': 'utf8',
                }
            connect = mysql.connector.connect(**config)
            if database is None:
                db = getDatabases(connect)
            else:
                db = (database,)
            setReport(connect, db)
        except mysql.connector.Error as error:
            print(error)
        else:
            connect.close()
