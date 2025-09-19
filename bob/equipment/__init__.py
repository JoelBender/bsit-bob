from ..core import P223, S223, Equipment, LocationReference, Property, PropertyReference

"""
Depending on the nature of equipment, some are considered s223:System, other
s223:Equipment. 

This lead to potential import issues when using the library as the user will
have to know upfront if he's looking for a Equipment or a system. 

By merging both modules into one, it'll be easier to find what we look for.

"""
_namespace = P223


class _Actuator(Equipment):
    """
    This version of an actuator is meant to be the opposite of a sensor
    It relates properties to an action
    It can be located with hasActuationLocation (mirror of hasObservationLocation)

    This way, the model can illutrate the link between a property and something else (like
    a connection point)
    example :


    __|___|__|___|___|__
    |  Supply Fan      |------------s223:hasProperty--------(flow)
    |  s223:Equipment  |------------s223:hasProperty--------(OnOffCommand) <-> A
    |  s223:Fan        |------------s223:hasProperty--------(rotation) <-> B
    |                  |------------s223:hasProperty--------(status)
    |__________________|------------s223:hasConnectionPoint----(AirOutlet) <-> C
            |                               ____________________
            |___________s223:contains_______|  OnOff Actuator  |---s223:isCommandedBy----------(OnOffCommand) <-> A
                                            |  P223:Actuator   |---p223:actuatesProperty ------(rotation) <-> B
                                            |__________________|---p223:hasActuationLocation---(AirOutlet) <-> C


    This shows that the actuator is `commandedBy` the property "OnOffCommand". This actuation takes place at the air outlet of the fan.
    The actuator "actuates" the speed_ratio of the fan which is a property of the fan representing the fact that it can be stopped (speed_ratio
    of 0%) or run at a speed which is >0% to 100%.

    The speed ratio property is not a property that is meant to be observed. It is an intrinsic property of a fan, it is the fact that it can run.
    It represents the core function of the fan.

    A damper would have a shaft_position(?) property, a pump would also have something similar to speed_ratio. All Equipment should have one main "function"
    property.

    A sensor could be used to observe the "status" of the fan. We shall resist to relate the actuator to the status. The actuator do
    not actuate the status, it actuates the rotation of the fan and if we observe it, the status should be On.

    An actuator should not have CP. Its role is to represent the relaiton between properties and action.

    """

    _class_iri = P223.Actuator
    isCommandedBy: PropertyReference
    actuatesProperty: PropertyReference
    hasActuationLocation: LocationReference
