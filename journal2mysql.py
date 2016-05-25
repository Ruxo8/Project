#! /usr/bin/python
#-*- coding: utf-8-*-
#
# Sergi Ruiz
# isx48031044
#
# Program that exports logs from journalctl in JSON format to insert them into a mysql db
# You can limit the scope of the search of logs with the journalctl comand. 
# For more info see 'man journalctl'
# usage: journalctl --output=json-pretty | journal2mysql.py
# Parameters:
# -u, --user
#		especifies the user to connect to mysql.
# -p, --password
#		especifies the password to connect to mysql.
# -d, --database
#		especifies the db name to connect to mysql.
# -t, --table
#		especifies the name of the table.
# -n, --new
#		especifies if it's needed to create a new table.
# -T, --truncate
#		especifies if it's needed to truncate the table before adding new entires.
#-----------------------------------------------------------------------------------------

import sys
import argparse
import json
import mysql.connector
from mysql.connector import errorcode
import datetime
import syslog

class JJSON:
	def __init__(self, dicJson):
		######################### User Journal Fields ############################
		if "MESSAGE" in dicJson:
			self.MESSAGE = dicJson["MESSAGE"].replace('\'', '"')
		else:
			self.MESSAGE = "NULL"
		
		if "MESSAGE_ID" in dicJson:
			self.MESSAGE_ID = dicJson["MESSAGE_ID"]
		else:
			self.MESSAGE_ID = "NULL"
		
		if "PRIORITY" in dicJson:
			self.PRIORITY = dicJson["PRIORITY"]
		else:
			self.PRIORITY = "NULL"
		
		if "CODE_FILE" in dicJson:
			self.CODE_FILE = dicJson["CODE_FILE"]
		else:
			self.CODE_FILE = "NULL"
		
		if "CODE_LINE" in dicJson:
			self.CODE_LINE = dicJson["CODE_LINE"]
		else:
			self.CODE_LINE = "NULL"
		
		if "CODE_FUNCTION" in dicJson:
			self.CODE_FUNCTION = dicJson["CODE_FUNCTION"]
		else:
			self.CODE_FUNCTION = "NULL"
		
		if "CODE_FUNC" in dicJson:
			self.CODE_FUNC = dicJson["CODE_FUNC"]
		else:
			self.CODE_FUNC = "NULL"
		
		if "ERRNO" in dicJson:
			self.ERRNO = dicJson["ERRNO"]
		else:
			self.ERRNO = "NULL"
		
		if "SYSLOG_FACILITY" in dicJson:
			self.SYSLOG_FACILITY = dicJson["SYSLOG_FACILITY"]
		else:
			self.SYSLOG_FACILITY = "NULL"
		
		if "SYSLOG_IDENTIFIER" in dicJson:
			self.SYSLOG_IDENTIFIER = dicJson["SYSLOG_IDENTIFIER"]
		else:
			self.SYSLOG_IDENTIFIER = "NULL"
		
		if "SYSLOG_PID" in dicJson:
			self.SYSLOG_PID = dicJson["SYSLOG_PID"]
		else:
			self.SYSLOG_PID = "NULL"
		
		######################## Trusted Journal Fields ##########################
		if "_PID" in dicJson:
			self._PID = dicJson["_PID"]
		else:
			self._PID = "NULL"
		
		if "_UID" in dicJson:
			self._UID = dicJson["_UID"]
		else:
			self._UID = "NULL"
		
		if "_GID" in dicJson:
			self._GID = dicJson["_GID"]
		else:
			self._GID = "NULL"
		
		if "_COMM" in dicJson:
			self._COMM = dicJson["_COMM"]
		else:
			self._COMM = "NULL"
		
		if "_EXE" in dicJson:
			self._EXE = dicJson["_EXE"]
		else:
			self._EXE = "NULL"
		
		if "_CMDLINE" in dicJson:
			self._CMDLINE = dicJson["_CMDLINE"]
		else:
			self._CMDLINE = "NULL"
		
		if "_CAP_EFFECTIVE" in dicJson:
			self._CAP_EFFECTIVE = dicJson["_CAP_EFFECTIVE"]
		else:
			self._CAP_EFFECTIVE = "NULL"
		
		if "_AUDIT_SESSION" in dicJson:
			self._AUDIT_SESSION = dicJson["_AUDIT_SESSION"]
		else:
			self._AUDIT_SESSION = "NULL"
		
		if "_AUDIT_LOGINUID" in dicJson:
			self._AUDIT_LOGINUID = dicJson["_AUDIT_LOGINUID"]
		else:
			self._AUDIT_LOGINUID = "NULL"
		
		if "_SYSTEMD_CGROUP" in dicJson:
			self._SYSTEMD_CGROUP = dicJson["_SYSTEMD_CGROUP"]
		else:
			self._SYSTEMD_CGROUP = "NULL"
		
		if "_SYSTEMD_SESSION" in dicJson:
			self._SYSTEMD_SESSION = dicJson["_SYSTEMD_SESSION"]
		else:
			self._SYSTEMD_SESSION = "NULL"
		
		if "_SYSTEMD_UNIT" in dicJson:
			self._SYSTEMD_UNIT = dicJson["_SYSTEMD_UNIT"]
		else:
			self._SYSTEMD_UNIT = "NULL"
		
		if "_SYSTEMD_OWNER_UID" in dicJson:
			self._SYSTEMD_OWNER_UID = dicJson["_SYSTEMD_OWNER_UID"]
		else:
			self._SYSTEMD_OWNER_UID = "NULL"
		
		if "_SYSTEMD_SLICE" in dicJson:
			self._SYSTEMD_SLICE = dicJson["_SYSTEMD_SLICE"]
		else:
			self._SYSTEMD_SLICE = "NULL"
		
		if "_SELINUX_CONTEXT" in dicJson:
			self._SELINUX_CONTEXT = dicJson["_SELINUX_CONTEXT"]
		else:
			self._SELINUX_CONTEXT = "NULL"
		
		if "_SOURCE_REALTIME_TIMESTAMP" in dicJson:
			self._SOURCE_REALTIME_TIMESTAMP = dicJson["_SOURCE_REALTIME_TIMESTAMP"]
		else:
			self._SOURCE_REALTIME_TIMESTAMP = "NULL"
		
		if "_BOOT_ID" in dicJson:
			self._BOOT_ID = dicJson["_BOOT_ID"]
		else:
			self._BOOT_ID = "NULL"
		
		if "_MACHINE_ID" in dicJson:
			self._MACHINE_ID = dicJson["_MACHINE_ID"]
		else:
			self._MACHINE_ID = "NULL"
		
		if "_HOSTNAME" in dicJson:
			self._HOSTNAME = dicJson["_HOSTNAME"]
		else:
			self._HOSTNAME = "NULL"
		
		if "_TRANSPORT" in dicJson:
			self._TRANSPORT = dicJson["_TRANSPORT"]
		else:
			self._TRANSPORT = "NULL"
		
		######################### Kernel Journal Fields ###########################
		if "_KERNEL_DEVICE" in dicJson:
			self._KERNEL_DEVICE = dicJson["_KERNEL_DEVICE"]
		else:
			self._KERNEL_DEVICE = "NULL"
		
		if "_KERNEL_SUBSYSTEM" in dicJson:
			self._KERNEL_SUBSYSTEM = dicJson["_KERNEL_SUBSYSTEM"]
		else:
			self._KERNEL_SUBSYSTEM = "NULL"
		
		if "_UDEV_SYSNAME" in dicJson:
			self._UDEV_SYSNAME = dicJson["_UDEV_SYSNAME"]
		else:
			self._UDEV_SYSNAME = "NULL"
		
		if "_UDEV_DEVNODE" in dicJson:
			self._UDEV_DEVNODE = dicJson["_UDEV_DEVNODE"]
		else:
			self._UDEV_DEVNODE = "NULL"
		
		if "_UDEV_DEVLINK" in dicJson:
			self._UDEV_DEVLINK = dicJson["_UDEV_DEVLINK"]
		else:
			self._UDEV_DEVLINK = "NULL"
		
		############# Fields to log on behalf of a different program ##############
		if "COREDUMP_UNIT" in dicJson:
			self.COREDUMP_UNIT = dicJson["COREDUMP_UNIT"]
		else:
			self.COREDUMP_UNIT = "NULL"
		
		if "COREDUMP_USER_UNIT" in dicJson:
			self.COREDUMP_USER_UNIT = dicJson["COREDUMP_USER_UNIT"]
		else:
			self.COREDUMP_USER_UNIT = "NULL"
		
		if "OBJECT_PID" in dicJson:
			self.OBJECT_PID = dicJson["OBJECT_PID"]
		else:
			self.OBJECT_PID = "NULL"
		
		if "OBJECT_UID" in dicJson:
			self.OBJECT_UID = dicJson["OBJECT_UID"]
		else:
			self.OBJECT_UID = "NULL"
		
		if "OBJECT_GID" in dicJson:
			self.OBJECT_GID = dicJson["OBJECT_GID"]
		else:
			self.OBJECT_GID = "NULL"
		
		if "OBJECT_COMM" in dicJson:
			self.OBJECT_COMM = dicJson["OBJECT_COMM"]
		else:
			self.OBJECT_COMM = "NULL"
		
		if "OBJECT_EXE" in dicJson:
			self.OBJECT_EXE = dicJson["OBJECT_EXE"]
		else:
			self.OBJECT_EXE = "NULL"
		
		if "OBJECT_CMDLINE" in dicJson:
			self.OBJECT_CMDLINE = dicJson["OBJECT_CMDLINE"]
		else:
			self.OBJECT_CMDLINE = "NULL"
		
		if "OBJECT_AUDIT_SESSION" in dicJson:
			self.OBJECT_AUDIT_SESSION = dicJson["OBJECT_AUDIT_SESSION"]
		else:
			self.OBJECT_AUDIT_SESSION = "NULL"
		
		if "OBJECT_AUDIT_LOGINUID" in dicJson:
			self.OBJECT_AUDIT_LOGINUID = dicJson["OBJECT_AUDIT_LOGINUID"]
		else:
			self.OBJECT_AUDIT_LOGINUID = "NULL"
		
		if "OBJECT_SYSTEMD_CGROUP" in dicJson:
			self.OBJECT_SYSTEMD_CGROUP = dicJson["OBJECT_SYSTEMD_CGROUP"]
		else:
			self.OBJECT_SYSTEMD_CGROUP = "NULL"
		
		if "OBJECT_SYSTEMD_SESSION" in dicJson:
			self.OBJECT_SYSTEMD_SESSION = dicJson["OBJECT_SYSTEMD_SESSION"]
		else:
			self.OBJECT_SYSTEMD_SESSION = "NULL"
		
		if "OBJECT_SYSTEMD_OWNER_UID" in dicJson:
			self.OBJECT_SYSTEMD_OWNER_UID = dicJson["OBJECT_SYSTEMD_OWNER_UID"]
		else:
			self.OBJECT_SYSTEMD_OWNER_UID = "NULL"
		
		if "OBJECT_SYSTEMD_UNIT" in dicJson:
			self.OBJECT_SYSTEMD_UNIT = dicJson["OBJECT_SYSTEMD_UNIT"]
		else:
			self.OBJECT_SYSTEMD_UNIT = "NULL"
		
		if "OBJECT_SYSTEMD_USER_UNIT" in dicJson:
			self.OBJECT_SYSTEMD_USER_UNIT = dicJson["OBJECT_SYSTEMD_USER_UNIT"]
		else:
			self.OBJECT_SYSTEMD_USER_UNIT = "NULL"
		
		############################ Address Fields ##############################
		if "_CURSOR" in dicJson:
			self._CURSOR = dicJson["_CURSOR"]
		else:
			self._CURSOR = "NULL"
		
		if "_REALTIME_TIMESTAMP" in dicJson:
			self._REALTIME_TIMESTAMP = dicJson["_REALTIME_TIMESTAMP"]
		else:
			self._REALTIME_TIMESTAMP = "NULL"
		
		if "_MONOTONIC_TIMESTAMP" in dicJson:
			self._MONOTONIC_TIMESTAMP = dicJson["_MONOTONIC_TIMESTAMP"]
		else:
			self._MONOTONIC_TIMESTAMP = "NULL"
		
		##########################################################################
		if "UNIT" in dicJson:
			self.UNIT = dicJson["UNIT"]
		else:
			self.UNIT = "NULL"

