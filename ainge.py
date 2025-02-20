import json
import csv
import features

def fileExists(fileName):
	try:
		open(fileName.strip(), "r", encoding='utf-8-sig')
	except FileNotFoundError:
		return 0

	return 1

print("Welcome to the Ainge-BBGM CLI tool, made to make your BBGM multiplayer commissioner life just a bit easier.\n")

#Handle export: Try export.json as default, else ask for input
fileName = "export.json"
while True:
	if (fileExists(fileName)):
		with open(fileName.strip(), "r", encoding='utf-8-sig') as file:
			print("Loading export",fileName)
			export = json.load(file)
		break
	else:
		print(fileName,"does not exist.")
		fileName = input("Please enter your export's name (include .json): ")

print("\n")

while True:
	print("Currently modifying " + fileName + "...\n")
	print("Edit Options:")
	print("U. Type U to Update Export with FAs")
	print("T. Type T to Eliminate Transaction / Event")
	print("P: Type P to Print Current Standings")
	print("O: Type O to Pick Up Options")
	print("F: Type F to Update Finances")
	print("C: Type C to Cleanup Free Agents")
	print("H. Type H for Help")
	choice = input().strip().upper()

	if (choice == "U"):
		#Try decisionMatrx.csv as default, else request input
		csvName = "decisionMatrix.csv"
		while True:
			if (fileExists(csvName)):
				print("Initializing export... \n")
				with open(csvName.strip(), "r", encoding="utf-8-sig") as file:
					reader = csv.reader(file)
					#skip column headers row
					next(reader)
					decisionArr = []
					i = 0

					for row in reader:
						#ignore blank lines from csv						
						if not row == []:
							decisionArr.append(row)
							i += 1
				break
			else:
				print("No such file exists!")
				csvName = input("Please input the CSV's name (include .csv): ")

		isResign = input("Is this concerning Re-signings? If yes, type 1. If not, type 0: ")

		print("Beginning export update... \n")
		features.updateExportWithFreeAgents(isResign, decisionArr, fileName)
		break

	elif (choice == "T"):
		print("You can find the eid if you export the league and go to events.")
		eid = input("Please tell us the Event ID (eid) of the transaction to be deleted: ")

		features.deleteTransaction(eid, fileName)
		break

	elif (choice == "P"):
		discord = input("If you are printing this for Discord, type 1. If not, type 0: ")

		if int(discord):
			useAts = bool(input("Type 1 if your Discord server has team roles. If not, type 0: "))
			useEmojis = bool(input("Type 1 if your Discord server has team emojis. If not, type 0: "))

			features.printStandings(fileName, useEmojis, useAts)

		else:
			features.printStandings(fileName)

		break

	elif (choice == "O"):
		#Try options.csv as default, else ask for input
		csvName = "options.csv"
		while True:
			if (fileExists(csvName)):
				print("Initializing export... \n")
				with open(csvName.strip(), "r", encoding="utf-8-sig") as file:
					reader = csv.reader(file)
					next(reader)
					optionsArr = []

					for row in reader:
						optionsArr.append(row)
				break
			else:
				print(csvName," does not exist")
				csvName = input("Please re-input the CSV's name (include .csv): ")

		print("Beginning export update... \n")
		features.pickupOptions(optionsArr, fileName)
		break

	elif (choice == "F"):
		csvName = input("Please tell us the Option CSV's name (include .csv): ")

		while True:
			if (fileExists(csvName)):
				print("Initializing export... \n")
				with open(csvName.strip(), "r", encoding="utf-8-sig") as file:
					reader = csv.reader(file)
					next(reader)
					financesArr = []

					for row in reader:
						financesArr.append(row)
				break
			else:
				print("No such file exists!")
				csvName = input("Please re-input the CSV's name (include .csv): ")

		print("Beginning export update... \n")
		features.updateFinances(financesArr, fileName)
		break

	elif (choice == "C"):
		print("Initializing export... \n")
		print("Beginning export update... \n")
		features.cleanupFreeAgents(fileName)
		break
				
	elif (choice == "H"):
		print("You can use Ainge-BBGM to update your export or eliminate a transaction at the current moment.\n")
		print("Update Export: by typing U, you can choose to update your export with FA signings that were made.")
		print("All you need to do is include a CSV file in the same directory as Ainge-BBGM and the export ")
		print("in the specified format and simply enter its name.")
		print("The specified format is as follows: the columns must be Player Name, Team Signed With, Offer AAV, Offer Years")
		print("in that order. Each player decision should be a row; keep in mind the program will skip row one, assuming")
		print("that it will be used for headers.\n")
		print("Eliminate Transaction: by typing T, you can choose to eliminate an accidental transaction that occurred,")
		print("whether it be because of Ainge-BBGM or if you simply butterfingered a trade.")
		print("All you must do is provide Ainge-BBGM with the information about the transaction.\n")
		print("Print Standings: by typing P, Ainge-BBGM will print the current standings in the export for you.")
		print("It will also ask you if you use a Discord server, and if so, if you have team roles and/or team emojis.\n")
		print("Pick Up Options: by typing O, you can have options specified in the CSV inputted into the export")
		print("with fancy and unique transaction text that specifies that a TO or PO was picked up. The CSV must have")
		print("a header row, and each following row must be as follows: player name, type of option (TO or PO).\n")
		print("Update Finances: by typing F, you can have the finances in-game updated. The Exodus League implements")
		print("finances into its league, and each team is granted a total of 100M to allocate into coaching, facilities,")
		print("and health. Ainge-BBGM will check that teams follow this requirement and update all finances as specified")
		print("in a CSV. All teams who fail to submit will get 33/33/33. The CSV must have a header row, and then be formatted")
		print("as follows: team name, coaching budget, health budget, and then finances budget.")

input("Press ENTER to exit")