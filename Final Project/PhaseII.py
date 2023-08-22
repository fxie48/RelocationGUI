from pprint import pprint
import pandas as pd
import numpy as np
import sys
import re
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QHBoxLayout, QVBoxLayout, QRadioButton, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox, QTextEdit, QTableWidget, QTableWidgetItem, QPushButton
from PyQt5 import QtWebEngineWidgets
import plotly.express as px
import plotly.graph_objects as go
import emoji

def future_score():
    df = pd.read_excel("FinalData.xlsx", sheet_name = "Sheet1", header = 0)
    df["Country Name"] = df["Country Name"].str.title()
    df.set_index("Country Name", inplace = True)
    country_list = list(df.index)

    df.replace("Unknown", np.nan, inplace = True)
    df["GDP Future Percentage"] = df["GDP 20 years Prediction"]/df["GDP 20 years Prediction"].mean(axis = 0)
    df["Future Score"] = round(((df["GDP Future Percentage"]/df["GDP Future Percentage"].max(axis = 0))\
                    * (df["Vaccine Coverage 20 years Prediction"]/100)) * ((df["Employment in Service 20 years Prediction"]/100)\
                   + (df["Employment in Industry 20 years Prediction"]/100) +\
                   (df["Employment in Agriculture 20 years Prediction"]/100)) /(df["Unemployment 20 years Prediction"]/100),5)

    df.fillna("Unknown", inplace = True)

    combo_countries = []
    i = 0
    for country1 in country_list:
        i += 1
        for country2 in country_list[i:]:
            combo_countries.append([country1, country2])

    summary = []
    with open("insight5.txt", "w") as fout:
        for combo in combo_countries:
            if df.loc[combo[0], "Future Score"] == "Unknown" and df.loc[combo[1], "Future Score"] == "Unknown":
                summary.append(f"The scores of {combo[0].title()} and {combo[1].title()} cannot be calculated due to missing data. Therefore, a comparison could not be made.")
            elif df.loc[combo[0], "Future Score"] == "Unknown":
                summary.append(f"""{combo[0].title()}'s score is unknown, while {combo[1].title()} has a score of {df.loc[combo[1], "Future Score"]}. A comparison could not be made due to missing data.""")
            elif df.loc[combo[1], "Future Score"] == "Unknown":
                summary.append(f"""{combo[0].title()} has a score of {df.loc[combo[0], "Future Score"]}, while {combo[1].title()}'s score is unknown. A comparison could not be made due to missing data.""")
            elif df.loc[combo[0], "Future Score"] > df.loc[combo[1], "Future Score"]:
                summary.append(f"""{combo[0].title()}, with a score of {df.loc[combo[0], "Future Score"]}, is projected to have more beneficial characteristics in the next 20 years than {combo[1].title()}, with a score of {df.loc[combo[1], "Future Score"]}, which will collectively most likely provide you with an overall higher standard of living.""")
            elif df.loc[combo[0], "Future Score"] < df.loc[combo[1], "Future Score"]:
                summary.append(f"""{combo[1].title()}, with a score of {df.loc[combo[1], "Future Score"]}, is projected to have more beneficial characteristics in the next 20 years than {combo[0].title()}, with a score of {df.loc[combo[0], "Future Score"]}, which will collectively most likely provide you with an overall higher standard of living.""")
            elif df.loc[combo[0], "Future Score"] == df.loc[combo[1], "Future Score"]:
                summary.append(f"""{combo[0].title()} and {combo[1].title()}, both with a score of {df.loc[combo[0], "Future Score"]}, have an equal number of beneficial qualities within the 50 year projection. Please refer to the information provided to determine which characteristics are of more importance to you when deciding where to move.""")
        for entry in summary:
            print(entry, file = fout)
    return df

def current_country():
    df = pd.read_excel("FinalData.xlsx", sheet_name = "Sheet1", header = 0)
    df["Country Name"] = df["Country Name"].str.title()
    df.set_index("Country Name", inplace = True)
    country_list = list(df.index)

    df.replace("Unknown", np.nan, inplace = True)
    df["GDP Percentage 2019"] = df["2019 GDP"]/df["2019 GDP"].mean(axis = 0)
    df["Current Score"] = round(((df["GDP Percentage 2019"]/df["GDP Percentage 2019"].max(axis = 0))\
                    * (df[2019]/100)) * ((df["Employment in Services 2020 (% of employed)"]/100)\
                   + (df["Employment in Industry 2020 (% of employed)"]/100) +\
                   (df["Employment in Agriculture 2020 (% of employed)"]/100)) /(df["2019 Unemployment"]/100),5)

    df.fillna("Unknown", inplace = True)

    combo_countries = []
    i = 0
    for country1 in country_list:
        i += 1
        for country2 in country_list[i:]:
            combo_countries.append([country1, country2])

    summary = []
    with open("insight6.txt", "w") as fout:
        for combo in combo_countries:
            if df.loc[combo[0], "Current Score"] == "Unknown" and df.loc[combo[1], "Current Score"] == "Unknown":
                summary.append(f"The scores of {combo[0].title()} and {combo[1].title()} cannot be calculated due to missing data. Therefore, a comparison could not be made.")
            elif df.loc[combo[0], "Current Score"] == "Unknown":
                summary.append(f"""{combo[0].title()}'s score is unknown, while {combo[1].title()} has a score of {df.loc[combo[1], "Current Score"]}. A comparison could not be made due to missing data.""")
            elif df.loc[combo[1], "Current Score"] == "Unknown":
                summary.append(f"""{combo[0].title()} has a score of {df.loc[combo[0], "Current Score"]}, while {combo[1].title()}'s score is unknown. A comparison could not be made due to missing data.""")
            elif df.loc[combo[0], "Current Score"] > df.loc[combo[1], "Current Score"]:
                summary.append(f"""{combo[0].title()}, with a score of {df.loc[combo[0], "Current Score"]}, as of 2019, has more beneficial characteristics  {combo[1].title()}, with a score of {df.loc[combo[1], "Current Score"]}, which will collectively most likely provide you with an overall higher standard of living.""")
            elif df.loc[combo[0], "Current Score"] < df.loc[combo[1], "Current Score"]:
                summary.append(f"""{combo[1].title()}, with a score of {df.loc[combo[1], "Current Score"]}, as of 2019, has more beneficial characteristics {combo[0].title()}, with a score of {df.loc[combo[0], "Current Score"]}, which will collectively most likely provide you with an overall higher standard of living.""")
            elif df.loc[combo[0], "Current Score"] == df.loc[combo[1], "Current Score"]:
                summary.append(f"""{combo[0].title()} and {combo[1].title()}, both with a score of {df.loc[combo[0], "Current Score"]}, have an equal number of beneficial qualities, as of 2019. Please refer to the information provided to determine which characteristics are of more importance to you when deciding where to move.""")
        for entry in summary:
            print(entry, file = fout)
    return df



