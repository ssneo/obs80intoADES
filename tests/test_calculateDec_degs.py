
import os
import sys
import pytest


cwd = os.getcwd()
parentName = os.path.dirname( cwd )
parentName = os.path.join( parentName, 'src' )
sys.path.insert( 0, parentName )

from calculateDec_degs import calculateDec_degs


def test_calculateDec_degs_0():

    #test basic value
    
    dec_degrees = 0
    dec_minutes = 0
    dec_seconds = 0
    obs = {}
    obs["dec_degrees"] = dec_degrees
    obs["dec_minutes"] = dec_minutes
    obs["dec_seconds"] = dec_seconds

    dec_deg = calculateDec_degs( obs )

    print ('dec_deg', dec_deg)


    if dec_deg == 0.0:
        assert True
    else:
        assert False


def test_calculateDec_degs_1():

    #test basic value
    
    dec_degrees = 1
    dec_minutes = 2
    dec_seconds = 3
    obs = {}
    obs["dec_degrees"] = dec_degrees
    obs["dec_minutes"] = dec_minutes
    obs["dec_seconds"] = dec_seconds

    dec_deg = calculateDec_degs( obs )

    print ('')
    print ('dec_deg', dec_deg)
    #print ('hello good bye')


    if dec_deg == 1.034167:
        assert True
    else:
        assert False

def test_calculateDec_degs_2():

    #test basic value
    
    dec_degrees = 0
    dec_minutes = 7
    dec_seconds = 30.6
    obs = {}
    obs["dec_degrees"] = dec_degrees
    obs["dec_minutes"] = dec_minutes
    obs["dec_seconds"] = dec_seconds

    dec_deg = calculateDec_degs( obs )

    print ('')
    print ('dec_deg', dec_deg)
    #print ('hello good bye')


    if dec_deg == 0.125167:
        assert True
    else:
        assert False
    