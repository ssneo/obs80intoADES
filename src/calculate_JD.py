
from astropy.time import Time

def calculteJD( time_value ):

    date= "%s-%s-%s"%(time_value['year'], time_value['month'], time_value['day'] )
    dateTime = date + "T00:00:00.0"
    t = Time( dateTime, format='isot', scale='utc' )
    #print ('t.jd', t.jd)
    #print ('time', self.obs[i]['time'])
    jd = t.jd + float( time_value['time'] )
    #print ('jd', jd)
    #stop
    return str(jd)