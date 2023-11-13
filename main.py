
from tkinter import *
from tkinter.scrolledtext import ScrolledText
import os
import json
from create_ades import generate_xml, update_xml
from datetime import datetime
import glob
import xml.etree.ElementTree as XMLElement
import xml.dom.minidom as minidom

class autoOperations:

    def __init__(self):

        self.mp = Tk()

        #self.mp.geometry("400x300")

        self.mp.title("Turn Obs80 Into ADES")

        mainLabel = Label(self.mp, text='Turn Obs80 Into ADES', bg='white', fg='blue', font=('times', 20, 'bold'), height=1, width=20).grid(row=0, column=0, columnspan=20, sticky = N+S+W+E)

        #self.text_area = ScrolledText( self.mp, wrap="word", width=100, height=10, font= ("Times New Roman", 10) )
        #self.text_area.grid( row=50, column=0, columnspan=21 ) 

        cwd = os.getcwd()
        #print ('cwd', cwd)
        config_files = glob.glob( cwd + "\\config*.json")
        self.config_val = StringVar()
        self.config_val.set( config_files[0] )
        self.previous_config_file = self.config_val.get()
        config_files_menu = OptionMenu(self.mp, self.config_val, *config_files)
        config_files_menu.grid( row = 1, column = 0, columnspan=5, sticky=W )

        #load the selected_config_file
        with open( config_files[0] ) as infile:
            self.config = json.load(infile)

        Label( self.mp, text='Submiter').grid(row=2, column=0, sticky=W)
        self.submiter_for_ades = Label( self.mp, text=self.config["NAME_FOR_THE_ADES_SUBMITTER_FIELD"] )
        self.submiter_for_ades.grid( row=2, column = 1, columnspan=2, sticky = W)

        Label( self.mp, text='Observatory').grid(row=2, column=3, sticky=E)
        self.observatory_for_ades = Label( self.mp, text=self.config["OBSERVATORY_NAME_FOR_ADES"] )
        self.observatory_for_ades.grid( row=2, column = 4, columnspan=2, sticky = W)

        Label( self.mp, text='Observers').grid(row=3, column=0, sticky=W)
        self.observers_for_ades = Label( self.mp, text=self.config["OBSERVERS_FOR_ADES"] )
        self.observers_for_ades.grid( row=3, column = 1, columnspan=2, sticky = W)

        Label( self.mp, text='Tel Design').grid(row=3, column=3, sticky=W)
        self.tel_design_for_ades = Label( self.mp, text=self.config["TELESCOPE_DESIGN_FOR_ADES"] )
        self.tel_design_for_ades.grid( row=3, column = 4, columnspan=2, sticky = W)

        Label( self.mp, text='Measures').grid(row=4, column=0, sticky=W)
        self.measures_for_ades = Label( self.mp, text=self.config["MEASURERS_FOR_ADES"] )
        self.measures_for_ades.grid( row=4, column = 1, columnspan=2, sticky = W)

        Label( self.mp, text='Tel Aperture').grid(row=4, column=3, sticky=E)
        self.tel_aperture_for_ades = Label( self.mp, text=self.config["TELESCOPE_APERTURE_FOR_ADES"] )
        self.tel_aperture_for_ades.grid( row=4, column = 4, columnspan=2, sticky = W)

        Label( self.mp, text='Funding Agency').grid(row=5, column=0, sticky=W)
        self.funding_agency_for_ades = Label( self.mp, text=self.config["FUNDING_AGENCY_FOR_ADES"] )
        self.funding_agency_for_ades.grid( row=5, column = 1, sticky = W)

        Label( self.mp, text='Tel Detector').grid(row=5, column=3, sticky=E)
        self.tel_detector_for_ades = Label( self.mp, text=self.config["TELESCOPE_DETECTOR_FOR_ADES"] )
        self.tel_detector_for_ades.grid( row=5, column = 4, columnspan=2, sticky = W)

        

        
        Button( self.mp, text='Reload Obs80', command=self.reloadObs80Button ).grid(row=9, column=5, columnspan=2, sticky=W+E)
        Label( self.mp, text='Use').grid(row=10, column=0)
        Label( self.mp, text='Permid').grid(row=10, column=1)
        Label( self.mp, text='Provid').grid(row=10, column=2)
        Label( self.mp, text='Obs80').grid(row=10, column=3, sticky=W+E)
        Label( self.mp, text='FWHM', width=10).grid(row=10, column=4, sticky=W+E)
        Label( self.mp, text='SNR', width=10).grid(row=10, column=5, sticky=W+E)
        Label( self.mp, text='POS_UNC', width=10).grid(row=10, column=6, sticky=W+E)
        Button( self.mp, text='Submit Obs', command=self.submit_obs ).grid(row=50, column=5, columnspan=2, sticky=W+E)

        self.reloadObs80Button()

        self.checkIfConfigFileWasUpdated()
        
        mainloop()

    def checkIfConfigFileWasUpdated( self ):

        #print (self.config_val.get())
        if self.config_val.get() != self.previous_config_file:

            with open( self.config_val.get() ) as infile:
                self.config = json.load(infile)

            self.submiter_for_ades.config( text=self.config["NAME_FOR_THE_ADES_SUBMITTER_FIELD"]  )
            self.observatory_for_ades.config( text=self.config["OBSERVATORY_NAME_FOR_ADES"] )
            self.observers_for_ades.config( text=self.config["OBSERVERS_FOR_ADES"]  )
            self.tel_design_for_ades.config( text=self.config["TELESCOPE_DESIGN_FOR_ADES"]  )
            self.measures_for_ades.config( text=self.config["MEASURERS_FOR_ADES"]  )
            self.tel_aperture_for_ades.config( text=self.config["TELESCOPE_APERTURE_FOR_ADES"]  )
            self.funding_agency_for_ades.config( text=self.config["FUNDING_AGENCY_FOR_ADES"]  )
            self.tel_detector_for_ades.config( text=self.config["TELESCOPE_DETECTOR_FOR_ADES"]  )

            self.previous_config_file = self.config_val #reset the previous value


        
        refreshRate = 500
        self.measures_for_ades.after(refreshRate, self.checkIfConfigFileWasUpdated)

    def reloadObs80Button(self):

        self.readObs80()

        #print (len( self.obs ) )

        self.checkBoxList = []
        self.dic = {}
        listOfHeaderValues = ["COD", "CON", "OBS", "MEA", "TEL", "ACK", "AC2", "NET", "---"]
        end = 20
        #if len( self.obs ) > 20:
        #    end = 20
        #else:
        #    end = len( self.obs )
        for i in range( 0, end ):
            useObs = True
            #print (self.obs80[i][0:3])
            
            if len( self.obs) != 0 and i < len( self.obs ) : #is i variable greater than the number of obs, this means we need to send destroy commands
                for j in listOfHeaderValues:
                    
                    if self.obs[i]['obs80'][0:3] == j:
                        useObs = False
                
                if useObs == True:
                    self.dic[i] = {}
                    self.dic[i]['variable'] = IntVar()
                    #self.dic[i]['button'] = Checkbutton( self.mp, text=self.obs80[i], variable = self.dic[i]['variable'], onvalue=1, offvalue=0, height=2, width=100)
                    self.dic[i]['button'] = Checkbutton( self.mp, variable = self.dic[i]['variable'], onvalue=1, offvalue=0, height=2, width=5)
                    row_value = 20 + i
                    self.dic[i]['button'].grid(row=row_value, column=0, stick=W)
                    self.dic[i]['variable'].set(1)

                    permid, provid = self.determinePermidProvidValues( self.obs[i]['name'] )
                    #print (permid, provid)

                    self.dic[i]['entry_permid'] = Entry(  width=8 )
                    self.dic[i]['entry_permid'].grid( row=row_value, column=1, sticky=W+E)
                    if permid != None:
                        self.dic[i]['entry_permid'].insert(0, permid)
                    

                    self.dic[i]['entry_provid'] = Entry( width=8 )
                    self.dic[i]['entry_provid'].grid( row=row_value, column=2, sticky=W+E)
                    if provid != None:
                        self.dic[i]['entry_provid'].insert(0, provid)

                    

                    

                    self.dic[i]['label_obs80'] = Label( self.mp, text=self.obs[i]['obs80'] )
                    self.dic[i]['label_obs80'].grid(row=row_value, column=3, sticky=W)

                    if 'fwhm' in self.obs[i]: #if 'fwhm key does not exist there was a fail
                        self.dic[i]['label_fwhm'] = Label( self.mp, text=self.obs[i]['fwhm'] )
                        self.dic[i]['label_snr'] = Label( self.mp, text=self.obs[i]['snr'] )
                        self.dic[i]['label_pos_unc'] = Label( self.mp, text=self.obs[i]['pos_unc'] )
                    else:
                        self.dic[i]['label_fwhm'] = Label( self.mp, text='n/a', bg='red' )
                        self.dic[i]['label_snr'] = Label( self.mp, text='n/a', bg='red' )
                        self.dic[i]['label_pos_unc'] = Label( self.mp, text='n/a', bg='red' )
                        self.dic[i]['variable'].set(0)
                        

                    self.dic[i]['label_fwhm'].grid(row=row_value, column=4, sticky=W+E)
                    self.dic[i]['label_snr'].grid(row=row_value, column=5, sticky=W+E)
                    self.dic[i]['label_pos_unc'].grid(row=row_value, column=6, sticky=W+E)

            else:
                try:
                    self.dic[i]['button'].destory
                    self.dic[i]['entry_permid'].destory
                    self.dic[i]['entry_provid'].destory
                    self.dic[i]['label_obs80'].destory
                    self.dic[i]['label_fwhm'].destory
                    self.dic[i]['label_snr'].destory
                    self.dic[i]['label_pos_und'].destory
                except:
                    #print ('no destory')
                    pass

    def readObs80(self):

        #cwd = os.getcwd()
        #config_path = os.path.join( cwd, "config.json")
        #with open(config_path) as infile:
        #    self.config = json.load(infile)

        location_of_astrometrica_log_files = self.config["LOCATION_OF_ASTROMETRICA_LOG_FILES"]

        file_path = os.path.join( location_of_astrometrica_log_files, "MPCReport.txt" )
        try:
            file = open( file_path, 'r')
            self.obs80 = file.readlines()
            file.close()
        except:
            self.obs80 = {}

        file_path = os.path.join( location_of_astrometrica_log_files, "Astrometrica.log" )
        try:
            file = open( file_path, 'r')
            self.log = file.readlines()
            file.close()
        except:
            self.log = {}

        file_path = os.path.join( location_of_astrometrica_log_files, "PhotReport.txt" )
        try:
            file = open( file_path, 'r')
            self.phot = file.readlines()
            file.close()
        except:
            self.phot = {}

        #build a dictionary with all of the fields that Astrometrica can provide between the three files. Then get all of the information into a single location

        self.obs = {}
        self.header = {}
        listOfHeaderValues = ["COD", "CON", "OBS", "MEA", "TEL", "ACK", "AC2", "NET", "---"]
        catalog = None
        measures = None
        observers = None
        acknowledge_email = None
        tel_line = None
        count = 0
        for i in range( 0, len( self.obs80 ) ): #loop through each observations in the MPCReport.txt file

            useObs = True
            
            for j in listOfHeaderValues:
                if self.obs80[i][0:3] == j:
                    useObs = False
                    if j == "COD":
                        mpc_code = self.obs80[i][4:-1]
                    if j == "CON":
                        address = self.obs80[i][4:-1]
                    if j == "OBS":
                        observers = self.obs80[i][4:-1]
                    if j == "MEA":
                        measures = self.obs80[i][4:-1]
                    if j == "TEL":
                        tel_line = self.obs80[i][4:-1]
                    if j == "AC2":
                        acknowledge_email = self.obs80[i][4:-1]
                    if j == "NET":
                        catalog = self.obs80[i][4:-1]

            if useObs == True: #if the is not a header or the end line
                self.obs[count] = {}
                #from MPCReport.txt File
                self.obs[count]['obs80'] = self.obs80[i][:-1]
                self.obs[count]['name'] = self.obs80[i][0:13]
                if self.obs80[i][14] == 'C':
                    date_start = 15
                elif self.obs80[i][15] == 'C':
                    date_start = 16

                #print ( self.obs80[i][15], self.obs80[i][16] )

                self.obs[count]['year'] = self.obs80[i][date_start : (date_start + 4) ]
                self.obs[count]['month'] = self.obs80[i][ (date_start + 5) : (date_start + 7) ]
                self.obs[count]['day'] = self.obs80[i][ (date_start + 8) : (date_start + 10) ]
                self.obs[count]['time'] = self.obs80[i][ (date_start + 11) : (date_start + 17) ].replace(" ", "") #get rid of the extra spaces
                self.obs[count]['ra_hour'] = self.obs80[i][32:34]
                self.obs[count]['ra_minutes'] = self.obs80[i][35:37]
                self.obs[count]['ra_seconds'] = self.obs80[i][38:43]
                self.obs[count]['ra_hms'] = "%s:%s:%s"%(self.obs[count]['ra_hour'], self.obs[count]['ra_minutes'], self.obs[count]['ra_seconds'])
                self.obs[count]['dec_degrees'] = self.obs80[i][44:47]
                self.obs[count]['dec_minutes'] = self.obs80[i][48:50]
                self.obs[count]['dec_seconds'] = self.obs80[i][51:56].replace(" ", "") #get rid of a possible trailing blank space
                self.obs[count]['dec_dms'] = "%s:%s:%s"%(self.obs[count]['dec_degrees'], self.obs[count]['dec_minutes'], self.obs[count]['dec_seconds'])
                self.obs[count]['mag'] = self.obs80[i][65:70]
                self.obs[count]['filter'] = self.obs80[i][70]
                self.obs[count]['obs_code'] = self.obs80[i][77:80]
                
                
                #header information is now required to be in the config file
                self.header['obs_code'] = mpc_code
                self.header['address'] = mpc_code
                self.header['observers'] = observers
                self.header['measurers'] = measures
                self.header['tel_line'] = tel_line
                self.header['acknowledge_email'] = acknowledge_email
                if catalog == 'UCAC-3':
                    catalog = "UCAC3" #mpc has changed their requirement
                self.header['catalog'] = catalog


                #match information from log.log File
                for k in range( 0, len( self.log ) ):
                #print (self.obs[count]['obs80'] )
                #for k in range( 1816, len( self.log ) ): #for testing
                    #print ('count', count, 'k', k)
                    obsMatch = False
                    obsMatch_ra = False
                    obsMatch_dec = False
                    #make sure log length line is more than 100 characters
                    if len( self.log[k] ) > 100:

                        #if k > 118 and k < 120:
                        #    print (self.log[k] )
                        #    print (self.log[k][2:4])
                        #    print (self.log[k][5:7])
                        #    print (self.log[k][8:13])
                        #    print (self.log[k][8:12])
                        #    print (self.log[k][25:28])
                        #    print (self.log[k][29:31])
                        #    print (self.log[k][32:37])
                        #    print (self.log[k][32:36])

                        #check if RA matches
                        if self.log[k][2:4] == self.obs[count]['ra_hour']: #check that ra_hour matches 
                            #print ('yes1')
                            if self.log[k][5:7] == self.obs[count]['ra_minutes']: #check that ra_minute matches
                                #print ('yes2')
                                if len( self.obs[count]['ra_seconds'] ) == 6: #there is a rounding issue to deal with in the obs80 line depending on the precision of the format
                                    #if 6 characters long then it should be a direct match to the log file
                                    #print ('yes3')
                                    if self.log[k][8:13] == self.obs[count]['ra_seconds']:
                                        obsMatch_ra = True
                                elif len( self.obs[count]['ra_seconds'] ) == 5:
                                    #print ('yes4')
                                    #print (self.log[k][8:12] == self.obs[count]['ra_seconds'][:-1], self.log[k][8:12], self.obs[count]['ra_seconds'][:-1])
                                    if self.log[k][8:12] == self.obs[count]['ra_seconds'][:-1]: #if only five characters then only going to check five values
                                        obsMatch_ra = True

                        #print (obsMatch_ra)

                        if obsMatch_ra == True:
                            #print ('count', self.obs[count]['obs80'] )
                            #print ('k', self.log[k])
                            if self.log[k][25:28] == self.obs[count]['dec_degrees']: #check that dec_degrees matches 
                                #print ('yes1dec')
                                if self.log[k][29:31] == self.obs[count]['dec_minutes']: #check that dec_degrees matches
                                    #print ('yes2dec')
                                    if len( self.obs[count]['dec_seconds'] ) == 5: #there is a rounding issue to deal with in the obs80 line depending on the precision of the format
                                        #if 6 characters long then it should be a direct match to the log file
                                        #print ('yes3dec')
                                        #The dec_seconds in the log file are saved as xx.yy. However, Obs80 could have xx.y but you can't just compare the .y because of rounding
                                        #therefore, if dec_seconds has a length of 5, then we know it is xx.yy. 
                                        #print (self.log[k][32:37] == self.obs[count]['dec_seconds'], self.log[k][32:37], self.obs[count]['dec_seconds'])
                                        #print (self.log[k][32:36] == self.obs[count]['dec_seconds'][:-1], self.log[k][32:36], self.obs[count]['dec_seconds'][:-1])
                                        #stop
                                        if self.log[k][32:37] == self.obs[count]['dec_seconds']:
                                            obsMatch_dec = True

                                    elif len( self.obs[count]['dec_seconds'] ) == 4:
                                        #print ('yes4dec')
                                        #a dec_seconds length of 4 means we have xx.y therefore we need to round the log file value prior to comparing
                                        log_file_dec_secods = float( self.log[k][32:37] )
                                        log_file_dec_secods = round ( log_file_dec_secods, 1)
                                        #print (log_file_dec_secods == float( self.obs[count]['dec_seconds'] ) , log_file_dec_secods, float( self.obs[count]['dec_seconds'] ) )
                                        if log_file_dec_secods == float( self.obs[count]['dec_seconds'] ): #if only five characters then only going to check five values
                                            obsMatch_dec = True
                        
                        #if obsMatch_ra == True and obsMatch_dec == True:
                            #print (self.log[k] )
                            #print (self.log[k][18:22])
                            #print (self.log[k][41:45])
                            #print (self.log[k][48:53])
                            #print (self.log[k][57:61])
                            #print (self.log[k][64:71])
                            #print (self.log[k][73:80])
                            #print (self.log[k][81:88])
                            #print (self.log[k][90:94])
                            #print (self.log[k][95:102])
                            #print (self.log[k][103:108])


                        #print ( 'obsMatch_ra', obsMatch_ra, 'obsMatch_dec', obsMatch_dec)
                        if obsMatch_dec == True and obsMatch_ra == True:
                            self.obs[count]['ra_error_arc_minutes']     = self.log[k+1][18:22]
                            self.obs[count]['dec_error_arc_minutes']    = self.log[k+1][41:45]
                            self.obs[count]['mag']                      = self.log[k][48:53]
                            self.obs[count]['mag_error']                = self.log[k+1][57:61]
                            self.obs[count]['x_pixel']                  = self.log[k][64:71]
                            self.obs[count]['y_pixel']                  = self.log[k][73:80]
                            self.obs[count]['flux']                     = self.log[k][81:88]
                            if float( self.log[k][90:94] ) == 0.0: #if fwhm is reported to be zero, then assume a 5 for fwhm
                                self.obs[count]['fwhm']                 = float( self.config["IF_NO_FWHM_IS_CALCULTED_USE_VALUE"] )
                            else: 
                                self.obs[count]['fwhm']                 = self.log[k][90:94]
                            self.obs[count]['snr']                      = self.log[k][95:102]
                            self.obs[count]['fit_rms']                  = self.log[k][103:108]
                            self.obs[count]['pos_unc']                  = round( ( float( self.obs[count]['fwhm'] ) / float( self.obs[count]['snr'] ) ) , 2)
                            break #this will break the k loop
                            #stop
                        
                                


                

                #for key in self.obs[count]:
                #    print (key, self.obs[count][key])

                #stop
                count += 1

        with open("astrometrica_data.json", "w") as outfile:
            json.dump(self.obs, outfile)

        with open("astrometrica_header.json", "w") as outfile:
            json.dump(self.obs, outfile)

    def submit_obs( self ):

        fileName = self.build_xml()

        command = 'curl https://minorplanetcenter.net/submit_xml -F "ack=curl_test" -F "ac2=tlinder34@gmail.com" -F "source=<%s" '%(fileName)

        print (command)

        os.system( command )

    def build_xml( self ):

        current_date_time = datetime.utcnow()
        xml_filename = f"xml_output_{ current_date_time.strftime( '%Y' ) }_{ current_date_time.strftime( '%m' ) }_{ current_date_time.strftime( '%d' ) }_{ current_date_time.strftime( '%H' ) }_{ current_date_time.strftime( '%M' ) }_{ current_date_time.strftime( '%S' ) }.xml"

        #xml_filename = "Catalog.xml"

 

        #build ades_header dictionary
        head_dict = {}
        head_dict["mpcCode"]            = self.config["MPC_CODE"]
        if self.config["FUNDING_AGENCY_FOR_ADES"] != "None":
            head_dict["fundingSource"]  = self.config["FUNDING_AGENCY_FOR_ADES"]

        head_dict["observatoryName"]            = self.config["OBSERVATORY_NAME_FOR_ADES"]
        head_dict["submitter"]          = self.config["NAME_FOR_THE_ADES_SUBMITTER_FIELD"]
        head_dict["observers"]          = self.config["OBSERVERS_FOR_ADES"]
        head_dict["measurers"]          = self.config["MEASURERS_FOR_ADES"]
        head_dict["telescope_design"]   = self.config["TELESCOPE_DESIGN_FOR_ADES"]
        head_dict["telescope_aperture"] = self.config["TELESCOPE_APERTURE_FOR_ADES"]
        head_dict["telescope_detector"] = self.config["TELESCOPE_DETECTOR_FOR_ADES"]
        head_dict["fRatio"] = self.config["TELESCOPE_FOCAL_RATIO_FOR_ADES"]
        

        #build ades_data dictionary
        data_dic = {}
        data_dic_count = 0
        for i in range( 0, len( self.obs ) ):

            if self.dic[i]['variable'].get() == 1:

                obsTime = self.calculteObsTime( i )
                ra_degs = self.calculteRa_degs( i )
                dec_degs = self.calculteDec_degs( i )

                #print ('obsTime', obsTime)

                #stop
                #calculte ra_degs and dec_degs 

                data_dic[data_dic_count] = {}
                
                permid = self.dic[i]['entry_permid'].get()
                print ('permid', permid)
                if len( permid ) != 0:
                    data_dic[data_dic_count]['permID']   = permid
                provid = self.dic[i]['entry_provid'].get()
                print ('provid', provid)
                if len( provid ) != 0:
                    data_dic[data_dic_count]['provID']   = provid

                data_dic[data_dic_count]['trkSub']   = "None"
                data_dic[data_dic_count]['mode']     = "CCD"
                data_dic[data_dic_count]['stn']      = self.config["MPC_CODE"]
                data_dic[data_dic_count]['obsTime']  = obsTime
                data_dic[data_dic_count]['ra']       = str( ra_degs )
                data_dic[data_dic_count]['dec']      = str( dec_degs )
                data_dic[data_dic_count]['rmsRA']    = self.obs[i]['pos_unc']
                data_dic[data_dic_count]['rmsDec']   = self.obs[i]['pos_unc']
                data_dic[data_dic_count]['astCat']   = self.header['catalog']
                data_dic[data_dic_count]['mag']      = self.obs[i]['mag']
                data_dic[data_dic_count]['rmsMag']   = self.obs[i]['mag_error']
                data_dic[data_dic_count]['band']   = self.obs[i]['filter']
                

                data_dic_count += 1


            

            

            #note including 'exp' right now because that would involve reading the data again or another scrube of the astrometric.log file to understand which images were stacked



        # generate the header and the first observation.
        XMLElement, ades, obsData = generate_xml(head_dict, data_dic[0] )

        # update the xml
        for i in range( 1, len( data_dic ) ): #start at one because data_dic[0] was used to create the orginal file
            XMLElement, ades, obsData = update_xml(XMLElement, ades, obsData, data_dic[i] )

        # write the ADES xml to file
        tree = XMLElement.ElementTree(ades)
        xml_string = minidom.parseString(XMLElement.tostring(ades)).toprettyxml()
        with open(xml_filename, "w", encoding="UTF-8") as files:
            files.write(xml_string)



        #def find_match_in_log_file( self ):

        #    for i in range(0, len( self.log ) ):

        return xml_filename

    def calculteObsTime( self, i):

            #obsTime format is yyyy-mm-ddThh:mm:ss.sssZ
            date = "%s-%s-%s"%(self.obs[i]['year'], self.obs[i]['month'], self.obs[i]['day'] )

            #convert obs80 time into HMS
            #print ('time', self.obs[i]['time'])
            zero_value = "".zfill( len( self.obs[i]['time'] ) -1 ) #need to divide the obs80 to get a decimal but dependnt on how many digits of time you have
            #print ('zero_value', zero_value)
            zero_value = "1" + zero_value
            #print ('zero_value', zero_value)
            time = float( self.obs[i]['time'] ) / int( zero_value )
            #print ('time', time)

            hours_1 =  time * 24
            hours = int( hours_1 )
            hours_rem = hours_1 - hours
            minutes_1 = hours_rem * 60
            minutes = int( minutes_1)
            minutes_rem = minutes_1 - minutes
            seconds_1 = minutes_rem * 60
            seconds = int( seconds_1 )
            seconds_rem = int( round( seconds_1 - seconds, 2) * 100) #this needs to be a whole number value

            hours = str( hours ).zfill(2)
            minutes = str( minutes ).zfill(2)
            seconds = str( seconds ).zfill(2)

            time = '%s:%s:%s.%s'%(hours, minutes, seconds, seconds_rem)
            #print ('time', time)

            

            obsTime = "%sT%sZ"%(date, time)

            return obsTime
    
    def calculteRa_degs( self, i):
        ra_hour = int( self.obs[i]['ra_hour'] )
        ra_minutes = int( self.obs[i]['ra_minutes'] )
        ra_seconds = float( self.obs[i]['ra_seconds'] )
    
        ra = ra_hour + (ra_minutes/60.) + (ra_seconds/3600.)
        ra_degs = round( (ra * 15.), 6 )

        return ra_degs
    
    def calculteDec_degs( self, i):

        dec_degrees = int( self.obs[i]["dec_degrees"] )
        dec_minutes = int( self.obs[i]["dec_minutes"] )
        dec_seconds = float( self.obs[i]["dec_seconds"] )

        if dec_degrees > 0:
            dec = dec_degrees + (dec_minutes / 60.) + (dec_seconds / 3600.)
        else: #dec is negative
            dec = dec_degrees - (dec_minutes / 60.) - (dec_seconds / 3600.)

        dec_degs = round( dec, 6 )

        return dec_degs
    
    def determinePermidProvidValues( self, name ):
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
                unpacked_provid = f"{first_half_of_year}{second_half_of_year} {first_letter}{second_letter}{second_number}"
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
            permid = unpacked_number
            provid = None

        elif we_have_packed_provid == True:
            permid = None
            provid = unpacked_provid

        if we_have_neocp == True:
            permid = None
            provid = name.replace(" ", "")

        #print ('permid', permid, 'provid', provid)
        #stop

        return permid, provid

            




        
        

if __name__ == "__main__":
    autoOperations()