syslog.openlog('journal2mysql')

# Parsing the arguments
try:
	parser = argparse.ArgumentParser(description='From Journalctl to mysql')
	parser.add_argument('-u', '--user', dest='user_name', help='user', type=str, default='root')
	parser.add_argument('-p', '--password', dest='user_password', help='password', type=str, default='2016Jupiter!')
	parser.add_argument('-d', '--database', dest='db_name', help='database name', type=str, default='Journalctl')
	parser.add_argument('-t', '--table', dest='table_name', help='table name', type=str, default='Logs')
	parser.add_argument('-n', '--new', help='new table', action="store_true")
	parser.add_argument('-T', '--truncate', help='truncate table', action="store_true")
	args=parser.parse_args()
except Exception:
	syslog.syslog("Error reading the arguments\n")
	sys.exit(1)

# Constants
TABLE = {}

TABLE[args.table_name] = (
						"CREATE TABLE `%s` ("
						" LOG_ID int(25) NOT NULL AUTO_INCREMENT, "
						" MESSAGE varchar(1023), "
						" MESSAGE_ID varchar(255), "
						" PRIORITY varchar(255), "
						" CODE_FILE varchar(255), "
						" CODE_LINE varchar(255), "
						" CODE_FUNCTION varchar(255), "
						" CODE_FUNC varchar(255), "
						" ERRNO varchar(255), "
						" SYSLOG_FACILITY varchar(255), "
						" SYSLOG_IDENTIFIER varchar(255), "
						" SYSLOG_PID varchar(255), "
						" _PID varchar(255), "
						" _UID varchar(255), "
						" _GID varchar(255), "
						" _COMM varchar(255), "
						" _EXE varchar(255), "
						" _CMDLINE varchar(255), "
						" _CAP_EFFECTIVE varchar(255), "
						" _AUDIT_SESSION varchar(255), "
						" _AUDIT_LOGINUID varchar(255), "
						" _SYSTEMD_CGROUP varchar(255), "
						" _SYSTEMD_SESSION varchar(255), "
						" _SYSTEMD_UNIT varchar(255), "
						" _SYSTEMD_OWNER_UID varchar(255), "
						" _SYSTEMD_SLICE varchar(255), "
						" _SELINUX_CONTEXT varchar(255), "
						" _SOURCE_REALTIME_TIMESTAMP varchar(255), "
						" _BOOT_ID varchar(255), "
						" _MACHINE_ID varchar(255), "
						" _HOSTNAME varchar(255), "
						" _TRANSPORT varchar(255), "
						" _KERNEL_DEVICE varchar(255), "
						" _KERNEL_SUBSYSTEM varchar(255), "
						" _UDEV_SYSNAME varchar(255), "
						" _UDEV_DEVNODE varchar(255), "
						" _UDEV_DEVLINK varchar(255), "
						" COREDUMP_UNIT varchar(255), "
						" COREDUMP_USER_UNIT varchar(255), "
						" OBJECT_PID varchar(255), "
						" OBJECT_UID varchar(255), "
						" OBJECT_GID varchar(255), "
						" OBJECT_COMM varchar(255), "
						" OBJECT_EXE varchar(255), "
						" OBJECT_CMDLINE varchar(255), "
						" OBJECT_AUDIT_SESSION varchar(255), "
						" OBJECT_AUDIT_LOGINUID varchar(255), "
						" OBJECT_SYSTEMD_CGROUP varchar(255), "
						" OBJECT_SYSTEMD_SESSION varchar(255), "
						" OBJECT_SYSTEMD_OWNER_UID varchar(255), "
						" OBJECT_SYSTEMD_UNIT varchar(255), "
						" OBJECT_SYSTEMD_USER_UNIT varchar(255), "
						" __CURSOR varchar(255), "
						" __REALTIME_TIMESTAMP varchar(255), "
						" __MONOTONIC_TIMESTAMP varchar(255), "
						" UNIT varchar(255), "
						" PRIMARY KEY (LOG_ID)"
						")ENGINE=InnoDB" % (args.table_name)
						)

