
def calculateDec_degs( obs, negative_or_postive ):

    dec_degrees = int( obs["dec_degrees"] )
    dec_minutes = int( obs["dec_minutes"] )
    dec_seconds = float( obs["dec_seconds"] )

    if negative_or_postive == 'positive': #greater than or equal
        dec = dec_degrees + (dec_minutes / 60.) + (dec_seconds / 3600.)
        #stop
    else: #dec is negative
        dec = dec_degrees - (dec_minutes / 60.) - (dec_seconds / 3600.)
        #print ('dec', dec)


    
    dec_degs = round( dec, 6 )
    #print ('dec_degs', dec_degs)

    return dec_degs


if __name__ == "__main__":

    #quick_test

    dec_degrees = -0
    dec_minutes = 7
    dec_seconds = 30.6
    obs = {}
    obs["dec_degrees"] = dec_degrees
    obs["dec_minutes"] = dec_minutes
    obs["dec_seconds"] = dec_seconds

    dec_degs = calculateDec_degs( obs, 'negative' )

    #print ('dec_degs', dec_degs)