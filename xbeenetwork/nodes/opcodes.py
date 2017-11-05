"""A list of Opcodes for Roomba Control."""

sensorpackets = {
    19: ('distance', '>h'),
    20: ('angle', '>h'),
    21: ('charging state', 'B'),
    22: ('voltage', 'H'),
    23: ('current', 'H')
}