DELETE = "DROP TABLE %s" % (args.table_name)

TRUNCATE = "TRUNCATE TABLE %s" % (args.table_name)

# Connecting
try:
	connection = mysql.connector.connect(user=args.user_name, password=args.user_password, database=args.db_name)
	cursor = connection.cursor()
	
except mysql.connector.Error as err:
	if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
		syslog.syslog('Something is wrong with your user name or password\n')
	elif err.errno == errorcode.ER_BAD_DB_ERROR:
		syslog.syslog('Database does not exist\n')
	else:
		syslog.syslog(err)
	sys.exit(2)

# If we have to create a Table
if args.new:
	try:
		syslog.syslog("Creating table {}.\n".format(args.table_name))
		cursor.execute(TABLE[args.table_name])
	except mysql.connector.Error as err:
		# If table already exists we drop it and create a new one
		if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
			syslog.syslog("Table {} already exists.\n".format(args.table_name))
			# Delete
			try:
				syslog.syslog("Deleting and creating a new one... \n")
				cursor.execute(DELETE)
				# Create
				try:
					syslog.syslog("Creating table {}".format(args.table_name))
					cursor.execute(TABLE[args.table_name])
				except mysql.connector.Error as err:
					syslog.syslog(err.msg)
				else:
					syslog.syslog("Created table {}.\n".format(args.table_name))
			except mysql.connector.Error as err:
				syslog.syslog(err.msg)
			else:
				syslog.syslog("Deleted and created table.\n")
		else:
			syslog.syslog(err.msg)
	else:
		syslog.syslog("Created table {}.\n".format(args.table_name))

