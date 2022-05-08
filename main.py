import subprocess
from subprocess import check_output
import pymysql

username = None
password = None

running = True

def comExit(dummy):
	global running

	running = False


def comCred(dummy):
	global username, password

	print("Enter your credentials.")
	username = input("Username: ")
	password = input("Password: ")


def comBackup(dbName):
	global username, password

	dbContent = check_output(["mysqldump", "-u" + username, "-p" + password, dbName])
	dbContent_str = dbContent.decode()

	bakFile = open(dbName + ".bak", "w")
	bakFile.write(dbContent_str)
	bakFile.close()


def comRestore(dbName):
	global username, password

	bakFile = open(dbName + ".bak", "r")
	dbContent = bakFile.read()
	bakFile.close()
	
	dbContent_arr = dbContent.split('\n')
	
	s_erver = pymysql.connect(
		host="localhost",
		user=username,
		passwd=password
	)
	c_ursor = s_erver.cursor()

	c_ursor.execute("use " + dbName + ";")
	print("Now using database {0}.".format(dbName))

	index = 0

	while index < len(dbContent_arr):
		str = dbContent_arr[index]
		str_sub = str[0:2:1]
		if (str_sub == "--") or (str_sub == "/*") or (len(str) < 1):
			dbContent_arr.pop(index)
		else:
			index += 1
	
	dbContent = ""

	for str in dbContent_arr:
		dbContent = dbContent + str

	dbContent_arr = dbContent.split(";")
	dbContent_arr.pop(len(dbContent_arr)-1)

	for str in dbContent_arr:
		c_ursor.execute(str + ";")
	
	s_erver.commit()
	c_ursor.close()
	s_erver.close()


def comHelp(dummy):
	print("""
'help' - Show this menu
'exit' - Exit the program
'backup myDB' - Back up database name to local file
'restore myDB' - Load database from local file
'cred' - Re-enter your credentials
		""")


comMap = {
	'exit': comExit,
	'cred': comCred,
	'backup': comBackup,
	'restore': comRestore,
	'help': comHelp
}


def run():
	global running, username, password

	print("Enter a command or type \"help\" for a list of commands.")

	usrin = input("> ")

	usrin_arr = usrin.split(' ')

	try:
		comMap[usrin_arr[0]](usrin_arr[1] if len(usrin_arr) > 1 else '')
	except KeyError:
		print("Unexpected token \"{0}\". Type help for a list of commands.".format(usrin_arr[0]))
	except:
		pass
	


def main():
	global running, username, password

	print("Enter your credentials.")
	username = input("Username: ")
	password = input("Password: ")

	while running:
		run()


if __name__ == "__main__":
	main()

