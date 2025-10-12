# Competency Questions

## 1. How many lights are on?#

Find the external references for lights which could be read to determine if the light is on.
(Suggestion: for this exercise, let's use hasValue instead of hasExternalReference so that we can execute the queries)



```
match (d:Luminaire)-[:onOffStatus]-(s {hasValue: 1})  return count(d)
# result = 2
```

### Explanation
In the model I set the corridor lights to On (OnOffStatus.hasValue=1)

And the Bathroom to Off (OnOffStatus.hasValue=0)
```
match (d:Luminaire)-[:onOffStatus]-(s {hasValue: 0})  return count(d)
# result = 1
```

## 2. What is the average temperature of spaces fed by VAV box 1? What are the min and max?

Find VAV Box 1
```
match (d:VAV {label:"VAVBox1"}) return d
```

It's a System. Let's use servesZone to find space then lookup for Zone Temperature in all spaces

```
match path=(d:VAV {label:"VAVBox1"})-[:servesZone]-(z)-[:contains]-(s:HVACSpace)
WITH s
MATCH (s)<-[:hasObservationLocation]-(t:Sensor)
WITH t
MATCH path=(t)-[:observes]-()-[:hasExternalReference]-(bacnet) return path
```

```
match path=(d:VAV {label:"VAVBox1"})-[:servesZone]-(z)-[:contains]-(s:HVACSpace)
WITH s
MATCH (s)<-[:hasObservationLocation]-(t:Sensor)
WITH t
MATCH (t)-[:observes]-(temp) return temp.hasValue
```


To answer the "number" part, we need to lookup the BACnet value(s)

## 3. What are all the temperature sensors?

```
MATCH (t:TemperatureSensor) return t
```

## 4. What is the average temperature of unoccupied rooms?

Tricky. Depends on how the model is made and what we think is given
by the occupancy sensors.
The typical sensors I know give pulses.
There is a controller somewhere that give the occupancy status.

## 5. Turn off lights in unoccupied spaces.


## 6. What occupancy sensors are available in a particular zone?
```
match (:Zone)-[:contains]-()<-[:hasObservationLocation]-(os:MovementSensor) return count(os)
```

## REQUEST TO FOLLOW AIR
```
match (c:Connection)
WITH c
match (c)-[:hasMedium]-(m) where m.uri contains "Air"
WITH *
match path=()-[:connectedThrough]-(c) return path
```