#If we have to truncate the Table
if args.truncate:
	try:
		syslog.syslog("Truncating table {}".format(args.table_name))
		cursor.execute(TRUNCATE)
	except mysql.connector.Error as err:
		syslog.syslog(err.msg)
	else:
		syslog.syslog("Truncated table {}.\n".format(args.table_name))

# Insert into db
ok = 0
ko = 0
syslog.syslog("Inserting Data in table {}".format(args.table_name))
for line in sys.stdin.readlines():
	if line[-1] != "\n":
		line += "} \n"
		
	try:
		jsonDictionary = json.loads(line)
	except:
		print line
	
	JsonLog = JJSON(jsonDictionary)
	
	try:
		cursor.execute(("INSERT INTO `%s` "
			"(MESSAGE, "
			"MESSAGE_ID, "
			"PRIORITY, "
			"CODE_FILE, "
			"CODE_LINE, "
			"CODE_FUNCTION, "
			"CODE_FUNC, "
			"ERRNO, "
			"SYSLOG_FACILITY, "
			"SYSLOG_IDENTIFIER, "
			"SYSLOG_PID, "
			"_PID, "
			"_UID, "
			"_GID, "
			"_COMM, "
			"_EXE, "
			"_CMDLINE, "
			"_CAP_EFFECTIVE, "
			"_AUDIT_SESSION, "
			"_AUDIT_LOGINUID, "
			"_SYSTEMD_CGROUP, "
			"_SYSTEMD_SESSION, "
			"_SYSTEMD_UNIT, "
			"_SYSTEMD_OWNER_UID, "
			"_SYSTEMD_SLICE, "
			"_SELINUX_CONTEXT, "
			"_SOURCE_REALTIME_TIMESTAMP, "
			"_BOOT_ID, "
			"_MACHINE_ID, "
			"_HOSTNAME, "
			"_TRANSPORT, "
			"_KERNEL_DEVICE, "
			"_KERNEL_SUBSYSTEM, "
			"_UDEV_SYSNAME, "
			"_UDEV_DEVNODE, "
			"_UDEV_DEVLINK, "
			"COREDUMP_UNIT, "
			"COREDUMP_USER_UNIT, "
			"OBJECT_PID, "
			"OBJECT_UID, "
			"OBJECT_GID, "
			"OBJECT_COMM, "
			"OBJECT_EXE, "
			"OBJECT_CMDLINE, "
			"OBJECT_AUDIT_SESSION, "
			"OBJECT_AUDIT_LOGINUID, "
			"OBJECT_SYSTEMD_CGROUP, "
			"OBJECT_SYSTEMD_SESSION, "
			"OBJECT_SYSTEMD_OWNER_UID, "
			"OBJECT_SYSTEMD_UNIT, "
			"OBJECT_SYSTEMD_USER_UNIT, "
			"__CURSOR, "
			"__REALTIME_TIMESTAMP, "
			"__MONOTONIC_TIMESTAMP, "
			"UNIT) "
			"VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', "
			" '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', "
			" '%s', '%s', '%s' )" % (args.table_name,
				JsonLog.MESSAGE,
				JsonLog.MESSAGE_ID,
				JsonLog.PRIORITY,
				JsonLog.CODE_FILE,
				JsonLog.CODE_LINE,
				JsonLog.CODE_FUNCTION,
				JsonLog.CODE_FUNC,
				JsonLog.ERRNO,
				JsonLog.SYSLOG_FACILITY,
				JsonLog.SYSLOG_IDENTIFIER,
				JsonLog.SYSLOG_PID,
				JsonLog._PID,
				JsonLog._UID,
				JsonLog._GID,
				JsonLog._COMM,
				JsonLog._EXE,
				JsonLog._CMDLINE,
				JsonLog._CAP_EFFECTIVE,
				JsonLog._AUDIT_SESSION,
				JsonLog._AUDIT_LOGINUID,
				JsonLog._SYSTEMD_CGROUP,
				JsonLog._SYSTEMD_SESSION,
				JsonLog._SYSTEMD_UNIT,
				JsonLog._SYSTEMD_OWNER_UID,
				JsonLog._SYSTEMD_SLICE,
				JsonLog._SELINUX_CONTEXT,
				JsonLog._SOURCE_REALTIME_TIMESTAMP,
				JsonLog._BOOT_ID,
				JsonLog._MACHINE_ID,
				JsonLog._HOSTNAME,
				JsonLog._TRANSPORT,
				JsonLog._KERNEL_DEVICE,
				JsonLog._KERNEL_SUBSYSTEM,
				JsonLog._UDEV_SYSNAME,
				JsonLog._UDEV_DEVNODE,
				JsonLog._UDEV_DEVLINK,
				JsonLog.COREDUMP_UNIT,
				JsonLog.COREDUMP_USER_UNIT,
				JsonLog.OBJECT_PID,
				JsonLog.OBJECT_UID,
				JsonLog.OBJECT_GID,
				JsonLog.OBJECT_COMM,
				JsonLog.OBJECT_EXE,
				JsonLog.OBJECT_CMDLINE,
				JsonLog.OBJECT_AUDIT_SESSION,
				JsonLog.OBJECT_AUDIT_LOGINUID,
				JsonLog.OBJECT_SYSTEMD_CGROUP,
				JsonLog.OBJECT_SYSTEMD_SESSION,
				JsonLog.OBJECT_SYSTEMD_OWNER_UID,
				JsonLog.OBJECT_SYSTEMD_UNIT,
				JsonLog.OBJECT_SYSTEMD_USER_UNIT,
				JsonLog._CURSOR,
				JsonLog._REALTIME_TIMESTAMP,
				JsonLog._MONOTONIC_TIMESTAMP,
				JsonLog.UNIT)))
	except mysql.connector.Error as err:
		syslog.syslog(err.msg)
		ko += 1
	else:
		ok += 1

# Make sure data is committed to the database
connection.commit()

# Writing end log
syslog.syslog('Inserted Data in table %s. OK: %i KO: %i' % (args.table_name, ok, ko))

# Closing connection
cursor.close()
connection.close()
