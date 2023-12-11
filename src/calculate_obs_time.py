


def calculateObsTime( time_value ):

    #obsTime format is yyyy-mm-ddThh:mm:ss.sssZ
    date = "%s-%s-%s"%(time_value['year'], time_value['month'], time_value['day'] )

    #convert obs80 time into HMS

    time = float( time_value['time'] )
    #print ('time', time)

    hours_1 =  time * 24
    hours = int( hours_1 )
    hours_rem = hours_1 - hours
    #print ('h', hours_1, hours, hours_rem,)
    minutes_1 = hours_rem * 60
    minutes = int( minutes_1)
    minutes_rem = minutes_1 - minutes
    #print ('m', minutes_1, minutes, minutes_rem)
    seconds_1 = minutes_rem * 60
    seconds = int( seconds_1 )
    seconds_rem = int( round( seconds_1 - seconds, 2) * 100) #this needs to be a whole number value
    #print ('s', seconds_1, seconds, seconds_rem)

    hours = str( hours ).zfill(2)
    minutes = str( minutes ).zfill(2)
    seconds = str( seconds ).zfill(2)

    #print (hours, minutes, seconds)

    time = '%s:%s:%s.%s'%(hours, minutes, seconds, seconds_rem)

    

    obsTime = "%sT%sZ"%(date, time)

    return obsTime