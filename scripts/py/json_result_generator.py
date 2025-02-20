#!/usr/bin/env python3

"""Reads result CSV files and converts them into
   compatible JSON files.
"""

import csv, json, os

SEASON = 2024
ROUND = 5

SCRIPT_DIR = os.path.dirname(__file__) + '/'
CSV_DIR = os.path.abspath(SCRIPT_DIR + './csv/' + str(SEASON))
JSON_DIR = os.path.abspath(SCRIPT_DIR + '../../data/' + str(SEASON))

class SeasonData:
    def __init__(self):
        self.list_fastestLaps = []
        self.dict_constructors = {}
        self.dict_team_fullname = {}
        self.dict_drivers = {}
        self.dict_calendar = {}
        self.list_roundResults = {}
        self.readSeasonData()


    def readSeasonData(self):
        with open(JSON_DIR + '/constructors.json', 'r') as json_file:
            dict_constructors = json.load(json_file)

        with open(JSON_DIR + '/team_fullname.json', 'r') as json_file:
            dict_team_fullname = json.load(json_file)

        with open(JSON_DIR + '/drivers.json', 'r') as json_file:
            dict_drivers = json.load(json_file)
        
        with open(JSON_DIR + '/calendar.json', 'r') as json_file:
            dict_calendar = json.load(json_file)
        
        self.dict_constructors = dict_constructors
        self.dict_team_fullname = dict_team_fullname
        self.dict_drivers = dict_drivers
        self.dict_calendar = dict_calendar

        self.readFastestLaps()


    def getDriverIdFromDriverName(self, str_driverName):
        str_result = None
        dict_drivers = self.dict_drivers['drivers']
        for str_driver in dict_drivers:
            pass
            if (dict_drivers[str_driver]['name'] == str_driverName.replace('\xa0',' ')):
                str_result = dict_drivers[str_driver]['id']
                return str_result
        
        return 'ERR'
        
        
    def getDriverIdFromCarNumber(self, str_carNumber):
        str_result = None
        dict_drivers = self.dict_drivers['drivers']
        for str_driver in dict_drivers:
            pass
            if (dict_drivers[str_driver]['car'] == str_carNumber):
                str_result = dict_drivers[str_driver]['id']
        
        return str_result
    

    def getTeamIdFromFullName(self, str_fullTeamName):
        str_result = None
        dict_team_fullname = self.dict_team_fullname['teams']
        for obj_team in dict_team_fullname:
            pass
            if (obj_team['fullname'] == str_fullTeamName):
                str_result = obj_team['id']
        
        return str_result
    

    def getRoundIdFromGpName(self, str_gpName):
        str_result = None
        dict_calendar = self.dict_calendar['schedule']
        for str_round in dict_calendar:
            pass
            if (dict_calendar[str_round]['gp'] == str_gpName):
                str_result = str_round
        
        return str_result


    def readFastestLaps(self):
        list_fastestLaps = []
        with open(CSV_DIR + '/fastest_laps.csv', 'r') as file:
            csv_fastestLaps = csv.reader(file)
            for row in csv_fastestLaps:
                list_fastestLaps.append(
                    {self.getRoundIdFromGpName(row[0]): [self.getDriverIdFromDriverName(row[1]), self.getTeamIdFromFullName(row[2])]})
        
        self.list_fastestLaps = list_fastestLaps
                

    def readRoundResult(self, int_round):
        obj_RoundResult = RoundResult(int_round)
        dict_race = {}
        dict_sprint = None

        with open(CSV_DIR + '/' + str(int_round).zfill(2) + '.csv', 'r') as file:
            csv_roundResult = csv.reader(file)
            int_placeAfterRace = 1
            for row in csv_roundResult:
                dict_race[str(int_placeAfterRace)] = [self.getDriverIdFromDriverName(row[2]), self.getTeamIdFromFullName(row[3])]
                int_placeAfterRace += 1

        if(os.path.exists(CSV_DIR + '/' + str(int_round).zfill(2) + '_sprint.csv')):
            with open(CSV_DIR + '/' + str(int_round).zfill(2) + '_sprint.csv', 'r') as file:
                dict_sprint = {}
                csv_roundResult = csv.reader(file)
                int_placeAfterRace = 1
                for row in csv_roundResult:
                    dict_sprint[str(int_placeAfterRace)] = [self.getDriverIdFromDriverName(row[2]), self.getTeamIdFromFullName(row[3])]
                    int_placeAfterRace += 1

        obj_RoundResult.dict_sprint = dict_sprint
        obj_RoundResult.dict_race = dict_race
        obj_RoundResult.list_fastestLap = (self.list_fastestLaps[int_round - 1][str(int_round)])
        self.list_roundResults[str(int_round)] = obj_RoundResult


    def writeRoundJson(self, int_round):
        obj_roundResults = self.list_roundResults[str(int_round)]
        str_jsonRoundResults = \
        '{\n'\
        '    "round": "' + str(obj_roundResults.int_round) + '",\n'

        if (obj_roundResults.dict_sprint == None):
            str_sprintResults = \
            '    "sprint": null,\n'
        else:
            str_sprintResults = \
            '    "sprint": \n' + \
            '    {\n'
            for obj_place in obj_roundResults.dict_sprint:
                str_sprintResults += '        "' + obj_place + '": ["' + obj_roundResults.dict_sprint[obj_place][0] + '", "' + obj_roundResults.dict_sprint[obj_place][1] + '"],\n'

            str_sprintResults = str_sprintResults[:-2] + '\n    },\n'
        
        str_raceResults = \
        '    "race": \n' + \
        '    {\n'
        for obj_place in obj_roundResults.dict_race:
            str_raceResults += '        "' + obj_place + '": ["' + obj_roundResults.dict_race[obj_place][0] + '", "' + obj_roundResults.dict_race[obj_place][1] + '"],\n'

        str_raceResults = str_raceResults[:-2] + '\n    },\n'
        
        str_fastestLap = \
        '    "fastest_lap": ["' + obj_roundResults.list_fastestLap[0] + '", "' + obj_roundResults.list_fastestLap[1] + '"]\n' + \
        '}'

        str_jsonRoundResults += str_sprintResults + str_raceResults + str_fastestLap

        with open(JSON_DIR + '/results/' + str(int_round).zfill(2) + '.json', 'w') as json_file:
            json_file.write(str_jsonRoundResults)


class RoundResult:
    def __init__(self, int_round):
        self.int_round = int_round
        self.dict_sprint = None
        self.dict_race = {}
        self.list_fastestLap = []
    

if(__name__ == "__main__"):
    obj_SeasonData = SeasonData()
    obj_SeasonData.readRoundResult(ROUND)
    obj_SeasonData.writeRoundJson(ROUND)
    print("end")
