# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 10:06:43 2020

@author: gn023
"""

from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import pandas as pd


""" Selenium Block """

driver_path = "C:/Users/gn023/Desktop/Python_Scripts/Web_Parser/chromedriver.exe"

driver = webdriver.Chrome(driver_path)

driver.get("http://www.google.com")

driver.close()

driver.quit()