#GUI
class CompareTwoWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Comparing 2 Countries")
        width = 1200
        self.setFixedWidth(width)
        height = 800
        self.setFixedHeight(height)

        vbox1 = QVBoxLayout()

        hbox1 = QHBoxLayout()
        self.textbox1 = QLineEdit()
        self.textbox1.textEdited.connect(self.country_entered)
        self.label1 = QLabel("Country 1:")
        self.label1.setBuddy(self.textbox1)
        self.textbox2 = QLineEdit()
        self.textbox2.textEdited.connect(self.country_entered)
        self.label2 = QLabel("Country 2:")
        self.label2.setBuddy(self.textbox2)
        hbox1.addWidget(self.label1)
        hbox1.addWidget(self.textbox1)
        hbox1.addWidget(self.label2)
        hbox1.addWidget(self.textbox2)

        vbox = QVBoxLayout()
        self.label3 = QLabel("*note that the U.S. must be entered as United States of America*")
        vbox.addWidget(self.label3)

        vbox2 = QVBoxLayout()
        self.button1 = QPushButton("Compare")
        self.button1.setEnabled(False)
        self.button1.clicked.connect(self.compare_clicked)
        vbox2.addWidget(self.button1)


        hbox2 = QHBoxLayout()
        self.textbox4 = QTextEdit()
        self.textbox4.setReadOnly(True)

        vbox4 = QVBoxLayout()
        self.table1label = QLabel("2019 Data")
        self.table2label = QLabel("Future Projection (20 Years)")
        self.table = QTableWidget()
        self.table.setRowCount(2)
        self.table.setColumnCount(9)

        self.table.setColumnWidth(1, 200)
        self.table.setColumnWidth(2, 200)
        self.table.setColumnWidth(3, 200)
        self.table.setColumnWidth(4, 200)
        self.table.setColumnWidth(5, 200)
        self.table.setColumnWidth(6, 200)
        self.table.setColumnWidth(7, 200)
        self.table.setColumnWidth(8, 200)
        self.table.setRowHeight(1, 100)
        self.table.setRowHeight(2, 100)
        self.table.setRowHeight(0,50)

        self.table2 = QTableWidget()
        self.table2.setRowCount(2)
        self.table2.setColumnCount(9)

        self.table2.setColumnWidth(1, 200)
        self.table2.setColumnWidth(2, 200)
        self.table2.setColumnWidth(3, 200)
        self.table2.setColumnWidth(4, 200)
        self.table2.setColumnWidth(5, 200)
        self.table2.setColumnWidth(6, 200)
        self.table2.setColumnWidth(7, 200)
        self.table2.setColumnWidth(8, 200)
        self.table2.setRowHeight(1, 100)
        self.table2.setRowHeight(2, 100)
        self.table2.setRowHeight(0,50)

        vbox4.addWidget(self.table1label)
        vbox4.addWidget(self.table)
        vbox4.addWidget(self.table2label)
        vbox4.addWidget(self.table2)

        hbox2.addLayout(vbox4)
        hbox2.addWidget(self.textbox4)

        vbox3 = QVBoxLayout()
        self.textbox5 = QLineEdit()
        self.textbox5.setReadOnly(True)
        self.label4 = QLabel("Recommended country to move to in 20 years:")
        self.textbox6 = QLineEdit()
        self.textbox6.setReadOnly(True)
        self.label5 = QLabel("Recommended country to move to now (2019):")
        vbox3.addWidget(self.label4)
        vbox3.addWidget(self.textbox5)
        vbox3.addWidget(self.label5)
        vbox3.addWidget(self.textbox6)

        vbox1.addLayout(hbox1)
        vbox1.addLayout(vbox)
        vbox1.addLayout(vbox2)
        vbox1.addLayout(hbox2)
        vbox1.addLayout(vbox3)

        self.setLayout(vbox1)


    def country_entered(self):
        if self.textbox1.text() and self.textbox2.text():
            self.button1.setEnabled(True)
            self.textbox4.clear()
            self.table.clear()
            self.textbox5.clear()
            self.table2.clear()
            self.textbox6.clear()
        if self.textbox1.text() == "" or self.textbox2.text() == "":
            self.button1.setEnabled(False)
            self.textbox4.clear()
            self.table.clear()
            self.textbox5.clear()
            self.table2.clear()
            self.textbox6.clear()

    def compare_clicked(self):
        df = pd.read_excel("FinalData.xlsx", sheet_name = "Sheet1", index_col = 0, header = 0)
        countries = list(df.index)
        if (self.textbox1.text().lower() in countries and self.textbox2.text().lower() in countries) and (self.textbox1.text().lower() != self.textbox2.text().lower()):

            try:
                if float(df.loc[self.textbox2.text().lower(), "Unemployment 20 years Prediction"]) < float(df.loc[self.textbox1.text().lower(), "Unemployment 20 years Prediction"]):
                    self.textbox4.append(f'Unemployment relative change in {self.textbox1.text().lower().title()}: {round(df.loc[self.textbox1.text().lower(), "Unemployment Average Relative Change"],5)}%\n\nUsing this calculated relative change, {self.textbox2.text().lower().title()} is predicted to have less unemployment in 20 years.\n\n')
                if float(df.loc[self.textbox2.text().lower(), "Unemployment 20 years Prediction"]) > float(df.loc[self.textbox1.text().lower(), "Unemployment 20 years Prediction"]):
                    self.textbox4.append(f'Unemployment relative change in {self.textbox1.text().lower().title()}: {round(df.loc[self.textbox1.text().lower(), "Unemployment Average Relative Change"],5)}%\n\nUsing this calculated relative change, {self.textbox1.text().lower().title()} is predicted to have less unemployment in 20 years.\n\n')
            except:
                self.textbox4.append(f'Relative change in unemployment in {self.textbox1.text().lower().title()}: {df.loc[self.textbox1.text().lower(), "Unemployment Average Relative Change"]}\n\nIn contrast, the relative change of unemployment in {self.textbox2.text().lower().title()} is {df.loc[self.textbox2.text().lower(), "Unemployment Average Relative Change"]}. It can not be predicted which country would have less unemployment in 20 years.\n\n')
            #self.textbox1.text().lower() has higher agricultural, higher service, higher industrial
            if (df.loc[self.textbox1.text().lower(), "Employment in Agriculture 20 years Prediction"] > df.loc[self.textbox2.text().lower(), "Employment in Agriculture 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Service 20 years Prediction"] > df.loc[self.textbox2.text().lower(), "Employment in Service 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Industry 20 years Prediction"] > df.loc[self.textbox2.text().lower(), "Employment in Industry 20 years Prediction"]):
                self.textbox4.append(f'The calculated relative change for employment in agriculture, industry, and services for {self.textbox1.text().lower().title()} is:\nAgriculture: {round(df.loc[self.textbox1.text().lower(), "Agriculture Employment Average Relative Change"], 5)}%\nIndustry: {round(df.loc[self.textbox1.text().lower(), "Industry Employment Average Relative Change"],5)}%\nService: {round(df.loc[self.textbox1.text().lower(), "Services Employment Average Relative Change"],5)}%\n\nIn contrast, the calculated relative change for employment in agriculture, industry, and services for {self.textbox2.text().lower().title()} is:\nAgriculture: {round(df.loc[self.textbox2.text().lower(), "Agriculture Employment Average Relative Change"],5)}%\nIndustry: {round(df.loc[self.textbox2.text().lower(), "Industry Employment Average Relative Change"],5)}%\nServices: {round(df.loc[self.textbox2.text().lower(), "Services Employment Average Relative Change"],5)}%\n\nUsing this relative change trend, it has been calculated that {self.textbox1.text().lower().title()} is predicted to have higher agricultural, service, and industrial employment than the {self.textbox2.text().lower().title()} in 20 years.\n\n')
            #self.textbox1.text().lower() has higher agricultural, higher service, lower industrial
            elif (df.loc[self.textbox1.text().lower(), "Employment in Agriculture 20 years Prediction"] > df.loc[self.textbox2.text().lower(), "Employment in Agriculture 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Service 20 years Prediction"] > df.loc[self.textbox2.text().lower(), "Employment in Service 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Industry 20 years Prediction"] < df.loc[self.textbox2.text().lower(), "Employment in Industry 20 years Prediction"]):
                self.textbox4.append(f'The calculated relative change for employment in agriculture, industry, and services for {self.textbox1.text().lower().title()} is:\nAgriculture: {round(df.loc[self.textbox1.text().lower(), "Agriculture Employment Average Relative Change"], 5)}%\nIndustry: {round(df.loc[self.textbox1.text().lower(), "Industry Employment Average Relative Change"],5)}%\nService: {round(df.loc[self.textbox1.text().lower(), "Services Employment Average Relative Change"],5)}%\n\nIn contrast, the calculated relative change for employment in agriculture, industry, and services for {self.textbox2.text().lower().title()} is:\nAgriculture: {round(df.loc[self.textbox2.text().lower(), "Agriculture Employment Average Relative Change"],5)}%\nIndustry: {round(df.loc[self.textbox2.text().lower(), "Industry Employment Average Relative Change"],5)}%\nServices: {round(df.loc[self.textbox2.text().lower(), "Services Employment Average Relative Change"],5)}%\n\nUsing this relative change trend, it has been calculated that {self.textbox1.text().lower().title()} is predicted to have higher agricultural and service employments, but lower industrial employment than the {self.textbox2.text().lower().title()} in 20 years.\n\n')
            #self.textbox1.text().lower() has higher agricultural, lower service, lower industrial
            elif (df.loc[self.textbox1.text().lower(), "Employment in Agriculture 20 years Prediction"] > df.loc[self.textbox2.text().lower(), "Employment in Agriculture 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Service 20 years Prediction"] < df.loc[self.textbox2.text().lower(), "Employment in Service 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Industry 20 years Prediction"] < df.loc[self.textbox2.text().lower(), "Employment in Industry 20 years Prediction"]):
                self.textbox4.append(f'The calculated relative change for employment in agriculture, industry, and services for {self.textbox1.text().lower().title()} is:\nAgriculture: {round(df.loc[self.textbox1.text().lower(), "Agriculture Employment Average Relative Change"], 5)}%\nIndustry: {round(df.loc[self.textbox1.text().lower(), "Industry Employment Average Relative Change"],5)}%\nService: {round(df.loc[self.textbox1.text().lower(), "Services Employment Average Relative Change"],5)}%\n\nIn contrast, the calculated relative change for employment in agriculture, industry, and services for {self.textbox2.text().lower().title()} is:\nAgriculture: {round(df.loc[self.textbox2.text().lower(), "Agriculture Employment Average Relative Change"],5)}%\nIndustry: {round(df.loc[self.textbox2.text().lower(), "Industry Employment Average Relative Change"],5)}%\nServices: {round(df.loc[self.textbox2.text().lower(), "Services Employment Average Relative Change"],5)}%\n\nUsing this relative change trend, it has been calculated that {self.textbox1.text().lower().title()} is predicted to have higher agricultural employment, but lower industrial and service employments than the {self.textbox2.text().lower().title()} in 20 years.\n\n')
            #self.textbox1.text().lower() has higher agricultural, lower service, higher industrial
            elif (df.loc[self.textbox1.text().lower(), "Employment in Agriculture 20 years Prediction"] > df.loc[self.textbox2.text().lower(), "Employment in Agriculture 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Service 20 years Prediction"] < df.loc[self.textbox2.text().lower(), "Employment in Service 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Industry 20 years Prediction"] > df.loc[self.textbox2.text().lower(), "Employment in Industry 20 years Prediction"]):
                self.textbox4.append(f'The calculated relative change for employment in agriculture, industry, and services for {self.textbox1.text().lower().title()} is:\nAgriculture: {round(df.loc[self.textbox1.text().lower(), "Agriculture Employment Average Relative Change"], 5)}%\nIndustry: {round(df.loc[self.textbox1.text().lower(), "Industry Employment Average Relative Change"],5)}%\nService: {round(df.loc[self.textbox1.text().lower(), "Services Employment Average Relative Change"],5)}%\n\nIn contrast, the calculated relative change for employment in agriculture, industry, and services for {self.textbox2.text().lower().title()} is:\nAgriculture: {round(df.loc[self.textbox2.text().lower(), "Agriculture Employment Average Relative Change"],5)}%\nIndustry: {round(df.loc[self.textbox2.text().lower(), "Industry Employment Average Relative Change"],5)}%\nServices: {round(df.loc[self.textbox2.text().lower(), "Services Employment Average Relative Change"],5)}%\n\nUsing this relative change trend, it has been calculated that {self.textbox1.text().lower().title()} is predicted to have higher agricultural and industrial employments, but lower service employment than the {self.textbox2.text().lower().title()} in 20 years.\n\n')
            #higher service, higher industrial, lower agriculture
            elif (df.loc[self.textbox1.text().lower(), "Employment in Service 20 years Prediction"] > df.loc[self.textbox2.text().lower(), "Employment in Service 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Agriculture 20 years Prediction"] < df.loc[self.textbox2.text().lower(), "Employment in Agriculture 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Industry 20 years Prediction"] > df.loc[self.textbox2.text().lower(), "Employment in Industry 20 years Prediction"]):
                self.textbox4.append(f'The calculated relative change for employment in agriculture, industry, and services for {self.textbox1.text().lower().title()} is:\nAgriculture: {round(df.loc[self.textbox1.text().lower(), "Agriculture Employment Average Relative Change"], 5)}%\nIndustry: {round(df.loc[self.textbox1.text().lower(), "Industry Employment Average Relative Change"],5)}%\nService: {round(df.loc[self.textbox1.text().lower(), "Services Employment Average Relative Change"],5)}%\n\nIn contrast, the calculated relative change for employment in agriculture, industry, and services for {self.textbox2.text().lower().title()} is:\nAgriculture: {round(df.loc[self.textbox2.text().lower(), "Agriculture Employment Average Relative Change"],5)}%\nIndustry: {round(df.loc[self.textbox2.text().lower(), "Industry Employment Average Relative Change"],5)}%\nServices: {round(df.loc[self.textbox2.text().lower(), "Services Employment Average Relative Change"],5)}%\n\nUsing this relative change trend, it has been calculated that {self.textbox1.text().lower().title()} is predicted to have higher service and industrial employments, but lower agricultural employment than the {self.textbox2.text().lower().title()} in 20 years.\n\n')
            #higher service, lower industrial, lower agricultural
            elif (df.loc[self.textbox1.text().lower(), "Employment in Service 20 years Prediction"] > df.loc[self.textbox2.text().lower(), "Employment in Service 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Agriculture 20 years Prediction"] < df.loc[self.textbox2.text().lower(), "Employment in Agriculture 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Industry 20 years Prediction"] < df.loc[self.textbox2.text().lower(), "Employment in Industry 20 years Prediction"]):
                self.textbox4.append(f'The calculated relative change for employment in agriculture, industry, and services for {self.textbox1.text().lower().title()} is:\nAgriculture: {round(df.loc[self.textbox1.text().lower(), "Agriculture Employment Average Relative Change"], 5)}%\nIndustry: {round(df.loc[self.textbox1.text().lower(), "Industry Employment Average Relative Change"],5)}%\nService: {round(df.loc[self.textbox1.text().lower(), "Services Employment Average Relative Change"],5)}%\n\nIn contrast, the calculated relative change for employment in agriculture, industry, and services for {self.textbox2.text().lower().title()} is:\nAgriculture: {round(df.loc[self.textbox2.text().lower(), "Agriculture Employment Average Relative Change"],5)}%\nIndustry: {round(df.loc[self.textbox2.text().lower(), "Industry Employment Average Relative Change"],5)}%\nServices: {round(df.loc[self.textbox2.text().lower(), "Services Employment Average Relative Change"],5)}%\n\nUsing this relative change trend, it has been calculated that {self.textbox1.text().lower().title()} is predicted to have higher service employment, but lower industrial and agricultural employments than the {self.textbox2.text().lower().title()} in 20 years.\n\n')
            #higher industrial, lower service, lower agricultural
            elif (df.loc[self.textbox1.text().lower(), "Employment in Service 20 years Prediction"] < df.loc[self.textbox2.text().lower(), "Employment in Service 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Agriculture 20 years Prediction"] < df.loc[self.textbox2.text().lower(), "Employment in Agriculture 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Industry 20 years Prediction"] > df.loc[self.textbox2.text().lower(), "Employment in Industry 20 years Prediction"]):
                    self.textbox4.append(f'The calculated relative change for employment in agriculture, industry, and services for {self.textbox1.text().lower().title()} is:\nAgriculture: {round(df.loc[self.textbox1.text().lower(), "Agriculture Employment Average Relative Change"], 5)}%\nIndustry: {round(df.loc[self.textbox1.text().lower(), "Industry Employment Average Relative Change"],5)}%\nService: {round(df.loc[self.textbox1.text().lower(), "Services Employment Average Relative Change"],5)}%\n\nIn contrast, the calculated relative change for employment in agriculture, industry, and services for {self.textbox2.text().lower().title()} is:\nAgriculture: {round(df.loc[self.textbox2.text().lower(), "Agriculture Employment Average Relative Change"],5)}%\nIndustry: {round(df.loc[self.textbox2.text().lower(), "Industry Employment Average Relative Change"],5)}%\nServices: {round(df.loc[self.textbox2.text().lower(), "Services Employment Average Relative Change"],5)}%\n\nUsing this relative change trend, it has been calculated that {self.textbox1.text().lower().title()} is predicted to have higher industrial employment, but lower service and agricultural employments than the {self.textbox2.text().lower().title()} in 20 years than.\n\n')
            #lower industrial, lower service, lower agricultural
            elif (df.loc[self.textbox1.text().lower(), "Employment in Service 20 years Prediction"] < df.loc[self.textbox2.text().lower(), "Employment in Service 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Agriculture 20 years Prediction"] < df.loc[self.textbox2.text().lower(), "Employment in Agriculture 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Industry 20 years Prediction"] < df.loc[self.textbox2.text().lower(), "Employment in Industry 20 years Prediction"]):
                    self.textbox4.append(f'The calculated relative change for employment in agriculture, industry, and services for {self.textbox1.text().lower().title()} is:\nAgriculture: {round(df.loc[self.textbox1.text().lower(), "Agriculture Employment Average Relative Change"], 5)}%\nIndustry: {round(df.loc[self.textbox1.text().lower(), "Industry Employment Average Relative Change"],5)}%\nService: {round(df.loc[self.textbox1.text().lower(), "Services Employment Average Relative Change"],5)}%\n\nIn contrast, the calculated relative change for employment in agriculture, industry, and services for {self.textbox2.text().lower().title()} is:\nAgriculture: {round(df.loc[self.textbox2.text().lower(), "Agriculture Employment Average Relative Change"],5)}%\nIndustry: {round(df.loc[self.textbox2.text().lower(), "Industry Employment Average Relative Change"],5)}%\nServices: {round(df.loc[self.textbox2.text().lower(), "Services Employment Average Relative Change"],5)}%\n\nUsing this relative change trend, it has been calculated that {self.textbox1.text().lower().title()} is predicted to have lower industrial, service and agricultural employments than the {self.textbox2.text().lower().title()} in 20 years.\n\n')
            #country 1 has lower industrial, lower service, equal agriculture
            elif (df.loc[self.textbox1.text().lower(), "Employment in Service 20 years Prediction"] < df.loc[self.textbox2.text().lower(), "Employment in Service 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Agriculture 20 years Prediction"] == df.loc[self.textbox2.text().lower(), "Employment in Agriculture 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Industry 20 years Prediction"] < df.loc[self.textbox2.text().lower(), "Employment in Industry 20 years Prediction"]):
                    self.textbox4.append(f'The calculated relative change for employment in agriculture, industry, and services for {self.textbox1.text().lower().title()} is:\nAgriculture: {round(df.loc[self.textbox1.text().lower(), "Agriculture Employment Average Relative Change"], 5)}%\nIndustry: {round(df.loc[self.textbox1.text().lower(), "Industry Employment Average Relative Change"],5)}%\nService: {round(df.loc[self.textbox1.text().lower(), "Services Employment Average Relative Change"],5)}%\n\nIn contrast, the calculated relative change for employment in agriculture, industry, and services for {self.textbox2.text().lower().title()} is:\nAgriculture: {round(df.loc[self.textbox2.text().lower(), "Agriculture Employment Average Relative Change"],5)}%\nIndustry: {round(df.loc[self.textbox2.text().lower(), "Industry Employment Average Relative Change"],5)},\nServices: {round(df.loc[self.textbox2.text().lower(), "Services Employment Average Relative Change"],5)}%\n\nUsing this relative change trend, it has been calculated that {self.textbox1.text().lower().title()} is predicted to have equal agricultural employments as {self.textbox2.text().lower().title()}, but lower service and industrial employments than {self.textbox2.text().lower().title()} in 20 years.')
            #country 1 has lower industrial, higher service, equal agriculture
            elif (df.loc[self.textbox1.text().lower(), "Employment in Service 20 years Prediction"] > df.loc[self.textbox2.text().lower(), "Employment in Service 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Agriculture 20 years Prediction"] == df.loc[self.textbox2.text().lower(), "Employment in Agriculture 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Industry 20 years Prediction"] < df.loc[self.textbox2.text().lower(), "Employment in Industry 20 years Prediction"]):
                    self.textbox4.append(f'The calculated relative change for employment in agriculture, industry, and services for {self.textbox1.text().lower().title()} is:\nAgriculture: {round(df.loc[self.textbox1.text().lower(), "Agriculture Employment Average Relative Change"], 5)}%\nIndustry: {round(df.loc[self.textbox1.text().lower(), "Industry Employment Average Relative Change"],5)}%\nService: {round(df.loc[self.textbox1.text().lower(), "Services Employment Average Relative Change"],5)}%\n\nIn contrast, the calculated relative change for employment in agriculture, industry, and services for {self.textbox2.text().lower().title()} is:\nAgriculture: {round(df.loc[self.textbox2.text().lower(), "Agriculture Employment Average Relative Change"],5)}%\nIndustry: {round(df.loc[self.textbox2.text().lower(), "Industry Employment Average Relative Change"],5)}\nServices: {round(df.loc[self.textbox2.text().lower(), "Services Employment Average Relative Change"],5)}%\n\nUsing this relative change trend, it has been calculated that {self.textbox1.text().lower().title()} is predicted to have equal agricultural employments as {self.textbox2.text().lower().title()}, but higher service employments and lower industrial employments than {self.textbox2.text().lower().title()} in 20 years.')
            #country 1 has higher industrial, lower service, equal agriculture
            elif (df.loc[self.textbox1.text().lower(), "Employment in Service 20 years Prediction"] < df.loc[self.textbox2.text().lower(), "Employment in Service 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Agriculture 20 years Prediction"] == df.loc[self.textbox2.text().lower(), "Employment in Agriculture 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Industry 20 years Prediction"] > df.loc[self.textbox2.text().lower(), "Employment in Industry 20 years Prediction"]):
                    self.textbox4.append(f'The calculated relative change for employment in agriculture, industry, and services for {self.textbox1.text().lower().title()} is:\nAgriculture: {round(df.loc[self.textbox1.text().lower(), "Agriculture Employment Average Relative Change"], 5)}%\nIndustry: {round(df.loc[self.textbox1.text().lower(), "Industry Employment Average Relative Change"],5)}%\nService: {round(df.loc[self.textbox1.text().lower(), "Services Employment Average Relative Change"],5)}%\n\nIn contrast, the calculated relative change for employment in agriculture, industry, and services for {self.textbox2.text().lower().title()} is:\nAgriculture: {round(df.loc[self.textbox2.text().lower(), "Agriculture Employment Average Relative Change"],5)}%\nIndustry: {round(df.loc[self.textbox2.text().lower(), "Industry Employment Average Relative Change"],5)}\nServices: {round(df.loc[self.textbox2.text().lower(), "Services Employment Average Relative Change"],5)}%\n\nUsing this relative change trend, it has been calculated that {self.textbox1.text().lower().title()} is predicted to have equal agricultural employments as {self.textbox2.text().lower().title()}, but lower service employments and higher industrial employments than {self.textbox2.text().lower().title()} in 20 years.')
            #country 1 has higher industrial, higher service, equal agriculture
            elif (df.loc[self.textbox1.text().lower(), "Employment in Service 20 years Prediction"] > df.loc[self.textbox2.text().lower(), "Employment in Service 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Agriculture 20 years Prediction"] == df.loc[self.textbox2.text().lower(), "Employment in Agriculture 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Industry 20 years Prediction"] > df.loc[self.textbox2.text().lower(), "Employment in Industry 20 years Prediction"]):
                    self.textbox4.append(f'The calculated relative change for employment in agriculture, industry, and services for {self.textbox1.text().lower().title()} is:\nAgriculture: {round(df.loc[self.textbox1.text().lower(), "Agriculture Employment Average Relative Change"], 5)}%\nIndustry: {round(df.loc[self.textbox1.text().lower(), "Industry Employment Average Relative Change"],5)}%\nService: {round(df.loc[self.textbox1.text().lower(), "Services Employment Average Relative Change"],5)}%\n\nIn contrast, the calculated relative change for employment in agriculture, industry, and services for {self.textbox2.text().lower().title()} is:\nAgriculture: {round(df.loc[self.textbox2.text().lower(), "Agriculture Employment Average Relative Change"],5)}%\nIndustry: {round(df.loc[self.textbox2.text().lower(), "Industry Employment Average Relative Change"],5)}\nServices: {round(df.loc[self.textbox2.text().lower(), "Services Employment Average Relative Change"],5)}%\n\nUsing this relative change trend, it has been calculated that {self.textbox1.text().lower().title()} is predicted to have equal agricultural employments as {self.textbox2.text().lower().title()}, but higher service and industrial employments than {self.textbox2.text().lower().title()} in 20 years.')
            #country 1 has equal industrial, lower service, higher agriculture
            elif (df.loc[self.textbox1.text().lower(), "Employment in Service 20 years Prediction"] < df.loc[self.textbox2.text().lower(), "Employment in Service 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Agriculture 20 years Prediction"] > df.loc[self.textbox2.text().lower(), "Employment in Agriculture 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Industry 20 years Prediction"] == df.loc[self.textbox2.text().lower(), "Employment in Industry 20 years Prediction"]):
                    self.textbox4.append(f'The calculated relative change for employment in agriculture, industry, and services for {self.textbox1.text().lower().title()} is:\nAgriculture: {round(df.loc[self.textbox1.text().lower(), "Agriculture Employment Average Relative Change"], 5)}%\nIndustry: {round(df.loc[self.textbox1.text().lower(), "Industry Employment Average Relative Change"],5)}%\nService: {round(df.loc[self.textbox1.text().lower(), "Services Employment Average Relative Change"],5)}%\n\nIn contrast, the calculated relative change for employment in agriculture, industry, and services for {self.textbox2.text().lower().title()} is:\nAgriculture: {round(df.loc[self.textbox2.text().lower(), "Agriculture Employment Average Relative Change"],5)}%\nIndustry: {round(df.loc[self.textbox2.text().lower(), "Industry Employment Average Relative Change"],5)}\nServices: {round(df.loc[self.textbox2.text().lower(), "Services Employment Average Relative Change"],5)}%\n\nUsing this relative change trend, it has been calculated that {self.textbox1.text().lower().title()} is predicted to have equal industrial employments as {self.textbox2.text().lower().title()}, but lower service and higher agricultural employments than {self.textbox2.text().lower().title()} in 20 years.')
            #country 1 has equal industrial, higher service, lower agriculture
            elif (df.loc[self.textbox1.text().lower(), "Employment in Service 20 years Prediction"] > df.loc[self.textbox2.text().lower(), "Employment in Service 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Agriculture 20 years Prediction"] < df.loc[self.textbox2.text().lower(), "Employment in Agriculture 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Industry 20 years Prediction"] == df.loc[self.textbox2.text().lower(), "Employment in Industry 20 years Prediction"]):
                    self.textbox4.append(f'The calculated relative change for employment in agriculture, industry, and services for {self.textbox1.text().lower().title()} is:\nAgriculture: {round(df.loc[self.textbox1.text().lower(), "Agriculture Employment Average Relative Change"], 5)}%\nIndustry: {round(df.loc[self.textbox1.text().lower(), "Industry Employment Average Relative Change"],5)}\nService: {round(df.loc[self.textbox1.text().lower(), "Services Employment Average Relative Change"],5)}%\n\nIn contrast, the calculated relative change for employment in agriculture, industry, and services for {self.textbox2.text().lower().title()} is:\nAgriculture: {round(df.loc[self.textbox2.text().lower(), "Agriculture Employment Average Relative Change"],5)}%\nIndustry: {round(df.loc[self.textbox2.text().lower(), "Industry Employment Average Relative Change"],5)}\nServices: {round(df.loc[self.textbox2.text().lower(), "Services Employment Average Relative Change"],5)}%\n\nUsing this relative change trend, it has been calculated that {self.textbox1.text().lower().title()} is predicted to have equal industrial employments as {self.textbox2.text().lower().title()}, but higher service and lower agricultural employments than {self.textbox2.text().lower().title()} in 20 years.')
            #country 1 has equal industrial, lower service, lower agriculture
            elif (df.loc[self.textbox1.text().lower(), "Employment in Service 20 years Prediction"] < df.loc[self.textbox2.text().lower(), "Employment in Service 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Agriculture 20 years Prediction"] < df.loc[self.textbox2.text().lower(), "Employment in Agriculture 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Industry 20 years Prediction"] == df.loc[self.textbox2.text().lower(), "Employment in Industry 20 years Prediction"]):
                    self.textbox4.append(f'The calculated relative change for employment in agriculture, industry, and services for {self.textbox1.text().lower().title()} is:\nAgriculture: {round(df.loc[self.textbox1.text().lower(), "Agriculture Employment Average Relative Change"],5)}%\nIndustry: {round(df.loc[self.textbox1.text().lower(), "Industry Employment Average Relative Change"],5)}\nService: {round(df.loc[self.textbox1.text().lower(), "Services Employment Average Relative Change"],5)}%\n\nIn contrast, the calculated relative change for employment in agriculture, industry, and services for {self.textbox2.text().lower().title()} is:\nAgriculture: {round(df.loc[self.textbox2.text().lower(), "Agriculture Employment Average Relative Change"],5)}%\nIndustry: {round(df.loc[self.textbox2.text().lower(), "Industry Employment Average Relative Change"],5)}\nServices: {round(df.loc[self.textbox2.text().lower(), "Services Employment Average Relative Change"])}%\n\nUsing this relative change trend, it has been calculated that {self.textbox1.text().lower().title()} is predicted to have equal industrial employments as {self.textbox2.text().lower().title()}, but lower service and agricultural employments than {self.textbox2.text().lower().title()} in 20 years.')
            #country 1 has equal industrial, higher service, higher agriculture
            elif (df.loc[self.textbox1.text().lower(), "Employment in Service 20 years Prediction"] > df.loc[self.textbox2.text().lower(), "Employment in Service 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Agriculture 20 years Prediction"] > df.loc[self.textbox2.text().lower(), "Employment in Agriculture 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Industry 20 years Prediction"] == df.loc[self.textbox2.text().lower(), "Employment in Industry 20 years Prediction"]):
                    self.textbox4.append(f'The calculated relative change for employment in agriculture, industry, and services for {self.textbox1.text().lower().title()} is:\nAgriculture: {round(df.loc[self.textbox1.text().lower(), "Agriculture Employment Average Relative Change"],5)}%\nIndustry: {round(df.loc[self.textbox1.text().lower(), "Industry Employment Average Relative Change"],5)}\nService: {round(df.loc[self.textbox1.text().lower(), "Services Employment Average Relative Change"],5)}%\n\nIn contrast, the calculated relative change for employment in agriculture, industry, and services for {self.textbox2.text().lower().title()} is:\nAgriculture: {round(df.loc[self.textbox2.text().lower(), "Agriculture Employment Average Relative Change"],5)}%\nIndustry: {round(df.loc[self.textbox2.text().lower(), "Industry Employment Average Relative Change"],5)}\nServices: {round(df.loc[self.textbox2.text().lower(), "Services Employment Average Relative Change"])}%\n\nUsing this relative change trend, it has been calculated that {self.textbox1.text().lower().title()} is predicted to have equal industrial employments as {self.textbox2.text().lower().title()}, but higher service and agricultural employments than {self.textbox2.text().lower().title()} in 20 years.')

            self.textbox4.append(f'{self.textbox1.text().lower().title()} has an exchange rate of {df.loc[self.textbox1.text().lower(), "Exchange Currency (per US $)"]} per U.S. dollar.\n\n')

            try:
                if float(df.loc[self.textbox2.text().lower(), "Vaccine Coverage 20 years Prediction"]) < float(df.loc[self.textbox1.text().lower(), "Vaccine Coverage 20 years Prediction"]):
                    self.textbox4.append(f'The vaccine coverage relative change in {self.textbox1.text().lower().title()} is {round(df.loc[self.textbox1.text().lower(), "Coverage Average Relative Change"],5)}% {self.textbox1.text().lower().title()}\'s average vaccine coverage relative change is higher than the {round(df.loc[self.textbox2.text().lower(), "Coverage Average Relative Change"],5)}% average vaccine coverage relative change in {self.textbox2.text().lower().title()}. Using this calculated relative change, {self.textbox2.text().lower().title()} is predicted to have less vaccine coverage in 20 years.\n\n')
                if float(df.loc[self.textbox2.text().lower(), "Vaccine Coverage 20 years Prediction"]) > float(df.loc[self.textbox1.text().lower(), "Vaccine Coverage 20 years Prediction"]):
                    self.textbox4.append(f'The vaccine coverage relative change in {self.textbox1.text().lower().title()} is {round(df.loc[self.textbox1.text().lower(), "Coverage Average Relative Change"],5)}%. {self.textbox1.text().lower().title()} has a lower average vaccine coverage relative change than the {round(df.loc[self.textbox2.text().lower(), "Coverage Average Relative Change"],5)}% average vaccine coverage relative change in {self.textbox2.text().lower().title()}. Using this calculated relative change, {self.textbox1.text().lower().title()} is predicted to have less vaccine coverage in 20 years.\n\n')
            except:
                self.textbox4.append(f'The vaccine coverage relative change in {self.textbox1.text().lower().title()} is {df.loc[self.textbox1.text().lower(), "Coverage Average Relative Change"]}% and {df.loc[self.textbox2.text().lower(), "Coverage Average Relative Change"]}% in the {self.textbox2.text().lower().title()}. It cannot be determined which country is predicted to have a higher vaccine coverage in 20 years.\n\n')
            self.textbox4.append(f'Going to {self.textbox1.text().lower().title()} will require {df.loc[self.textbox1.text().lower(), "Number of Vaccines Recommended"]} vaccines.\nThe vaccinations include:\n{df.loc[self.textbox1.text().lower(), "Vaccinations"]}\n\n')

            #table1
            self.table.setHorizontalHeaderItem(0, QTableWidgetItem("Country Name"))
            self.table.setHorizontalHeaderItem(1, QTableWidgetItem("Vaccinations"))
            self.table.setHorizontalHeaderItem(2, QTableWidgetItem("Exchange Currency (per US $)"))
            self.table.setHorizontalHeaderItem(3, QTableWidgetItem("Agriculture Employment 2019"))
            self.table.setHorizontalHeaderItem(4, QTableWidgetItem("Industry Employment 2019"))
            self.table.setHorizontalHeaderItem(5, QTableWidgetItem("Services Employment 2019"))
            self.table.setHorizontalHeaderItem(6, QTableWidgetItem("Unemployment 2019"))
            self.table.setHorizontalHeaderItem(7, QTableWidgetItem("GDP 2019"))
            self.table.setHorizontalHeaderItem(8, QTableWidgetItem("Vaccine Coverage 2019"))


            self.table.setItem(0,0, QTableWidgetItem(str(self.textbox1.text().lower().title())))
            self.table.setItem(0,1, QTableWidgetItem(str(df.loc[self.textbox1.text().lower(), "Vaccinations"])))

            try:
                self.table.setItem(0,2, QTableWidgetItem(str(round(df.loc[self.textbox1.text().lower(), "Exchange Currency (per US $)"],5))))
            except:
                self.table.setItem(0,2, QTableWidgetItem("Unknown"))
            try:
                self.table.setItem(0,3, QTableWidgetItem(str(round(df.loc[self.textbox1.text().lower(), "Employment in Agriculture 2020 (% of employed)"],5))))
            except:
                self.table.setItem(0,3, QTableWidgetItem("Unknown"))
            try:
                self.table.setItem(0,4, QTableWidgetItem(str(round(df.loc[self.textbox1.text().lower(), "Employment in Industry 2020 (% of employed)"],5))))
            except:
                self.table.setItem(0,4, QTableWidgetItem("Unknown"))
            try:
                self.table.setItem(0,5, QTableWidgetItem(str(round(df.loc[self.textbox1.text().lower(), "Employment in Services 2020 (% of employed)"],5))))
            except:
                self.table.setItem(0,5, QTableWidgetItem("Unknown"))
            try:
                self.table.setItem(0,6, QTableWidgetItem(str(round(df.loc[self.textbox1.text().lower(), "2019 Unemployment"],5))))
            except:
                self.table.setItem(0,6, QTableWidgetItem("Unknown"))
            try:
                self.table.setItem(0,7, QTableWidgetItem(str(round(df.loc[self.textbox1.text().lower(), "2019 GDP"],5))))
            except:
                self.table.setItem(0,7, QTableWidgetItem("Unknown"))
            try:
                self.table.setItem(0,8, QTableWidgetItem(str(round(df.loc[self.textbox1.text().lower(), 2019],5))))
            except:
                self.table.setItem(0,8, QTableWidgetItem("Unknown"))

            self.table.setItem(1,0, QTableWidgetItem(str(self.textbox2.text().lower().title())))
            self.table.setItem(1,1, QTableWidgetItem(str(df.loc[self.textbox2.text().lower(), "Vaccinations"])))
            try:
                self.table.setItem(1,2, QTableWidgetItem(str(round(df.loc[self.textbox2.text().lower(), "Exchange Currency (per US $)"],5))))
            except:
                self.table.setItem(1,2, QTableWidgetItem("Unknown"))
            try:
                self.table.setItem(1,3, QTableWidgetItem(str(round(df.loc[self.textbox2.text().lower(), "Employment in Agriculture 2020 (% of employed)"],5))))
            except:
                self.table.setItem(1,3, QTableWidgetItem("Unknown"))
            try:
                self.table.setItem(1,4, QTableWidgetItem(str(round(df.loc[self.textbox2.text().lower(), "Employment in Industry 2020 (% of employed)"],5))))
            except:
                self.table.setItem(1,4, QTableWidgetItem("Unknown"))
            try:
                self.table.setItem(1,5, QTableWidgetItem(str(round(df.loc[self.textbox2.text().lower(), "Employment in Services 2020 (% of employed)"],5))))
            except:
                self.table.setItem(1,5, QTableWidgetItem("Unknown"))
            try:
                self.table.setItem(1,6, QTableWidgetItem(str(round(df.loc[self.textbox2.text().lower(), "2019 Unemployment"],5))))
            except:
                self.table.setItem(1,6, QTableWidgetItem("Unknown"))
            try:
                self.table.setItem(1,7, QTableWidgetItem(str(round(df.loc[self.textbox2.text().lower(), "2019 GDP"],5))))
            except:
                self.table.setItem(1,7, QTableWidgetItem("Unknown"))
            try:
                self.table.setItem(1,8, QTableWidgetItem(str(round(df.loc[self.textbox2.text().lower(), 2019],5))))
            except:
                self.table.setItem(1,8, QTableWidgetItem("Unknown"))

            #table2
            self.table2.setHorizontalHeaderItem(0, QTableWidgetItem("Country Name"))
            self.table2.setHorizontalHeaderItem(1, QTableWidgetItem("Vaccinations"))
            self.table2.setHorizontalHeaderItem(2, QTableWidgetItem("Exchange Currency (per US $)"))
            self.table2.setHorizontalHeaderItem(3, QTableWidgetItem("Agriculture Employment 20 Years Prediction"))
            self.table2.setHorizontalHeaderItem(4, QTableWidgetItem("Industry Employment 20 Years Prediction"))
            self.table2.setHorizontalHeaderItem(5, QTableWidgetItem("Services Employment 20 Years Prediction"))
            self.table2.setHorizontalHeaderItem(6, QTableWidgetItem("Unemployment 20 Years Prediction"))
            self.table2.setHorizontalHeaderItem(7, QTableWidgetItem("GDP 20 Years Prediction"))
            self.table2.setHorizontalHeaderItem(8, QTableWidgetItem("Vaccine Coverage 20 Years Prediction"))


            self.table2.setItem(0,0, QTableWidgetItem(str(self.textbox1.text().lower().title())))
            self.table2.setItem(0,1, QTableWidgetItem(str(df.loc[self.textbox1.text().lower(), "Vaccinations"])))

            try:
                self.table2.setItem(0,2, QTableWidgetItem(str(round(df.loc[self.textbox1.text().lower(), "Exchange Currency (per US $)"],5))))
            except:
                self.table2.setItem(0,2, QTableWidgetItem("Unknown"))
            try:
                self.table2.setItem(0,3, QTableWidgetItem(str(round(df.loc[self.textbox1.text().lower(), "Employment in Agriculture 20 years Prediction"],5))))
            except:
                self.table2.setItem(0,3, QTableWidgetItem("Unknown"))
            try:
                self.table2.setItem(0,4, QTableWidgetItem(str(round(df.loc[self.textbox1.text().lower(), "Employment in Industry 20 years Prediction"],5))))
            except:
                self.table2.setItem(0,4, QTableWidgetItem("Unknown"))
            try:
                self.table2.setItem(0,5, QTableWidgetItem(str(round(df.loc[self.textbox1.text().lower(), "Employment in Service 20 years Prediction"],5))))
            except:
                self.table2.setItem(0,5, QTableWidgetItem("Unknown"))
            try:
                self.table2.setItem(0,6, QTableWidgetItem(str(round(df.loc[self.textbox1.text().lower(), "Unemployment 20 years Prediction"],5))))
            except:
                self.table2.setItem(0,6, QTableWidgetItem("Unknown"))
            try:
                self.table2.setItem(0,7, QTableWidgetItem(str(round(df.loc[self.textbox1.text().lower(), "GDP 20 years Prediction"],5))))
            except:
                self.table2.setItem(0,7, QTableWidgetItem("Unknown"))
            try:
                self.table2.setItem(0,8, QTableWidgetItem(str(round(df.loc[self.textbox1.text().lower(), "Vaccine Coverage 20 years Prediction"],5))))
            except:
                self.table2.setItem(0,8, QTableWidgetItem("Unknown"))

            self.table2.setItem(1,0, QTableWidgetItem(str(self.textbox2.text().lower().title())))
            self.table2.setItem(1,1, QTableWidgetItem(str(df.loc[self.textbox2.text().lower(), "Vaccinations"])))
            try:
                self.table2.setItem(1,2, QTableWidgetItem(str(round(df.loc[self.textbox2.text().lower(), "Exchange Currency (per US $)"],5))))
            except:
                self.table2.setItem(1,2, QTableWidgetItem("Unknown"))
            try:
                self.table2.setItem(1,3, QTableWidgetItem(str(round(df.loc[self.textbox2.text().lower(), "Employment in Agriculture 20 years Prediction"],5))))
            except:
                self.table2.setItem(1,3, QTableWidgetItem("Unknown"))
            try:
                self.table2.setItem(1,4, QTableWidgetItem(str(round(df.loc[self.textbox2.text().lower(), "Employment in Industry 20 years Prediction"],5))))
            except:
                self.table2.setItem(1,4, QTableWidgetItem("Unknown"))
            try:
                self.table2.setItem(1,5, QTableWidgetItem(str(round(df.loc[self.textbox2.text().lower(), "Employment in Service 20 years Prediction"],5))))
            except:
                self.table2.setItem(1,5, QTableWidgetItem("Unknown"))
            try:
                self.table2.setItem(1,6, QTableWidgetItem(str(round(df.loc[self.textbox2.text().lower(), "Unemployment 20 years Prediction"],5))))
            except:
                self.table2.setItem(1,6, QTableWidgetItem("Unknown"))
            try:
                self.table2.setItem(1,7, QTableWidgetItem(str(round(df.loc[self.textbox2.text().lower(), "GDP 20 years Prediction"],5))))
            except:
                self.table2.setItem(1,7, QTableWidgetItem("Unknown"))
            try:
                self.table2.setItem(1,8, QTableWidgetItem(str(round(df.loc[self.textbox2.text().lower(), "Vaccine Coverage 20 years Prediction"],5))))
            except:
                self.table2.setItem(1,8, QTableWidgetItem("Unknown"))
            try:
                if float(df.loc[self.textbox2.text().lower(), "GDP 20 years Prediction"]) < float(df.loc[self.textbox1.text().lower(), "GDP 20 years Prediction"]):
                    self.textbox4.append(f'The GDP average relative change in {self.textbox1.text().lower().title()} is {round(df.loc[self.textbox1.text().lower(), "GDP Average Relative Change"],5)}%, which is higher than the {round(df.loc[self.textbox2.text().lower(), "GDP Average Relative Change"],5)}% GDP average relative change in the {self.textbox2.text().lower().title()}. Using this calculated relative change, {self.textbox2.text().lower().title()} is predicted to have a lower GDP in 20 years.')
                if float(df.loc[self.textbox2.text().lower(), "GDP 20 years Prediction"]) > float(df.loc[self.textbox1.text().lower(), "GDP 20 years Prediction"]):
                    self.textbox4.append(f'The GDP average relative change in {self.textbox1.text().lower().title()} is {round(df.loc[self.textbox1.text().lower(), "GDP Average Relative Change"],5)}%, which is lower than the {round(df.loc[self.textbox2.text().lower(), "GDP Average Relative Change"],5)}% GDP average relative change in the U.S. Using this calculated relative change, {self.textbox1.text().lower().title()} is predicted to have a lower GDP in 20 years.')
            except:
                self.textbox4.append(f'The GDP average relative change in {self.textbox1.text().lower().title()} is {df.loc[self.textbox1.text().lower(), "GDP Average Relative Change"]} and {df.loc[self.textbox2.text().lower(), "GDP Average Relative Change"]} in the {self.textbox2.text().lower().title()}. It cannot be determined which country is predicted to have a higher GDP in 20 years.')

            #future better country
            try:
                if future_score_df.loc[self.textbox1.text().lower().title(),"Future Score"] > future_score_df.loc[self.textbox2.text().lower().title(), "Future Score"]:
                    self.textbox5.setText(self.textbox1.text().lower().title())
                elif future_score_df.loc[self.textbox1.text().lower().title(),"Future Score"] < future_score_df.loc[self.textbox2.text().lower().title(), "Future Score"]:
                    self.textbox5.setText(self.textbox2.text().lower().title())
                elif future_score_df.loc[self.textbox1.text().lower().title(),"Future Score"] == future_score_df.loc[self.textbox2.text().lower().title(), "Future Score"]:
                    self.textbox5.setText("Either option is good")
            except TypeError:
                self.textbox5.setText("Not enough information to tell")

            #current better country
            try:
                if current_score_df.loc[self.textbox1.text().lower().title(),"Current Score"] > current_score_df.loc[self.textbox2.text().lower().title(), "Current Score"]:
                    self.textbox6.setText(self.textbox1.text().lower().title())
                elif current_score_df.loc[self.textbox1.text().lower().title(),"Current Score"] < current_score_df.loc[self.textbox2.text().lower().title(), "Current Score"]:
                    self.textbox6.setText(self.textbox2.text().lower().title())
                elif current_score_df.loc[self.textbox1.text().lower().title(),"Current Score"] == current_score_df.loc[self.textbox2.text().lower().title(), "Current Score"]:
                    self.textbox6.setText("Either option is good")
            except TypeError:
                self.textbox6.setText("Not enough information to tell")


        else:
            if (self.textbox1.text().lower() not in countries) and (self.textbox2.text().lower() not in countries):
                self.textbox4.setText(f'Information from {self.textbox2.text().lower().title()} and {self.textbox1.text().lower().title()} are unknown.\n\n')
            elif self.textbox1.text().lower() not in countries:
                self.textbox4.setText(f'Information from {self.textbox1.text().lower().title()} is unknown.\n\n')
            elif self.textbox2.text().lower() not in countries:
                self.textbox4.setText(f'Information from {self.textbox2.text().lower().title()} is unknown.\n\n')
            elif self.textbox1.text().lower() == self.textbox2.text().lower():
                self.textbox4.setText("Please enter 2 different countries.")

