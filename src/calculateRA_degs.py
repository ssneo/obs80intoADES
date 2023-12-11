

def calculateRa_degs( obs ):
    ra_hour = int( obs['ra_hour'] )
    ra_minutes = int( obs['ra_minutes'] )
    ra_seconds = float( obs['ra_seconds'] )

    ra = ra_hour + (ra_minutes/60.) + (ra_seconds/3600.)
    ra_degs = round( (ra * 15.), 6 )

    return ra_degs