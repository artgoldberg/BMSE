'''
Solar system generator
Requirements:
    Locations
        Solid planets near the star
        Gasseous planets outside the solid planets
        Frozen plaents outside the gasseous planets
    Simulate GmM/r2 gravity
    Numbers of planets
        Between 0 and 4 solid, 2 and 4 gasseous, and 1 and 8 frozen
    Initial orbital data for each planet
        Distance from star
        Specify elliptical parameters
        Assume all orbits co-planar
    Generate random SS within parameters
'''

class SolarSystem(object):
    '''
    attributes:
        initial position
    methods:
        enumerate by position
        is_stable()
    '''
    def __init__(self):
        pass

class Planet(object):
    '''
    attributes:
        mass
        orbital radius, elliptical parameters
        physical radius
        name
        has_atmosphere
        
    methods:
        density()
        planet_type() # depends on density & distance from star, and star type
        instantaneous_velocity()
        
    '''

    def __init__(self):
        pass

class Star(object):
    '''
    attributes:
    methods:
    '''

    def __init__(self):
        pass

def main():
    '''
    input arguments
    create solar system
    create all planet
    '''