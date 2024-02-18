
def format_data( data):
    
    data_line = ""

    if 'permID' in data:
        data_line += f"{data['permid']:<15}|"

    if 'provID' in data:
        data_line += f"{data['provid']:<15}|"

    if 'trkSub' in data:
        data_line += f"{data['trkSub']:<8}|"

    if 'mode' in data:
        data_line += f"{data['mode']:<4}|"

    if 'stn' in data:
        data_line += f"{data['stn']:<4}|"

    if 'obsTime' in data:
        data_line += f"{data['obsTime']:<24}|"

    if 'ra' in data:
        data_line += f"{data['ra']:<13}|"

    if 'dec' in data:
        data_line += f"{data['dec']:<13}|"

    if 'rmsRA' in data:
        data_line += f"{data['rmsRA']:<7}|"

    if 'rmsDec' in data:
        data_line += f"{data['rmsDec']:<7}|"

    if 'astCat' in data:
        data_line += f"{data['astCat']:<8}|"

    if 'mag' in data:
        data_line += f"{data['mag']:<7}|"

    if 'band' in data:
        data_line += f"{data['band']:<4}|"

    if 'photCat' in data:
        data_line += f"{data['photCat']:<8}|"



    data_line = data_line[:-1] #all by the last '|' symbol


    return data_line

def format_header( data_dic ):

    header_line = ""

    if 'permid' in data_dic[0]:
        header_line += f"{'permid':<15}|"

    if 'provid' in data_dic[0]:
        header_line += f"{'provid':<15}|"

    if 'trkSub' in data_dic[0]:
        header_line += f"{'trkSub':<8}|"

    if 'mode' in data_dic[0]:
        header_line += f"{'mode':<4}|"

    if 'stn' in data_dic[0]:
        header_line += f"{'stn':<4}|"

    if 'obsTime' in data_dic[0]:
        header_line += f"{'obsTime':<24}|"

    if 'ra' in data_dic[0]:
        header_line += f"{'ra':<13}|"

    if 'dec' in data_dic[0]:
        header_line += f"{'dec':<13}|"

    if 'rmsRA' in data_dic[0]:
        header_line += f"{'rmsRA':<7}|"

    if 'rmsDec' in data_dic[0]:
        header_line += f"{'rmsDec':<7}|"

    if 'astCat' in data_dic[0]:
        header_line += f"{'astCat':<8}|"

    if 'mag' in data_dic[0]:
        header_line += f"{'mag':<7}|"

    if 'band' in data_dic[0]:
        header_line += f"{'band':<4}|"

    if 'photCat' in data_dic[0]:
        header_line += f"{'photCat':<8}|"



    header_line = header_line[:-1] #all by the last '|' symbol


    return header_line

    

    #stop


def generate_psv( head_dict, data_dic, ades_filename):

    

    #for key in head_dict:
    #    print (key, head_dict[key])

    for key in data_dic:
        print (key, data_dic[key])
    

    file = open( ades_filename, 'w')

    file.write( '# version=2022\n' )

    file.write( '# observatory\n' )
    file.write( '! mpcCode %s\n'%( head_dict['mpcCode'] ) )
    file.write( '! name %s\n'%( head_dict['observatoryName'] ) )

    file.write( '# submitter\n' )
    file.write( '! name %s\n'%( head_dict['submitter'] ) )

    file.write( '# telescope\n' )
    file.write( '! aperture %s\n'%( head_dict['telescope_aperture'] ) )
    file.write( '! design %s\n'%( head_dict['telescope_design'] ) )
    file.write( '! detector %s\n'%( head_dict['telescope_detector'] ) )

    file.write( '# observers\n' )
    observers = head_dict['observers'].split(',')
    for i in observers:
        if i[0] == ' ': #is there a leading space
            file.write( '! name %s\n'%( i[1:] ) )
        else:
            file.write( '! name %s\n'%( i ) )

    file.write( '# measurers\n' )
    observers = head_dict['measurers'].split(',')
    for i in observers:
        if i[0] == ' ': #is there a leading space
            file.write( '! name %s\n'%( i[1:] ) )
        else:
            file.write( '! name %s\n'%( i ) )

    header_line = format_header( data_dic )

    #print ('header_line', header_line)

    file.write( '%s\n' %( header_line ) )

    for key in data_dic:
        data_line = format_data( data_dic[key] )

        file.write( '%s\n' %( data_line ) )











    
    



    file.close()

    #print ('data_dic', data_dic)
        
    



    stop




if __name__ == "__main__":

    generate_psv()