
from astropy.time import Time

def calculateJD( time_value ):

    date= "%s-%s-%s"%(time_value['year'], time_value['month'], time_value['day'] )
    dateTime = date + "T00:00:00.0"
    t = Time( dateTime, format='isot', scale='utc' )

    jd = t.jd + float( time_value['time'] )

    return str(jd)