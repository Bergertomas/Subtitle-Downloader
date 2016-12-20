# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 22:59:43 2016

@author: Tomas
"""

import pip

def installModules():
    pip.main(["install", "babelfish"])
    pip.main(["install", "beautifulsoup4"])
    pip.main(["install", "subliminal"])

if __name__ == '__main__':
    question = input("Do you wish to install the required modules? enter 'y' or 'n': ")
    if question == "y":
        installModules()
    else:
        exit