from __future__ import annotations
import os
from typing import Iterable
from cfonts import say
from enum import Enum

from src.Greeter import Greeter
from src.User import User

class Commands(Enum):
    GET_BALANCE = "Get Balance"
    GET_OWNER_ACCOUNT = "Get owner account"
    DEPLOY_CONTRACT = "Deploy the contract to the blockchain"
    CLOSE = "Close"


class CLI():

    def __init__(self) -> None:
        self.header()
        self.menu()
        
    def clean(self):
        os.system('clear')

    def header(self):
        self.clean()

        say('Greeter', colors=['yellow', '#f80'], align='center', font='block')
        say('Version 0.0.1 - Enrico Zanardo(c)', align='center', font='console', colors=['yellow'])

    
    def menu(self):

        commands = [
            Commands.GET_BALANCE,
            Commands.GET_OWNER_ACCOUNT,
            Commands.DEPLOY_CONTRACT,
            Commands.CLOSE
        ]

        for index, cmd in enumerate(commands):
            print(f"[{index + 1}] {cmd.value}")

        
        index = input("Select: ")

        match index:
            case "1":
                self.cmdGetBalance()
                return
            case "2":
                self.cmdGetAccount()
                return
            case "3":
                self.cmdDeploySmartContract()
                return
            case "4":
                self.cmdClose()
                return
            case _:
                CLI()
                return
            

    def cmdGetAccount(self):
        self.header()

        greeter = Greeter("greeter.sol")
        owner: User = greeter.get_owner_account()

        print(f"User wallet: {owner.address}")

        self.cmdBack()


    def cmdDeploySmartContract(self):
        self.header()

        greeter = Greeter("greeter.sol")
        owner: User = greeter.get_owner_account()

        greeter.deploy()

        print(f"Contract Address: {greeter.contract_address}")

        self.cmdBack()


    def cmdGetBalance(self):
        self.header()

        greeter = Greeter("greeter.sol")
        owner: User = greeter.get_owner_account()
        balance = greeter.get_balance(owner.address)
        
        print(f"Balance: {balance}")

        self.cmdBack()


    def cmdBack(self):
        retunToCLI = self.yes_or_no("Go back?")

        if (retunToCLI):
            self.header()
            self.menu()
        else:
            self.cmdClose()
        
    def yes_or_no(self, question: str):
        reply = str(input(question+' (y/n): ')).lower().strip()

        if reply[0] == 'y':
            return True
        if reply[0] == 'n':
            return False
        else:
            return self.yes_or_no("Uhhh .. please enter 'y' or 'n'")

    def cmdClose(self):
        closeCLI = self.yes_or_no("Are you sure to close the application?")

        if (not closeCLI):
            self.header()
            self.menu()
        else:
            exit()