future_score_df = future_score()
current_score_df = current_country()

class SpecificCountry(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Info on a Specific Country")
        width = 800
        self.setFixedWidth(width)
        height = 500
        self.setFixedHeight(height)

        vbox1 = QVBoxLayout()

        vbox2 = QVBoxLayout()
        self.textbox1 = QLineEdit()
        self.label1 = QLabel("Enter Destination to be compared to United States:")
        self.label1.setBuddy(self.textbox1)
        self.textbox1.textEdited.connect(self.edited_text)
        vbox2.addWidget(self.label1)
        vbox2.addWidget(self.textbox1)

        vbox3 = QVBoxLayout()
        self.label2 = QLabel("Select the information you would like to know:")
        vbox3.addWidget(self.label2)
        self.combo_box2 = QComboBox(self)
        self.combo_box2.addItem("")
        self.combo_box2.addItem("Unemployment")
        self.combo_box2.addItem("Employment By Sector")
        self.combo_box2.addItem("Currency Exchange Rate")
        self.combo_box2.addItem("Vaccine Coverage")
        self.combo_box2.addItem("Vaccinations")
        self.combo_box2.addItem("GDP")
        vbox3.addWidget(self.combo_box2)
        self.combo_box2.activated[str].connect(self.specific)

        vbox4 = QVBoxLayout()
        self.textbox2 = QTextEdit()
        self.textbox2.setReadOnly(True)
        vbox4.addWidget(self.textbox2)

        hbox1 = QHBoxLayout()
        vbox5 = QVBoxLayout()
        vbox6 = QVBoxLayout()
        self.textbox3 = QTextEdit()
        self.textbox3.setReadOnly(True)
        self.label3 = QLabel("Should I move in 20 years?")
        vbox5.addWidget(self.label3)
        vbox5.addWidget(self.textbox3)
        hbox1.addLayout(vbox5)
        self.textbox4 = QTextEdit()
        self.textbox4.setReadOnly(True)
        self.label4 = QLabel("Should I move now?")
        vbox6.addWidget(self.label4)
        vbox6.addWidget(self.textbox4)
        hbox1.addLayout(vbox6)

        vbox1.addLayout(vbox2)
        vbox1.addLayout(vbox3)
        vbox1.addLayout(vbox4)
        vbox1.addLayout(hbox1)

        self.setLayout(vbox1)

    def edited_text(self, text):
        self.textbox2.clear()
        self.textbox3.clear()
        self.textbox4.clear()

    def specific(self, text):
        df = pd.read_excel("FinalData.xlsx", sheet_name = "Sheet1", index_col = 0, header = 0)
        countries = list(df.index)
        usList = ["united states of america", "u.s.a", "united states", "u.s."]
        if text == "":
            self.textbox2.clear()
            self.textbox3.clear()
            self.textbox4.clear()
        if self.textbox1.text() == "":
            self.textbox2.setText("Please enter a country name.")
        elif self.textbox1.text().lower() in usList:
            self.textbox2.setText("Please enter a different country.")
        elif self.textbox1.text().lower() in countries:
            try:
                if text == "Unemployment":
                    if float(df.loc["united states of america", "Unemployment 20 years Prediction"]) < float(df.loc[self.textbox1.text().lower(), "Unemployment 20 years Prediction"]):
                        self.textbox2.setText(f'Unemployment relative change in {self.textbox1.text().lower().title()}: {round(df.loc[self.textbox1.text().lower(), "Unemployment Average Relative Change"],5)}%\n\n{self.textbox1.text().lower().title()}\'s unemployment average relative change is also higher than the {round(df.loc["united states of america", "Unemployment Average Relative Change"],5)}% relative change in unemployment in the U.S. Using this calculated relative change, the U.S. is predicted to have less unemployment in 20 years.')
                    if float(df.loc["united states of america", "Unemployment 20 years Prediction"]) > float(df.loc[self.textbox1.text().lower(), "Unemployment 20 years Prediction"]):
                       self.textbox2.setText(f'Unemployment relative change in {self.textbox1.text().lower().title()}: {round(df.loc[self.textbox1.text().lower(), "Unemployment Average Relative Change"],5)}%\n\n{self.textbox1.text().lower().title()}\'s unemployment average relative change is also lower than the {round(df.loc["united states of america", "Unemployment Average Relative Change"],5)}% relative change in unemployment in the U.S. Using this calculated relative change, {df.loc[self.textbox1.text().lower(), "Unemployment Average Relative Change"]} is predicted to have less unemployment in 20 years.')
                    try:
                        #future better country
                        if df.loc[self.textbox1.text().lower(),"Unemployment 20 years Prediction"] < df.loc["United States Of America".lower(), "Unemployment 20 years Prediction"]:
                            self.textbox3.setText(f'Yes, {self.textbox1.text().lower().title()} will be better in 20 years based on unemployment.')
                        elif df.loc[self.textbox1.text().lower(),"Unemployment 20 years Prediction"] > df.loc["United States Of America".lower(), "Unemployment 20 years Prediction"]:
                            self.textbox3.setText('No, the United States of America will be better in 20 years based on unemployment.')
                        elif df.loc[self.textbox1.text().lower(),"Unemployment 20 years Prediction"] == df.loc["United States Of America".lower(), "Unemployment 20 years Prediction"]:
                            self.textbox3.setText("Either option is good based on unemployment.")
                    except TypeError:
                        self.textbox3.setText("Not enough information to tell")
                    try:
                        #current better country
                        if df.loc[self.textbox1.text().lower(),"2019 Unemployment"] < df.loc["United States Of America".lower(), "2019 Unemployment"]:
                            self.textbox4.setText(f'Yes, {self.textbox1.text().lower().title()} is better as of 2019 based on unemployment.')
                        elif df.loc[self.textbox1.text().lower(),"2019 Unemployment"] > df.loc["United States Of America".lower(), "2019 Unemployment"]:
                            self.textbox4.setText(f'No, the United States of America is better as of 2019 based on unemployment.')
                        elif df.loc[self.textbox1.text().lower(),"2019 Unemployment"] == df.loc["United States Of America".lower(), "2019 Unemployment"]:
                            self.textbox4.setText("Either option is good based on unemployment.")
                    except TypeError:
                        self.textbox4.setText("Not enough information to tell")

            except:
                self.textbox2.setText(f'Relative change in unemployment in {self.textbox1.text().lower().title()}: {df.loc[self.textbox1.text().lower(), "Unemployment Average Relative Change"]}\n\nIn contrast, the relative change of unemployment in the U.S. is {df.loc["united states of america", "Unemployment Average Relative Change"]}. It can not be predicted which country would have less unemployment in 20 years.\n\n')
                self.textbox3.setText("Not enough information to tell")

            if text == "Employment By Sector":
                #self.textbox1.text().lower() has higher agricultural, higher service, higher industrial
                if (df.loc[self.textbox1.text().lower(), "Employment in Agriculture 20 years Prediction"] > df.loc["united states of america", "Employment in Agriculture 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Service 20 years Prediction"] > df.loc["united states of america", "Employment in Service 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Industry 20 years Prediction"] > df.loc["united states of america", "Employment in Industry 20 years Prediction"]):
                    self.textbox2.setText(f'The calculated relative change for employment in agriculture, industry, and services for {self.textbox1.text().lower().title()} is:\nAgriculture: {round(df.loc[self.textbox1.text().lower(), "Agriculture Employment Average Relative Change"], 5)}%\nIndustry: {round(df.loc[self.textbox1.text().lower(), "Industry Employment Average Relative Change"],5)}%\nService: {round(df.loc[self.textbox1.text().lower(), "Services Employment Average Relative Change"],5)}%\n\nIn contrast, the calculated relative change for employment in agriculture, industry, and services for {"united states of america".title()} is:\nAgriculture: {round(df.loc["united states of america", "Agriculture Employment Average Relative Change"],5)}%\nIndustry: {round(df.loc["united states of america", "Industry Employment Average Relative Change"],5)}%\nServices: {round(df.loc["united states of america", "Services Employment Average Relative Change"],5)}%\n\nUsing this relative change trend, it has been calculated that {self.textbox1.text().lower().title()} is predicted to have higher agricultural, service, and industrial employment than the {"united states of america".title()} in 20 years.\n\n')
                    self.textbox3.setText(f'Yes, {self.textbox1.text().lower().title()} will be better in 20 years based on employment by sector.')
                #self.textbox1.text().lower() has higher agricultural, higher service, lower industrial
                elif (df.loc[self.textbox1.text().lower(), "Employment in Agriculture 20 years Prediction"] > df.loc["united states of america", "Employment in Agriculture 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Service 20 years Prediction"] > df.loc["united states of america", "Employment in Service 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Industry 20 years Prediction"] < df.loc["united states of america", "Employment in Industry 20 years Prediction"]):
                    self.textbox2.setText(f'The calculated relative change for employment in agriculture, industry, and services for {self.textbox1.text().lower().title()} is:\nAgriculture: {round(df.loc[self.textbox1.text().lower(), "Agriculture Employment Average Relative Change"], 5)}%\nIndustry: {round(df.loc[self.textbox1.text().lower(), "Industry Employment Average Relative Change"],5)}%\nService: {round(df.loc[self.textbox1.text().lower(), "Services Employment Average Relative Change"],5)}%\n\nIn contrast, the calculated relative change for employment in agriculture, industry, and services for {"united states of america".title()} is:\nAgriculture: {round(df.loc["united states of america", "Agriculture Employment Average Relative Change"],5)}%\nIndustry: {round(df.loc["united states of america", "Industry Employment Average Relative Change"],5)}%\nServices: {round(df.loc["united states of america", "Services Employment Average Relative Change"],5)}%\n\nUsing this relative change trend, it has been calculated that {self.textbox1.text().lower().title()} is predicted to have higher agricultural and service employments, but lower industrial employment than the {"united states of america".title()} in 20 years.\n\n')
                    self.textbox3.setText(f'Yes, {self.textbox1.text().lower().title()} will be better in 20 years based on employment by sector.')
                #self.textbox1.text().lower() has higher agricultural, lower service, lower industrial
                elif (df.loc[self.textbox1.text().lower(), "Employment in Agriculture 20 years Prediction"] > df.loc["united states of america", "Employment in Agriculture 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Service 20 years Prediction"] < df.loc["united states of america", "Employment in Service 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Industry 20 years Prediction"] < df.loc["united states of america", "Employment in Industry 20 years Prediction"]):
                    self.textbox2.setText(f'The calculated relative change for employment in agriculture, industry, and services for {self.textbox1.text().lower().title()} is:\nAgriculture: {round(df.loc[self.textbox1.text().lower(), "Agriculture Employment Average Relative Change"], 5)}%\nIndustry: {round(df.loc[self.textbox1.text().lower(), "Industry Employment Average Relative Change"],5)}%\nService: {round(df.loc[self.textbox1.text().lower(), "Services Employment Average Relative Change"],5)}%\n\nIn contrast, the calculated relative change for employment in agriculture, industry, and services for {"united states of america".title()} is:\nAgriculture: {round(df.loc["united states of america", "Agriculture Employment Average Relative Change"],5)}%\nIndustry: {round(df.loc["united states of america", "Industry Employment Average Relative Change"],5)}%\nServices: {round(df.loc["united states of america", "Services Employment Average Relative Change"],5)}%\n\nUsing this relative change trend, it has been calculated that {self.textbox1.text().lower().title()} is predicted to have higher agricultural employment, but lower industrial and service employments than the {"united states of america".title()} in 20 years.\n\n')
                    self.textbox3.setText('No, the United States of America will be better in 20 years based on employment by sector.')
                #self.textbox1.text().lower() has higher agricultural, lower service, higher industrial
                elif (df.loc[self.textbox1.text().lower(), "Employment in Agriculture 20 years Prediction"] > df.loc["united states of america", "Employment in Agriculture 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Service 20 years Prediction"] < df.loc["united states of america", "Employment in Service 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Industry 20 years Prediction"] > df.loc["united states of america", "Employment in Industry 20 years Prediction"]):
                    self.textbox2.setText(f'The calculated relative change for employment in agriculture, industry, and services for {self.textbox1.text().lower().title()} is:\nAgriculture: {round(df.loc[self.textbox1.text().lower(), "Agriculture Employment Average Relative Change"], 5)}%\nIndustry: {round(df.loc[self.textbox1.text().lower(), "Industry Employment Average Relative Change"],5)}%\nService: {round(df.loc[self.textbox1.text().lower(), "Services Employment Average Relative Change"],5)}%\n\nIn contrast, the calculated relative change for employment in agriculture, industry, and services for {"united states of america".title()} is:\nAgriculture: {round(df.loc["united states of america", "Agriculture Employment Average Relative Change"],5)}%\nIndustry: {round(df.loc["united states of america", "Industry Employment Average Relative Change"],5)}%\nServices: {round(df.loc["united states of america", "Services Employment Average Relative Change"],5)}%\n\nUsing this relative change trend, it has been calculated that {self.textbox1.text().lower().title()} is predicted to have higher agricultural and industrial employments, but lower service employment than the {"united states of america".title()} in 20 years.\n\n')
                    self.textbox3.setText(f'Yes, {self.textbox1.text().lower().title()} will be better in 20 years based on employment by sector.')
                #higher service, higher industrial, lower agriculture
                elif (df.loc[self.textbox1.text().lower(), "Employment in Service 20 years Prediction"] > df.loc["united states of america", "Employment in Service 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Agriculture 20 years Prediction"] < df.loc["united states of america", "Employment in Agriculture 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Industry 20 years Prediction"] > df.loc["united states of america", "Employment in Industry 20 years Prediction"]):
                    self.textbox2.setText(f'The calculated relative change for employment in agriculture, industry, and services for {self.textbox1.text().lower().title()} is:\nAgriculture: {round(df.loc[self.textbox1.text().lower(), "Agriculture Employment Average Relative Change"], 5)}%\nIndustry: {round(df.loc[self.textbox1.text().lower(), "Industry Employment Average Relative Change"],5)}%\nService: {round(df.loc[self.textbox1.text().lower(), "Services Employment Average Relative Change"],5)}%\n\nIn contrast, the calculated relative change for employment in agriculture, industry, and services for {"united states of america".title()} is:\nAgriculture: {round(df.loc["united states of america", "Agriculture Employment Average Relative Change"],5)}%\nIndustry: {round(df.loc["united states of america", "Industry Employment Average Relative Change"],5)}%\nServices: {round(df.loc["united states of america", "Services Employment Average Relative Change"],5)}%\n\nUsing this relative change trend, it has been calculated that {self.textbox1.text().lower().title()} is predicted to have higher service and industrial employments, but lower agricultural employment than the {"united states of america".title()} in 20 years.\n\n')
                    self.textbox3.setText(f'Yes, {self.textbox1.text().lower().title()} will be better in 20 years based on employment by sector.')
                #higher service, lower industrial, lower agricultural
                elif (df.loc[self.textbox1.text().lower(), "Employment in Service 20 years Prediction"] > df.loc["united states of america", "Employment in Service 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Agriculture 20 years Prediction"] < df.loc["united states of america", "Employment in Agriculture 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Industry 20 years Prediction"] < df.loc["united states of america", "Employment in Industry 20 years Prediction"]):
                    self.textbox2.setText(f'The calculated relative change for employment in agriculture, industry, and services for {self.textbox1.text().lower().title()} is:\nAgriculture: {round(df.loc[self.textbox1.text().lower(), "Agriculture Employment Average Relative Change"], 5)}%\nIndustry: {round(df.loc[self.textbox1.text().lower(), "Industry Employment Average Relative Change"],5)}%\nService: {round(df.loc[self.textbox1.text().lower(), "Services Employment Average Relative Change"],5)}%\n\nIn contrast, the calculated relative change for employment in agriculture, industry, and services for {"united states of america".title()} is:\nAgriculture: {round(df.loc["united states of america", "Agriculture Employment Average Relative Change"],5)}%\nIndustry: {round(df.loc["united states of america", "Industry Employment Average Relative Change"],5)}%\nServices: {round(df.loc["united states of america", "Services Employment Average Relative Change"],5)}%\n\nUsing this relative change trend, it has been calculated that {self.textbox1.text().lower().title()} is predicted to have higher service employment, but lower industrial and agricultural employments than the {"united states of america".title()} in 20 years.\n\n')
                    self.textbox3.setText('No, the United States of America will be better in 20 years based on employment by sector.')
                #higher industrial, lower service, lower agricultural
                elif (df.loc[self.textbox1.text().lower(), "Employment in Service 20 years Prediction"] < df.loc["united states of america", "Employment in Service 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Agriculture 20 years Prediction"] < df.loc["united states of america", "Employment in Agriculture 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Industry 20 years Prediction"] > df.loc["united states of america", "Employment in Industry 20 years Prediction"]):
                        self.textbox2.setText(f'The calculated relative change for employment in agriculture, industry, and services for {self.textbox1.text().lower().title()} is:\nAgriculture: {round(df.loc[self.textbox1.text().lower(), "Agriculture Employment Average Relative Change"], 5)}%\nIndustry: {round(df.loc[self.textbox1.text().lower(), "Industry Employment Average Relative Change"],5)}%\nService: {round(df.loc[self.textbox1.text().lower(), "Services Employment Average Relative Change"],5)}%\n\nIn contrast, the calculated relative change for employment in agriculture, industry, and services for {"united states of america".title()} is:\nAgriculture: {round(df.loc["united states of america", "Agriculture Employment Average Relative Change"],5)}%\nIndustry: {round(df.loc["united states of america", "Industry Employment Average Relative Change"],5)}%\nServices: {round(df.loc["united states of america", "Services Employment Average Relative Change"],5)}%\n\nUsing this relative change trend, it has been calculated that {self.textbox1.text().lower().title()} is predicted to have higher industrial employment, but lower service and agricultural employments than the {"united states of america".title()} in 20 years than.\n\n')
                        self.textbox3.setText('No, the United States of America will be better in 20 years based on employment by sector.')
                #lower industrial, lower service, lower agricultural
                elif (df.loc[self.textbox1.text().lower(), "Employment in Service 20 years Prediction"] < df.loc["united states of america", "Employment in Service 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Agriculture 20 years Prediction"] < df.loc["united states of america", "Employment in Agriculture 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Industry 20 years Prediction"] < df.loc["united states of america", "Employment in Industry 20 years Prediction"]):
                        self.textbox2.setText(f'The calculated relative change for employment in agriculture, industry, and services for {self.textbox1.text().lower().title()} is:\nAgriculture: {round(df.loc[self.textbox1.text().lower(), "Agriculture Employment Average Relative Change"], 5)}%\nIndustry: {round(df.loc[self.textbox1.text().lower(), "Industry Employment Average Relative Change"],5)}%\nService: {round(df.loc[self.textbox1.text().lower(), "Services Employment Average Relative Change"],5)}%\n\nIn contrast, the calculated relative change for employment in agriculture, industry, and services for {"united states of america".title()} is:\nAgriculture: {round(df.loc["united states of america", "Agriculture Employment Average Relative Change"],5)}%\nIndustry: {round(df.loc["united states of america", "Industry Employment Average Relative Change"],5)}%\nServices: {round(df.loc["united states of america", "Services Employment Average Relative Change"],5)}%\n\nUsing this relative change trend, it has been calculated that {self.textbox1.text().lower().title()} is predicted to have lower industrial, service and agricultural employments than the {"united states of america".title()} in 20 years.\n\n')
                        self.textbox3.setText('No, the United States of America will be better in 20 years based on employment by sector.')
                #country 1 has lower industrial, lower service, equal agriculture
                elif (df.loc[self.textbox1.text().lower(), "Employment in Service 20 years Prediction"] < df.loc["united states of america", "Employment in Service 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Agriculture 20 years Prediction"] == df.loc["united states of america", "Employment in Agriculture 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Industry 20 years Prediction"] < df.loc["united states of america", "Employment in Industry 20 years Prediction"]):
                        self.textbox2.setText(f'The calculated relative change for employment in agriculture, industry, and services for {self.textbox1.text().lower().title()} is:\nAgriculture: {round(df.loc[self.textbox1.text().lower(), "Agriculture Employment Average Relative Change"], 5)}%\nIndustry: {round(df.loc[self.textbox1.text().lower(), "Industry Employment Average Relative Change"],5)}%\nService: {round(df.loc[self.textbox1.text().lower(), "Services Employment Average Relative Change"],5)}%\n\nIn contrast, the calculated relative change for employment in agriculture, industry, and services for {"united states of america".title()} is:\nAgriculture: {round(df.loc["united states of america", "Agriculture Employment Average Relative Change"],5)}%\nIndustry: {round(df.loc["united states of america", "Industry Employment Average Relative Change"],5)},\nServices: {round(df.loc["united states of america", "Services Employment Average Relative Change"],5)}%\n\nUsing this relative change trend, it has been calculated that {self.textbox1.text().lower().title()} is predicted to have equal agricultural employments as {"united states of america".title()}, but lower service and industrial employments than {"united states of america".title()} in 20 years.')
                        self.textbox3.setText('No, the United States of America will be better in 20 years based on employment by sector.')
                #country 1 has lower industrial, higher service, equal agriculture
                elif (df.loc[self.textbox1.text().lower(), "Employment in Service 20 years Prediction"] > df.loc["united states of america", "Employment in Service 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Agriculture 20 years Prediction"] == df.loc["united states of america", "Employment in Agriculture 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Industry 20 years Prediction"] < df.loc["united states of america", "Employment in Industry 20 years Prediction"]):
                        self.textbox2.setText(f'The calculated relative change for employment in agriculture, industry, and services for {self.textbox1.text().lower().title()} is:\nAgriculture: {round(df.loc[self.textbox1.text().lower(), "Agriculture Employment Average Relative Change"], 5)}%\nIndustry: {round(df.loc[self.textbox1.text().lower(), "Industry Employment Average Relative Change"],5)}%\nService: {round(df.loc[self.textbox1.text().lower(), "Services Employment Average Relative Change"],5)}%\n\nIn contrast, the calculated relative change for employment in agriculture, industry, and services for {"united states of america".title()} is:\nAgriculture: {round(df.loc["united states of america", "Agriculture Employment Average Relative Change"],5)}%\nIndustry: {round(df.loc["united states of america", "Industry Employment Average Relative Change"],5)}\nServices: {round(df.loc["united states of america", "Services Employment Average Relative Change"],5)}%\n\nUsing this relative change trend, it has been calculated that {self.textbox1.text().lower().title()} is predicted to have equal agricultural employments as {"united states of america".title()}, but higher service employments and lower industrial employments than {"united states of america".title()} in 20 years.')
                        self.textbox3.setText(f'Either option is good based on employment by sector.')
                #country 1 has higher industrial, lower service, equal agriculture
                elif (df.loc[self.textbox1.text().lower(), "Employment in Service 20 years Prediction"] < df.loc["united states of america", "Employment in Service 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Agriculture 20 years Prediction"] == df.loc["united states of america", "Employment in Agriculture 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Industry 20 years Prediction"] > df.loc["united states of america", "Employment in Industry 20 years Prediction"]):
                        self.textbox2.setText(f'The calculated relative change for employment in agriculture, industry, and services for {self.textbox1.text().lower().title()} is:\nAgriculture: {round(df.loc[self.textbox1.text().lower(), "Agriculture Employment Average Relative Change"], 5)}%\nIndustry: {round(df.loc[self.textbox1.text().lower(), "Industry Employment Average Relative Change"],5)}%\nService: {round(df.loc[self.textbox1.text().lower(), "Services Employment Average Relative Change"],5)}%\n\nIn contrast, the calculated relative change for employment in agriculture, industry, and services for {"united states of america".title()} is:\nAgriculture: {round(df.loc["united states of america", "Agriculture Employment Average Relative Change"],5)}%\nIndustry: {round(df.loc["united states of america", "Industry Employment Average Relative Change"],5)}\nServices: {round(df.loc["united states of america", "Services Employment Average Relative Change"],5)}%\n\nUsing this relative change trend, it has been calculated that {self.textbox1.text().lower().title()} is predicted to have equal agricultural employments as {"united states of america".title()}, but lower service employments and higher industrial employments than {"united states of america".title()} in 20 years.')
                        self.textbox3.setText(f'Either option is good based on employment by sector.')
                #country 1 has higher industrial, higher service, equal agriculture
                elif (df.loc[self.textbox1.text().lower(), "Employment in Service 20 years Prediction"] > df.loc["united states of america", "Employment in Service 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Agriculture 20 years Prediction"] == df.loc["united states of america", "Employment in Agriculture 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Industry 20 years Prediction"] > df.loc["united states of america", "Employment in Industry 20 years Prediction"]):
                        self.textbox2.setText(f'The calculated relative change for employment in agriculture, industry, and services for {self.textbox1.text().lower().title()} is:\nAgriculture: {round(df.loc[self.textbox1.text().lower(), "Agriculture Employment Average Relative Change"], 5)}%\nIndustry: {round(df.loc[self.textbox1.text().lower(), "Industry Employment Average Relative Change"],5)}%\nService: {round(df.loc[self.textbox1.text().lower(), "Services Employment Average Relative Change"],5)}%\n\nIn contrast, the calculated relative change for employment in agriculture, industry, and services for {"united states of america".title()} is:\nAgriculture: {round(df.loc["united states of america", "Agriculture Employment Average Relative Change"],5)}%\nIndustry: {round(df.loc["united states of america", "Industry Employment Average Relative Change"],5)}\nServices: {round(df.loc["united states of america", "Services Employment Average Relative Change"],5)}%\n\nUsing this relative change trend, it has been calculated that {self.textbox1.text().lower().title()} is predicted to have equal agricultural employments as {"united states of america".title()}, but higher service and industrial employments than {"united states of america".title()} in 20 years.')
                        self.textbox3.setText(f'Yes, {self.textbox1.text().lower().title()} will be better in 20 years based on employment by sector.')
                #country 1 has equal industrial, lower service, higher agriculture
                elif (df.loc[self.textbox1.text().lower(), "Employment in Service 20 years Prediction"] < df.loc["united states of america", "Employment in Service 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Agriculture 20 years Prediction"] > df.loc["united states of america", "Employment in Agriculture 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Industry 20 years Prediction"] == df.loc["united states of america", "Employment in Industry 20 years Prediction"]):
                        self.textbox2.setText(f'The calculated relative change for employment in agriculture, industry, and services for {self.textbox1.text().lower().title()} is:\nAgriculture: {round(df.loc[self.textbox1.text().lower(), "Agriculture Employment Average Relative Change"], 5)}%\nIndustry: {round(df.loc[self.textbox1.text().lower(), "Industry Employment Average Relative Change"],5)}%\nService: {round(df.loc[self.textbox1.text().lower(), "Services Employment Average Relative Change"],5)}%\n\nIn contrast, the calculated relative change for employment in agriculture, industry, and services for {"united states of america".title()} is:\nAgriculture: {round(df.loc["united states of america", "Agriculture Employment Average Relative Change"],5)}%\nIndustry: {round(df.loc["united states of america", "Industry Employment Average Relative Change"],5)}\nServices: {round(df.loc["united states of america", "Services Employment Average Relative Change"],5)}%\n\nUsing this relative change trend, it has been calculated that {self.textbox1.text().lower().title()} is predicted to have equal industrial employments as {"united states of america".title()}, but lower service and higher agricultural employments than {"united states of america".title()} in 20 years.')
                        self.textbox3.setText(f'Either option is good based on employment by sector.')
                #country 1 has equal industrial, higher service, lower agriculture
                elif (df.loc[self.textbox1.text().lower(), "Employment in Service 20 years Prediction"] > df.loc["united states of america", "Employment in Service 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Agriculture 20 years Prediction"] < df.loc["united states of america", "Employment in Agriculture 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Industry 20 years Prediction"] == df.loc["united states of america", "Employment in Industry 20 years Prediction"]):
                        self.textbox2.setText(f'The calculated relative change for employment in agriculture, industry, and services for {self.textbox1.text().lower().title()} is:\nAgriculture: {round(df.loc[self.textbox1.text().lower(), "Agriculture Employment Average Relative Change"], 5)}%\nIndustry: {round(df.loc[self.textbox1.text().lower(), "Industry Employment Average Relative Change"],5)}\nService: {round(df.loc[self.textbox1.text().lower(), "Services Employment Average Relative Change"],5)}%\n\nIn contrast, the calculated relative change for employment in agriculture, industry, and services for {"united states of america".title()} is:\nAgriculture: {round(df.loc["united states of america", "Agriculture Employment Average Relative Change"],5)}%\nIndustry: {round(df.loc["united states of america", "Industry Employment Average Relative Change"],5)}\nServices: {round(df.loc["united states of america", "Services Employment Average Relative Change"],5)}%\n\nUsing this relative change trend, it has been calculated that {self.textbox1.text().lower().title()} is predicted to have equal industrial employments as {"united states of america".title()}, but higher service and lower agricultural employments than {"united states of america".title()} in 20 years.')
                        self.textbox3.setText(f'Either option is good based on employment by sector.')
                #country 1 has equal industrial, lower service, lower agriculture
                elif (df.loc[self.textbox1.text().lower(), "Employment in Service 20 years Prediction"] < df.loc["united states of america", "Employment in Service 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Agriculture 20 years Prediction"] < df.loc["united states of america", "Employment in Agriculture 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Industry 20 years Prediction"] == df.loc["united states of america", "Employment in Industry 20 years Prediction"]):
                        self.textbox2.setText(f'The calculated relative change for employment in agriculture, industry, and services for {self.textbox1.text().lower().title()} is:\nAgriculture: {round(df.loc[self.textbox1.text().lower(), "Agriculture Employment Average Relative Change"],5)}%\nIndustry: {round(df.loc[self.textbox1.text().lower(), "Industry Employment Average Relative Change"],5)}\nService: {round(df.loc[self.textbox1.text().lower(), "Services Employment Average Relative Change"],5)}%\n\nIn contrast, the calculated relative change for employment in agriculture, industry, and services for {"united states of america".title()} is:\nAgriculture: {round(df.loc["united states of america", "Agriculture Employment Average Relative Change"],5)}%\nIndustry: {round(df.loc["united states of america", "Industry Employment Average Relative Change"],5)}\nServices: {round(df.loc["united states of america", "Services Employment Average Relative Change"])}%\n\nUsing this relative change trend, it has been calculated that {self.textbox1.text().lower().title()} is predicted to have equal industrial employments as {"united states of america".title()}, but lower service and agricultural employments than {"united states of america".title()} in 20 years.')
                        self.textbox3.setText('No, the United States of America will be better in 20 years based on employment by sector.')
                #country 1 has equal industrial, higher service, higher agriculture
                elif (df.loc[self.textbox1.text().lower(), "Employment in Service 20 years Prediction"] > df.loc["united states of america", "Employment in Service 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Agriculture 20 years Prediction"] > df.loc["united states of america", "Employment in Agriculture 20 years Prediction"]) and (df.loc[self.textbox1.text().lower(), "Employment in Industry 20 years Prediction"] == df.loc["united states of america", "Employment in Industry 20 years Prediction"]):
                        self.textbox2.setText(f'The calculated relative change for employment in agriculture, industry, and services for {self.textbox1.text().lower().title()} is:\nAgriculture: {round(df.loc[self.textbox1.text().lower(), "Agriculture Employment Average Relative Change"],5)}%\nIndustry: {round(df.loc[self.textbox1.text().lower(), "Industry Employment Average Relative Change"],5)}\nService: {round(df.loc[self.textbox1.text().lower(), "Services Employment Average Relative Change"],5)}%\n\nIn contrast, the calculated relative change for employment in agriculture, industry, and services for {"united states of america".title()} is:\nAgriculture: {round(df.loc["united states of america", "Agriculture Employment Average Relative Change"],5)}%\nIndustry: {round(df.loc["united states of america", "Industry Employment Average Relative Change"],5)}\nServices: {round(df.loc["united states of america", "Services Employment Average Relative Change"])}%\n\nUsing this relative change trend, it has been calculated that {self.textbox1.text().lower().title()} is predicted to have equal industrial employments as {"united states of america".title()}, but higher service and agricultural employments than {"united states of america".title()} in 20 years.')
                        self.textbox3.setText(f'Yes, {self.textbox1.text().lower().title()} will be better in 20 years based on employment by sector.')

                #self.textbox1.text().lower() has higher agricultural, higher service, higher industrial
                if (df.loc[self.textbox1.text().lower(), "Employment in Agriculture 2020 (% of employed)"] > df.loc["united states of america", "Employment in Agriculture 2020 (% of employed)"]) and (df.loc[self.textbox1.text().lower(), "Employment in Services 2020 (% of employed)"] > df.loc["united states of america", "Employment in Services 2020 (% of employed)"]) and (df.loc[self.textbox1.text().lower(), "Employment in Industry 2020 (% of employed)"] > df.loc["united states of america", "Employment in Industry 2020 (% of employed)"]):
                    self.textbox4.setText(f'Yes, {self.textbox1.text().lower().title()} will be better in 2019 based on employment by sector.')
                #self.textbox1.text().lower() has higher agricultural, higher service, lower industrial
                elif (df.loc[self.textbox1.text().lower(), "Employment in Agriculture 2020 (% of employed)"] > df.loc["united states of america", "Employment in Agriculture 2020 (% of employed)"]) and (df.loc[self.textbox1.text().lower(), "Employment in Services 2020 (% of employed)"] > df.loc["united states of america", "Employment in Services 2020 (% of employed)"]) and (df.loc[self.textbox1.text().lower(), "Employment in Industry 2020 (% of employed)"] < df.loc["united states of america", "Employment in Industry 2020 (% of employed)"]):
                    self.textbox4.setText(f'Yes, {self.textbox1.text().lower().title()} will be better in 2019 based on employment by sector.')
                #self.textbox1.text().lower() has higher agricultural, lower service, lower industrial
                elif (df.loc[self.textbox1.text().lower(), "Employment in Agriculture 2020 (% of employed)"] > df.loc["united states of america", "Employment in Agriculture 2020 (% of employed)"]) and (df.loc[self.textbox1.text().lower(), "Employment in Services 2020 (% of employed)"] < df.loc["united states of america", "Employment in Services 2020 (% of employed)"]) and (df.loc[self.textbox1.text().lower(), "Employment in Industry 2020 (% of employed)"] < df.loc["united states of america", "Employment in Industry 2020 (% of employed)"]):
                    self.textbox4.setText('No, the United States of America will be better in 2019 based on employment by sector.')
                #self.textbox1.text().lower() has higher agricultural, lower service, higher industrial
                elif (df.loc[self.textbox1.text().lower(), "Employment in Agriculture 2020 (% of employed)"] > df.loc["united states of america", "Employment in Agriculture 2020 (% of employed)"]) and (df.loc[self.textbox1.text().lower(), "Employment in Services 2020 (% of employed)"] < df.loc["united states of america", "Employment in Services 2020 (% of employed)"]) and (df.loc[self.textbox1.text().lower(), "Employment in Industry 2020 (% of employed)"] > df.loc["united states of america", "Employment in Industry 2020 (% of employed)"]):
                    self.textbox4.setText(f'Yes, {self.textbox1.text().lower().title()} will be better in 2019 based on employment by sector.')
                #higher service, higher industrial, lower agriculture
                elif (df.loc[self.textbox1.text().lower(), "Employment in Services 2020 (% of employed)"] > df.loc["united states of america", "Employment in Services 2020 (% of employed)"]) and (df.loc[self.textbox1.text().lower(), "Employment in Agriculture 2020 (% of employed)"] < df.loc["united states of america", "Employment in Agriculture 2020 (% of employed)"]) and (df.loc[self.textbox1.text().lower(), "Employment in Industry 2020 (% of employed)"] > df.loc["united states of america", "Employment in Industry 2020 (% of employed)"]):
                    self.textbox4.setText(f'Yes, {self.textbox1.text().lower().title()} will be better in 2019 based on employment by sector.')
                #higher service, lower industrial, lower agricultural
                elif (df.loc[self.textbox1.text().lower(), "Employment in Services 2020 (% of employed)"] > df.loc["united states of america", "Employment in Services 2020 (% of employed)"]) and (df.loc[self.textbox1.text().lower(), "Employment in Agriculture 2020 (% of employed)"] < df.loc["united states of america", "Employment in Agriculture 2020 (% of employed)"]) and (df.loc[self.textbox1.text().lower(), "Employment in Industry 2020 (% of employed)"] < df.loc["united states of america", "Employment in Industry 2020 (% of employed)"]):
                    self.textbox4.setText('No, the United States of America will be better in 2019 based on employment by sector.')
                #higher industrial, lower service, lower agricultural
                elif (df.loc[self.textbox1.text().lower(), "Employment in Services 2020 (% of employed)"] < df.loc["united states of america", "Employment in Services 2020 (% of employed)"]) and (df.loc[self.textbox1.text().lower(), "Employment in Agriculture 2020 (% of employed)"] < df.loc["united states of america", "Employment in Agriculture 2020 (% of employed)"]) and (df.loc[self.textbox1.text().lower(), "Employment in Industry 2020 (% of employed)"] > df.loc["united states of america", "Employment in Industry 2020 (% of employed)"]):
                        self.textbox4.setText('No, the United States of America will be better in 2019 based on employment by sector.')
                #lower industrial, lower service, lower agricultural
                elif (df.loc[self.textbox1.text().lower(), "Employment in Services 2020 (% of employed)"] < df.loc["united states of america", "Employment in Services 2020 (% of employed)"]) and (df.loc[self.textbox1.text().lower(), "Employment in Agriculture 2020 (% of employed)"] < df.loc["united states of america", "Employment in Agriculture 2020 (% of employed)"]) and (df.loc[self.textbox1.text().lower(), "Employment in Industry 2020 (% of employed)"] < df.loc["united states of america", "Employment in Industry 2020 (% of employed)"]):
                        self.textbox4.setText('No, the United States of America will be better in 2019 based on employment by sector.')
                #country 1 has lower industrial, lower service, equal agriculture
                elif (df.loc[self.textbox1.text().lower(), "Employment in Services 2020 (% of employed)"] < df.loc["united states of america", "Employment in Services 2020 (% of employed)"]) and (df.loc[self.textbox1.text().lower(), "Employment in Agriculture 2020 (% of employed)"] == df.loc["united states of america", "Employment in Agriculture 2020 (% of employed)"]) and (df.loc[self.textbox1.text().lower(), "Employment in Industry 2020 (% of employed)"] < df.loc["united states of america", "Employment in Industry 2020 (% of employed)"]):
                        self.textbox4.setText('No, the United States of America will be better in 2019 based on employment by sector.')
                #country 1 has lower industrial, higher service, equal agriculture
                elif (df.loc[self.textbox1.text().lower(), "Employment in Services 2020 (% of employed)"] > df.loc["united states of america", "Employment in Services 2020 (% of employed)"]) and (df.loc[self.textbox1.text().lower(), "Employment in Agriculture 2020 (% of employed)"] == df.loc["united states of america", "Employment in Agriculture 2020 (% of employed)"]) and (df.loc[self.textbox1.text().lower(), "Employment in Industry 2020 (% of employed)"] < df.loc["united states of america", "Employment in Industry 2020 (% of employed)"]):
                        self.textbox4.setText(f'Either option is good based on employment by sector.')
                #country 1 has higher industrial, lower service, equal agriculture
                elif (df.loc[self.textbox1.text().lower(), "Employment in Services 2020 (% of employed)"] < df.loc["united states of america", "Employment in Services 2020 (% of employed)"]) and (df.loc[self.textbox1.text().lower(), "Employment in Agriculture 2020 (% of employed)"] == df.loc["united states of america", "Employment in Agriculture 2020 (% of employed)"]) and (df.loc[self.textbox1.text().lower(), "Employment in Industry 2020 (% of employed)"] > df.loc["united states of america", "Employment in Industry 2020 (% of employed)"]):
                        self.textbox4.setText(f'Either option is good based on employment by sector.')
                #country 1 has higher industrial, higher service, equal agriculture
                elif (df.loc[self.textbox1.text().lower(), "Employment in Services 2020 (% of employed)"] > df.loc["united states of america", "Employment in Services 2020 (% of employed)"]) and (df.loc[self.textbox1.text().lower(), "Employment in Agriculture 2020 (% of employed)"] == df.loc["united states of america", "Employment in Agriculture 2020 (% of employed)"]) and (df.loc[self.textbox1.text().lower(), "Employment in Industry 2020 (% of employed)"] > df.loc["united states of america", "Employment in Industry 2020 (% of employed)"]):
                        self.textbox4.setText(f'Yes, {self.textbox1.text().lower().title()} will be better in 2019 based on employment by sector.')
                #country 1 has equal industrial, lower service, higher agriculture
                elif (df.loc[self.textbox1.text().lower(), "Employment in Services 2020 (% of employed)"] < df.loc["united states of america", "Employment in Services 2020 (% of employed)"]) and (df.loc[self.textbox1.text().lower(), "Employment in Agriculture 2020 (% of employed)"] > df.loc["united states of america", "Employment in Agriculture 2020 (% of employed)"]) and (df.loc[self.textbox1.text().lower(), "Employment in Industry 2020 (% of employed)"] == df.loc["united states of america", "Employment in Industry 2020 (% of employed)"]):
                        self.textbox4.setText(f'Either option is good based on employment by sector.')
                #country 1 has equal industrial, higher service, lower agriculture
                elif (df.loc[self.textbox1.text().lower(), "Employment in Services 2020 (% of employed)"] > df.loc["united states of america", "Employment in Services 2020 (% of employed)"]) and (df.loc[self.textbox1.text().lower(), "Employment in Agriculture 2020 (% of employed)"] < df.loc["united states of america", "Employment in Agriculture 2020 (% of employed)"]) and (df.loc[self.textbox1.text().lower(), "Employment in Industry 2020 (% of employed)"] == df.loc["united states of america", "Employment in Industry 2020 (% of employed)"]):
                        self.textbox4.setText(f'Either option is good based on employment by sector.')
                #country 1 has equal industrial, lower service, lower agriculture
                elif (df.loc[self.textbox1.text().lower(), "Employment in Services 2020 (% of employed)"] < df.loc["united states of america", "Employment in Services 2020 (% of employed)"]) and (df.loc[self.textbox1.text().lower(), "Employment in Agriculture 2020 (% of employed)"] < df.loc["united states of america", "Employment in Agriculture 2020 (% of employed)"]) and (df.loc[self.textbox1.text().lower(), "Employment in Industry 2020 (% of employed)"] == df.loc["united states of america", "Employment in Industry 2020 (% of employed)"]):
                        self.textbox4.setText('No, the United States of America will be better in 2019 based on employment by sector.')
                #country 1 has equal industrial, higher service, higher agriculture
                elif (df.loc[self.textbox1.text().lower(), "Employment in Services 2020 (% of employed)"] > df.loc["united states of america", "Employment in Services 2020 (% of employed)"]) and (df.loc[self.textbox1.text().lower(), "Employment in Agriculture 2020 (% of employed)"] > df.loc["united states of america", "Employment in Agriculture 2020 (% of employed)"]) and (df.loc[self.textbox1.text().lower(), "Employment in Industry 2020 (% of employed)"] == df.loc["united states of america", "Employment in Industry 2020 (% of employed)"]):
                        self.textbox4.setText(f'Yes, {self.textbox1.text().lower().title()} will be better in 2019 based on employment by sector.')

            if text == "Currency Exchange Rate":
                self.textbox2.setText(f'{self.textbox1.text().lower().title()} has an exchange rate of {df.loc[self.textbox1.text().lower(), "Exchange Currency (per US $)"]} per U.S. dollar.')
                self.textbox3.clear()
                self.textbox4.clear()
            try:
                if text == "Vaccine Coverage":
                    if float(df.loc["united states of america", "Vaccine Coverage 20 years Prediction"]) < float(df.loc[self.textbox1.text().lower(), "Vaccine Coverage 20 years Prediction"]):
                        self.textbox2.setText(f'The vaccine coverage relative change in {self.textbox1.text().lower().title()} is:\n{round(df.loc[self.textbox1.text().lower(), "Vaccine Coverage 20 years Prediction"], 5)}%\n\nThe vaccine coverage average relative change in {self.textbox1.text().lower().title()} is higher than the {round(df.loc["united states of america", "Coverage Average Relative Change"],5)}% vaccine coverage relative change in the U.S.. Using this calculated relative change, the U.S. is predicted to have less vaccine coverage in 20 years.')
                    if float(df.loc["united states of america", "Vaccine Coverage 20 years Prediction"]) > float(df.loc[self.textbox1.text().lower(), "Coverage Average Relative Change"]):
                        self.textbox2.setText(f'The vaccine coverage relative change in {self.textbox1.text().lower().title()} is:\n {round(df.loc[self.textbox1.text().lower(), "Vaccine Coverage 20 years Prediction"],5)}%\n\nThe vaccine coverage average relative change in {self.textbox1.text().lower().title()} is lower than the {round(df.loc["united states of america", "Coverage Average Relative Change"],5)}% vaccine coverage relative change in the U.S.. Using this calculated relative change, {self.textbox1.text().lower().title()} is predicted to have less vaccine coverage in 20 years.')
                    try:
                        #future better country
                        if df.loc[self.textbox1.text().lower(),"Vaccine Coverage 20 years Prediction"] > df.loc["United States Of America".lower(), "Vaccine Coverage 20 years Prediction"]:
                            self.textbox3.setText(f'Yes, {self.textbox1.text().lower().title()} will be better in 20 years based on vaccine coverage.')
                        elif df.loc[self.textbox1.text().lower(),"Vaccine Coverage 20 years Prediction"] < df.loc["United States Of America".lower(), "Vaccine Coverage 20 years Prediction"]:
                            self.textbox3.setText('No, the United States of America will be better in 20 years based on vaccine coverage.')
                        elif df.loc[self.textbox1.text().lower(),"Vaccine Coverage 20 years Prediction"] == df.loc["United States Of America".lower(), "Vaccine Coverage 20 years Prediction"]:
                            self.textbox3.setText("Either option is good based on vaccine coverage.")
                    except TypeError:
                        self.textbox3.setText("Not enough information to tell")
                    try:
                        #current better country
                        if df.loc[self.textbox1.text().lower(),2019] > df.loc["United States Of America".lower(), 2019]:
                            self.textbox4.setText(f'Yes, {self.textbox1.text().lower().title()} is better as of 2019 based on vaccine coverage.')
                        elif df.loc[self.textbox1.text().lower(),2019] < df.loc["United States Of America".lower(), 2019]:
                            self.textbox4.setText(f'No, the United States of America is better as of 2019 based on vaccine coverage.')
                        elif df.loc[self.textbox1.text().lower(),2019] == df.loc["United States Of America".lower(), 2019]:
                            self.textbox4.setText("Either option is good based on vaccine coverage.")
                    except TypeError:
                        self.textbox4.setText("Not enough information to tell")
            except:
                self.textbox2.setText(f'The vaccine coverage relative change in {self.textbox1.text().lower().title()} is {round(df.loc[self.textbox1.text().lower(), "Coverage Average Relative Change"],5)}% and {round(df.loc["united states of america", "Coverage Average Relative Change"], 5)}% in the U.S.. It cannot be determined which country is predicted to have a higher vaccine coverage in 20 years.')
                self.textbox3.setText("Not enough information to tell")

            if text == "Vaccinations":
                self.textbox2.setText(f'Going to {self.textbox1.text().lower().title()} will require {df.loc[self.textbox1.text().lower(), "Number of Vaccines Recommended"]} vaccines.\nThe vaccinations include:\n{df.loc[self.textbox1.text().lower(), "Vaccinations"]}')
                self.textbox4.clear()
                self.textbox3.clear()
            try:
                if text == "GDP":
                    if float(df.loc["united states of america", "GDP 20 years Prediction"]) < float(df.loc[self.textbox1.text().lower(), "GDP 20 years Prediction"]):
                        self.textbox2.setText(f'The GDP average relative change in {self.textbox1.text().lower().title()} is:\n {round(df.loc[self.textbox1.text().lower(), "GDP Average Relative Change"],5)}%\n\n{self.textbox1.text().lower().title()}\'s GDP average relative change is higher than the {round(df.loc["united states of america", "GDP Average Relative Change"],5)}% GDP average relative change in the U.S.. Using this calculated relative change, the U.S. is predicted to have a lower GDP in 20 years.')
                    if float(df.loc["united states of america", "GDP 20 years Prediction"]) > float(df.loc[self.textbox1.text().lower(), "GDP 20 years Prediction"]):
                        self.textbox2.setText(f'The GDP average relative change in {self.textbox1.text().lower().title()} is:\n {round(df.loc[self.textbox1.text().lower(), "GDP Average Relative Change"],5)}%\n\n{self.textbox1.text().lower().title()}\'s GDP average relative change is lower than the {round(df.loc["united states of america", "GDP Average Relative Change"],5)}% GDP average relative change in the U.S.. Using this calculated relative change, {self.textbox1.text().lower().title()} is predicted to have a lower GDP in 20 years.')
                    try:
                        #future better country
                        if df.loc[self.textbox1.text().lower(),"GDP 20 years Prediction"] > df.loc["United States Of America".lower(), "GDP 20 years Prediction"]:
                            self.textbox3.setText(f'Yes, {self.textbox1.text().lower().title()} will be better in 20 years based on GDP.')
                        elif df.loc[self.textbox1.text().lower(),"GDP 20 years Prediction"] < df.loc["United States Of America".lower(), "GDP 20 years Prediction"]:
                            self.textbox3.setText('No, the United States of America will be better in 20 years based on GDP.')
                        elif df.loc[self.textbox1.text().lower(),"GDP 20 years Prediction"] == df.loc["United States Of America".lower(), "GDP 20 years Prediction"]:
                            self.textbox3.setText("Either option is good based on GDP.")
                    except TypeError:
                        self.textbox3.setText("Not enough information to tell")
                    try:
                        #current better country
                        if df.loc[self.textbox1.text().lower(),"2019 GDP"] > df.loc["United States Of America".lower(), "2019 GDP"]:
                            self.textbox4.setText(f'Yes, {self.textbox1.text().lower().title()} is better as of 2019 based on GDP.')
                        elif df.loc[self.textbox1.text().lower(),"2019 GDP"] < df.loc["United States Of America".lower(), "2019 GDP"]:
                            self.textbox4.setText(f'No, the United States of America is better as of 2019 based on GDP.')
                        elif df.loc[self.textbox1.text().lower(),"2019 GDP"] == df.loc["United States Of America".lower(), "2019 GDP"]:
                            self.textbox4.setText("Either option is good based on GDP.")
                    except TypeError:
                        self.textbox4.setText("Not enough information to tell")
            except:
                self.textbox2.setText(f'The GDP average relative change in {self.textbox1.text().lower().title()} is {round(df.loc[self.textbox1.text().lower(), "GDP Average Relative Change"],5)}% and {round(df.loc["united states of america", "GDP Average Relative Change"],5)}% in the U.S.. It cannot be determined which country is predicted to have a higher GDP in 20 years.')
                self.textbox3.setText("Not enough information to tell")
        else:
            self.textbox2.setText(f'{text} from {self.textbox1.text().lower().title()} is unknown.')


future_score_df = future_score()
current_score_df = current_country()

class MapsandGraphs(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Maps and Graphs")
        width = 800
        self.setFixedWidth(width)
        height = 500
        self.setFixedHeight(height)
        self.browser = QtWebEngineWidgets.QWebEngineView(self)

        vbox = QVBoxLayout(self)

        vbox2 = QVBoxLayout()
        self.combo_box = QComboBox(self)
        self.combo_box.addItem("")
        self.combo_box.addItem("2019 World Map")
        self.combo_box.addItem("Future Prediction World Map")
        self.combo_box.addItem("Unemployment vs. GDP Graph")
        self.combo_box.addItem("Vaccine Coverage vs. GDP Graph")
        self.combo_box.addItem("Employment and GDP Graph")
        self.combo_box.setGeometry(300, 30, 200, 50)
        self.combo_box.activated[str].connect(self.makeGraph)

        self.infobutton = QPushButton(emoji.emojize(":question:", use_aliases=True))
        self.infobutton.setEnabled(False)
        self.infobutton.clicked.connect(self.infoClicked)

        vbox2.addWidget(self.combo_box)
        vbox2.addWidget(self.infobutton)

        vbox.addLayout(vbox2)
        vbox.addWidget(self.browser)

        self.messagebox = QMessageBox()
        self.messagebox.setText("Help")
        self.messagebox.setInformativeText("The bigger the circle is on the map, the better the country is to live in based on the country's GDP, unemployment, and employment by sector.")

    def infoClicked(self):
        self.messagebox.exec()

    def makeGraph(self, text):
        if text == "":
            self.infobutton.setEnabled(False)
        if text == "2019 World Map":
            df = pd.read_excel("FinalData.xlsx", sheet_name = "Sheet1", header = 0)
            df["Country Name"] = df["Country Name"].str.title()
            df.replace("Unknown", np.nan, inplace = True)
            df["GDP Percentage 2019"] = df["2019 GDP"]/df["2019 GDP"].mean(axis = 0)
            df["Score"] = ((df["GDP Percentage 2019"]/df["GDP Percentage 2019"].max(axis = 0))\
                            * (df[2019]/100)) * ((df["Employment in Services 2020 (% of employed)"]/100)\
                           + (df["Employment in Industry 2020 (% of employed)"]/100) +\
                           (df["Employment in Agriculture 2020 (% of employed)"]/100)) /(df["2019 Unemployment"]/100)
            df.dropna(inplace = True)

            fig = px.scatter_geo(df, locations="Country Name", locationmode = "country names",
                                 hover_name= "Country Name", size="Score",
                                 projection="natural earth", size_max = 65)
            self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))
            self.infobutton.setEnabled(True)

        elif text == "Future Prediction World Map":
            df = pd.read_excel("FinalData.xlsx", sheet_name = "Sheet1", header = 0)
            df["Country Name"] = df["Country Name"].str.title()
            df.set_index("Country Name", inplace = True)
            df.replace("Unknown", np.nan, inplace = True)

            for num in range(1,21):
                df[f"Employment in Agriculture {num} years Prediction"] = df["Agriculture Employment Average Relative Change"]*num + df["Employment in Agriculture 2020 (% of employed)"]
                df[f"Employment in Industry {num} years Prediction"] = df["Industry Employment Average Relative Change"]*num + df["Employment in Industry 2020 (% of employed)"]
                df[f"Employment in Service {num} years Prediction"] = df["Services Employment Average Relative Change"]*num + df["Employment in Services 2020 (% of employed)"]
                df[f"Vaccine Coverage {num} years Prediction"] = df["Coverage Average Relative Change"]*num + df[2019]
                df[f"GDP {num} years Prediction"] = df["GDP Average Relative Change"]*num + df["2019 GDP"]
                df[f"Unemployment {num} years Prediction"] = df["Unemployment Average Relative Change"]*num + df["2019 Unemployment"]

                df[f"GDP {2019 + num} Percentage"] = df[f"GDP {num} years Prediction"]/df[f"GDP {num} years Prediction"].mean(axis = 0)
                df[f"{2019 + num}"] = round(((df[f"GDP {2019 + num} Percentage"]/df[f"GDP {2019 + num} Percentage"].max(axis = 0))\
                                * (df[f"Vaccine Coverage {num} years Prediction"]/100)) * ((df[f"Employment in Service {num} years Prediction"]/100)\
                               + (df[f"Employment in Industry {num} years Prediction"]/100) +\
                               (df[f"Employment in Agriculture {num} years Prediction"]/100)) /(df[f"Unemployment {num} years Prediction"]/100),5)

            df.dropna(inplace = True)

            heading_list = list(df.columns)
            year_list = [str(x) for x in range(2020,2040)]

            for column in heading_list:
                if column not in year_list:
                    df.drop(columns = column, inplace = True)

            for num in range(0,145):
                df.iloc[num,0:] = np.where(df.iloc[num,0:] < 0, 0, df.iloc[num])


            years = list(df.columns)
            countries = list(df.index)

            combinations = []
            for year in years:
                for country in countries:
                    combinations.append([country, year])

            combinations.sort()
            combinations

            a_list = []
            for index, combo in enumerate(combinations):
                a_list.append([combo[0], combo[1],df.loc[combo[0],combo[1]]])

            new_df = pd.DataFrame(a_list)
            new_df.rename(columns = {0: "Country Names",1:"Years",2:"Scores"}, inplace = True)
            self.infobutton.setEnabled(True)
            fig = px.scatter_geo(new_df, locations= "Country Names", locationmode = "country names", hover_name= "Country Names", size= "Scores", animation_frame= "Years", projection="natural earth", size_max = 60)
            self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))

        elif text == "Unemployment vs. GDP Graph":
            df = pd.read_excel("FinalData.xlsx", sheet_name = "Sheet1",\
               index_col = 0, header = 0)
            unemployment = df.loc[:, "2010 Unemployment": "2019 Unemployment"]
            unemployment.replace("Unknown", np.nan, inplace = True)
            unemployment.loc["Average Unemployment"] = unemployment.mean(axis = 0)
            unemployment_series = unemployment.loc["Average Unemployment"]

            GDP = df.loc[:,"2010 GDP": "2019 GDP"]
            GDP.replace("Unknown", np.nan, inplace = True)
            GDP.loc["Average GDP"] = GDP.mean(axis = 0)
            GDP_series = GDP.loc["Average GDP"]

            GDP_unemployment = pd.concat([unemployment_series, GDP_series], axis = 0)
            df = pd.DataFrame(data = GDP_unemployment)
            df = df.transpose()

            Unemployment_GDP_df = pd.DataFrame(data = [[df.loc[0, "2010 Unemployment"], df.loc[0, "2011 Unemployment"],\
                                    df.loc[0,"2012 Unemployment"], df.loc[0, "2013 Unemployment"],\
                                      df.loc[0, "2014 Unemployment"], df.loc[0, "2015 Unemployment"],\
                                      df.loc[0, "2016 Unemployment"], df.loc[0, "2017 Unemployment"],\
                                      df.loc[0, "2018 Unemployment"], df.loc[0, "2019 Unemployment"]],\
                                    [df.loc[0, "2010 GDP"], df.loc[0, "2011 GDP"],\
                                        df.loc[0, "2012 GDP"], df.loc[0,"2013 GDP"],\
                                      df.loc[0, "2014 GDP"], df.loc[0, "2015 GDP"],\
                                      df.loc[0, "2016 GDP"], df.loc[0, "2017 GDP"],\
                                      df.loc[0, "2018 GDP"], df.loc[0, "2019 GDP"]]], index = ["Unemployment", "GDP"],\
                              columns = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019])
            Unemployment_GDP_df = Unemployment_GDP_df.transpose()
            fig = px.scatter(Unemployment_GDP_df, x="Unemployment", y="GDP", title='Unemployment vs. GDP', trendline="ols")
            self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))
            self.infobutton.setEnabled(False)

        elif text == "Vaccine Coverage vs. GDP Graph":
            df = pd.read_excel("FinalData.xlsx", sheet_name = "Sheet1",\
               index_col = 0, header = 0)

            df.rename(columns = {2010: "2010", 2011: "2011", 2012: "2012", 2013: "2013", 2014: "2014", 2015: "2015",\
                                2016: "2016", 2017: "2017", 2018: "2018", 2019: "2019"}, inplace = True)
            GDP = df.loc[:,"2010 GDP": "2019 GDP"]
            GDP.replace("Unknown", np.nan, inplace = True)
            GDP.loc["Average GDP"] = GDP.mean(axis = 0)
            GDP_series = GDP.loc["Average GDP"]

            vaccine_coverage = df.loc[:, "2010": "2019"]
            vaccine_coverage.replace("Unknown", np.nan, inplace = True)
            vaccine_coverage.loc["Average coverage"] = vaccine_coverage.mean(axis = 0)
            vaccine_coverage_series = vaccine_coverage.loc["Average coverage"]

            GDP_coverage = pd.concat([vaccine_coverage_series, GDP_series], axis = 0)
            df = pd.DataFrame(data = GDP_coverage)
            df = df.transpose()

            coverage_GDP_df = pd.DataFrame(data = [[df.loc[0, "2010"], df.loc[0, "2011"],\
                                    df.loc[0,"2012"], df.loc[0, "2013"],\
                                      df.loc[0, "2014"], df.loc[0, "2015"],\
                                      df.loc[0, "2016"], df.loc[0, "2017"],\
                                      df.loc[0, "2018"], df.loc[0, "2019"]],\
                                    [df.loc[0, "2010 GDP"], df.loc[0, "2011 GDP"],\
                                        df.loc[0, "2012 GDP"], df.loc[0,"2013 GDP"],\
                                      df.loc[0, "2014 GDP"], df.loc[0, "2015 GDP"],\
                                      df.loc[0, "2016 GDP"], df.loc[0, "2017 GDP"],\
                                      df.loc[0, "2018 GDP"], df.loc[0, "2019 GDP"]]], index = ["Vaccine Coverage", "GDP"],\
                              columns = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019])
            coverage_GDP_df = coverage_GDP_df.transpose()
            self.infobutton.setEnabled(False)
            fig = px.scatter(coverage_GDP_df, x="Vaccine Coverage", y="GDP", title='Coverage vs. GDP', trendline="ols")
            self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))

        elif text == "Employment and GDP Graph":
            df = pd.read_excel("FinalData.xlsx", sheet_name = "Sheet1",\
               index_col = 0, header = 0)

            GDP = df.loc[:,"2010 GDP": "2019 GDP": 9]
            GDP.replace("Unknown", np.nan, inplace = True)
            GDP.loc["Average GDP"] = GDP.mean(axis = 0)
            GDP_series = GDP.loc["Average GDP"]

            agriculture = df.loc[:, "Employment in Agriculture 2010 (% of employed)": "Employment in Agriculture 2020 (% of employed)"]
            agriculture.replace("Unknown", np.nan, inplace = True)
            agriculture.loc["Average agriculture"] = agriculture.mean(axis = 0)
            agriculture_series = agriculture.loc["Average agriculture"]

            service = df.loc[:, "Employment in Services 2010 (% of employed)": "Employment in Services 2020 (% of employed)"]
            service.replace("Unknown", np.nan, inplace = True)
            service.loc["Average Service"] = service.mean(axis = 0)
            service_series = service.loc["Average Service"]

            industry = df.loc[:, "Employment in Industry 2010 (% of employed)": "Employment in Industry 2020 (% of employed)"]
            industry.replace("Unknown", np.nan, inplace = True)
            industry.loc["Average Industry"] = industry.mean(axis = 0)
            industry_series = industry.loc["Average Industry"]

            GDP_agriculture = pd.concat([agriculture_series, GDP_series, service_series, industry_series], axis = 0)
            df = pd.DataFrame(data = GDP_agriculture)
            df = df.transpose()

            employment_GDP_df = pd.DataFrame(data = [[df.loc[0, "Employment in Agriculture 2010 (% of employed)"],\
                                    df.loc[0, "Employment in Agriculture 2020 (% of employed)"],\
                                    df.loc[0, "Employment in Services 2010 (% of employed)"],\
                                    df.loc[0, "Employment in Services 2020 (% of employed)"],\
                                    df.loc[0, "Employment in Industry 2010 (% of employed)"],\
                                    df.loc[0, "Employment in Industry 2020 (% of employed)"],\
                                    df.loc[0, "2010 GDP"], df.loc[0, "2019 GDP"]]],
                              columns = ["Agriculture", "Agriculture", "Services", "Services", "Industry","Industry",\
                                         "GDP (in 10 billions)","GDP (in 10 billions)"])
            employment_GDP_df = employment_GDP_df.transpose()
            employment_GDP_df["Years"] = ["2010", "2019","2010", "2019","2010", "2019","2010", "2019"]
            employment_GDP_df.reset_index(inplace = True)
            employment_GDP_df.rename(columns = {"index": "Sector", 0: "Percentage"}, inplace = True)
            employment_GDP_df.loc[6, "Percentage"] = employment_GDP_df.loc[6, "Percentage"]/10**10
            employment_GDP_df.loc[7, "Percentage"] = employment_GDP_df.loc[7, "Percentage"]/10**10
            fig = px.scatter(employment_GDP_df, x="Years", y="Percentage", title='GDP and Employment', trendline="ols", \
                             color='Sector')
            self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))
            self.infobutton.setEnabled(False)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Country Comparisons")
        width = 500
        self.setFixedWidth(width)
        height = 300
        self.setFixedHeight(height)
        self.browser = QtWebEngineWidgets.QWebEngineView(self)

        self.combo_box = QComboBox(self)
        self.combo_box.addItem("Compare 2 Countries")
        self.combo_box.addItem("Info on a Specific Country")
        self.combo_box.addItem("Maps and Graphs")
        self.combo_box.setGeometry(150, 90, 150, 100)
        self.combo_box.activated[str].connect(self.compareTwo)



    def compareTwo(self, text):
        if text == "Compare 2 Countries":
            self.w = CompareTwoWindow()
            self.w.show()
        elif text == "Info on a Specific Country":
            self.w = SpecificCountry()
            self.w.show()
        elif text == "Maps and Graphs":
            self.w = MapsandGraphs()
            self.w.show()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())


















