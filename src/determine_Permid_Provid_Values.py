


def determinePermidProvidValues( name ):
    #print ('name', name)

    characters = [ "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "~" ]

    we_have_packed_number   = False
    we_have_packed_provid   = False
    we_have_neocp           = False
    
    if name[0] != " ": #this mean we have a numbered asteroid
        we_have_packed_number = True

        packed_number = name[0:5]

        character_value = None
        for j in range( 0, len( characters ) ):
            if name[0] == characters[j]:
                character_value = j
                break

        #print ('character_value', character_value)
        if character_value != None:
            character2Number = j + 10
            unpacked_number = str( character2Number) + name[1:5]
        else:
            unpacked_number = packed_number
            #print ("Correct Character_value was not found: name = %s"%(name))

        

    #print (name[5], name[6], name[7])
    if we_have_packed_number == False:
        if name[5] == "K" or name[5] == "J":
            try:
                int( name[6:8] ) #these two values should be a number
                if len( name.replace(" ", "") ) == 7: #a packed provid is only 7 characters long
                    we_have_packed_provid = True
            except:
                we_have_neocp = True
        else:
            we_have_neocp = True

    if we_have_packed_provid == True:
        first_half_of_year = None
        second_half_of_year = None
        first_letter = None
        second_letter = None
        first_number = None
        second_number = None

        if name[5] == 'K':
            first_half_of_year = '20'
        elif name[5] == 'J':
            first_half_of_year = '19'
        else:
            print ('Error: Could not determine first half of year for: %s'%(name) )

        #print ('first_half_of_year', first_half_of_year)

        second_half_of_year = name[6:8]

        #print ('second_half_of_year', second_half_of_year)

        first_letter = name[8]
        #print ('first_letter', first_letter)

        first_number = name[9]
        #print ('first_number', first_number)
        try:
            int(first_number) #if the value is  not a number then need to run the character search
        except:
            #print ('fail1')
            character_value = None
            for j in range( 0, len( characters ) ):
                if first_number == characters[j]:
                    character_value = j
                    break
            if character_value != None:
                character2Number = j + 10
                first_number = character2Number

        #print ('first_number', first_number, type(first_number))

        second_number = name[10]
        #print ('second_number', second_number)

        second_letter = name[11]
        #print ('second_letter', second_letter)

        if first_number == "0": #don't include the first zero
            if second_number != "0":
                unpacked_provid = f"{first_half_of_year}{second_half_of_year} {first_letter}{second_letter}{second_number}"
            else:
                unpacked_provid = f"{first_half_of_year}{second_half_of_year} {first_letter}{second_letter}"
        else:
            unpacked_provid = f"{first_half_of_year}{second_half_of_year} {first_letter}{second_letter}{first_number}{second_number}"
        #print ('unpacked_provid', unpacked_provid)

        #unpacked_provid = f"{first_half_of_year}{second_half_of_year} "
        #print ('unpacked_provid', unpacked_provid)

        #unpacked_provid = f"{first_letter}{second_letter}"
        #print ('unpacked_provid', unpacked_provid)

        #unpacked_provid = f"{first_number}{second_number}"
        #print ('unpacked_provid', unpacked_provid)


    #print (we_have_packed_number, we_have_packed_provid, we_have_neocp)
    if we_have_packed_number == True:
        permid  = unpacked_number
        provid  = None
        trksub   = name.replace(" ", "")

    elif we_have_packed_provid == True:
        permid  = None
        provid  = unpacked_provid
        trksub   = name.replace(" ", "")

    if we_have_neocp == True:
        permid  = None
        provid  = None
        trksub   = name.replace(" ", "")
    #print ('permid', permid, 'provid', provid)
    #stop

    return permid, provid, trksub

        