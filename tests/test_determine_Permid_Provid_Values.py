
import os
import sys
import pytest


cwd = os.getcwd()
parentName = os.path.dirname( cwd )
parentName = os.path.join( parentName, 'src' )
sys.path.insert( 0, parentName )

from determine_Permid_Provid_Values import determinePermidProvidValues


def test_permid_provid_values_0():

    #test basic file name
    name = '     K20V01N'

    permid, provid, trksub = determinePermidProvidValues( name )

    if permid == None and provid == '2020 VN1' and trksub == 'K20V01N':

        assert 1 == 1
    else:
        assert 1 == 0

def test_permid_provid_values_1():

    #test basic file name
    name = '     K23X00A'

    permid, provid, trksub = determinePermidProvidValues( name )

    if permid == None and provid == '2023 XA' and trksub == 'K23X00A':

        assert 1 == 1
    else:
        assert 1 == 0


    