from xml.dom import minidom
from nameparser import HumanName
import web.models

RFACTOR2NODEMAP = {
  "Position": "Position",
  "GridPos": "GridPosition",
  "CarNumber": "CarNumber",
  "Points": "Points",
  "Pitstops": "Stops"
}

def importResultFile(raceResult):
  """
  Parses the given rFacotr 2 result file and returns a list of (unsaved) driver results
  """
  resultList = list()
  xml = minidom.parse(raceResult.File.path)
  web.models.DriverResult.objects.filter(RaceResult__Race=raceResult.Race).delete()
  trackLength = float(xml.getElementsByTagName('TrackLength')[0].childNodes[0].nodeValue)
  driverResults = xml.getElementsByTagName('Driver')
  for driverResult in driverResults:
    resultToSave: web.models.DriverResult = web.models.DriverResult()
    resultToSave.RaceResult = raceResult # yes, it's redundant, but it makes querying simpler
    resultToSave.AverageSpeed = 0.0
    resultToSave.ArePointsScoring = True
    resultToSave.ArePointsScoringForTeam = True

    # Find referenced fields
    laps = list()
    teamName =  ""
    driverFirstName  = ""
    driverLastName  = ""
    finishStatus = ""
    for node in driverResult.childNodes:
      if "Element" in str(type(node)) and node.tagName in RFACTOR2NODEMAP:
        setattr(resultToSave,RFACTOR2NODEMAP[node.tagName],node.childNodes[0].nodeValue)
      elif "Element" in str(type(node)):
        if node.tagName == "Lap":
          # parse the laps
          lap = web.models.Lap()
          position = node.attributes["p"].value
          lapNumber = node.attributes["num"].value
          duration = node.childNodes[0].nodeValue
          lap.Position = position
          lap.Number = lapNumber
          lap.Duration = duration
          laps.append(lap)
        elif node.tagName =="TeamName":
          teamName = node.childNodes[0].nodeValue
        elif node.tagName =="Name":
          rawDriverName = node.childNodes[0].nodeValue
          name = HumanName(rawDriverName)
          driverFirstName = name.first
          if name.middle != "":
            driverLastName = name.middle + " " + name.last
          else:
            driverLastName = name.last
        elif node.tagName == "FinishStatus":
          resultToSave.FinishStatus  = web.models.FinishStatus.objects.get(Name=node.childNodes[0].nodeValue)
        elif node.tagName == "CarType":
          resultToSave.VehicleClass = web.models.VehicleClass.objects.get(Name=node.childNodes[0].nodeValue)
    # find the team entry
    teamQuery = web.models.TeamEntry.objects.filter(Name=teamName,Season=raceResult.Race.Season)
    if teamQuery.count() == 1:
      # team is signed up, continue
      team = teamQuery.first()
      driverQuery = team.Drivers.filter(FirstName=driverFirstName, LastName=driverLastName)
      driver = driverQuery.first()
      if team  is not None and driver is not None:
        # insert result
        resultToSave.Driver = driver
        resultToSave.save()
        overallTimeNeeded = 0.0
        completedDistance = trackLength * len(laps) / 1000
        for lap in laps:
          lap.save()
          resultToSave.Laps.add(lap)
          overallTimeNeeded = overallTimeNeeded + float(lap.Duration)
        resultToSave.AverageSpeed = round(completedDistance/ (overallTimeNeeded/60/60),2)
        resultToSave.save()
        raceResult.DriverResults.add(resultToSave) 
    resultList.append(resultToSave)
  return resultList