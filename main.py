
from tkinter import *
from tkinter.scrolledtext import ScrolledText
import os
import json
from create_ades import generate_xml, update_xml
from datetime import datetime
import glob
import xml.etree.ElementTree as XMLElement
import xml.dom.minidom as minidom

from src.calculate_JD import calculateJD
from src.calculateRA_degs import calculateRa_degs
from src.calculateDec_degs import calculateDec_degs
from src.calculate_obs_time import calculateObsTime
from src.determine_Permid_Provid_Values import determinePermidProvidValues

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
        config_files_menu.grid( row = 1, column = 0, columnspan=10, sticky=W )

        self.xml_files = glob.glob( cwd + "\\prep_xml*.xml")
        for i in self.xml_files: #errors occur when there is already a prep_xml file that is loaded on start-UP. to fix this, going to delete all prep_xml files on startup
            os.remove(i)
        self.xml_files = []    
        self.xml_val = StringVar()
        if len(self.xml_files) == 0:
            self.xml_files = ['None']
            self.xml_val.set( self.xml_files[0] )
        else:
            self.xml_val.set( self.xml_files[ len( self.xml_files ) - 1 ] )

        self.xml_files_menu = OptionMenu(self.mp, self.xml_val, *self.xml_files)
        self.xml_files_menu.grid( row = 50, column = 2, columnspan=10, sticky=W )

        obs_types =['NEO', 'NEOCP', 'Unclassified', 'Comet', 'TNO', 'New NEO Candidate', 'New Comet', 'ARTSAT' ]
        self.obs_types_val = StringVar()
        self.obs_types_val.set( obs_types[0] )
        obs_types_menu = OptionMenu(self.mp, self.obs_types_val, *obs_types )
        obs_types_menu.grid( row = 49, column = 14, columnspan=4, sticky=W )

        #load the selected_config_file
        with open( config_files[0] ) as infile:
            self.config = json.load(infile)

        Label( self.mp, text='Submiter').grid(row=2, column=0, sticky=W)
        self.submiter_for_ades = Label( self.mp, text=self.config["NAME_FOR_THE_ADES_SUBMITTER_FIELD"] )
        self.submiter_for_ades.grid( row=2, column = 2, columnspan=4, sticky = W)

        Label( self.mp, text='Observatory').grid(row=2, column=8, sticky=E)
        self.observatory_for_ades = Label( self.mp, text=self.config["OBSERVATORY_NAME_FOR_ADES"] )
        self.observatory_for_ades.grid( row=2, column = 10, columnspan=4, sticky = W)

        Label( self.mp, text='Observers').grid(row=3, column=0, sticky=W)
        self.observers_for_ades = Label( self.mp, text=self.config["OBSERVERS_FOR_ADES"] )
        self.observers_for_ades.grid( row=3, column = 2, columnspan=4, sticky = W)

        Label( self.mp, text='Tel Design   ').grid(row=3, column=8, sticky=E)
        self.tel_design_for_ades = Label( self.mp, text=self.config["TELESCOPE_DESIGN_FOR_ADES"] )
        self.tel_design_for_ades.grid( row=3, column = 10, columnspan=4, sticky = W)

        Label( self.mp, text='Measures').grid(row=4, column=0, sticky=W)
        self.measures_for_ades = Label( self.mp, text=self.config["MEASURERS_FOR_ADES"] )
        self.measures_for_ades.grid( row=4, column = 2, columnspan=4, sticky = W)

        Label( self.mp, text='Tel Aperture').grid(row=4, column=8, sticky=E)
        self.tel_aperture_for_ades = Label( self.mp, text=self.config["TELESCOPE_APERTURE_FOR_ADES"] )
        self.tel_aperture_for_ades.grid( row=4, column = 10, columnspan=4, sticky = W)

        Label( self.mp, text='Funding Agency').grid(row=5, column=0, sticky=W)
        self.funding_agency_for_ades = Label( self.mp, text=self.config["FUNDING_AGENCY_FOR_ADES"] )
        self.funding_agency_for_ades.grid( row=5, column = 2, sticky = W)

        Label( self.mp, text='Tel Detector').grid(row=5, column=8, sticky=E)
        self.tel_detector_for_ades = Label( self.mp, text=self.config["TELESCOPE_DETECTOR_FOR_ADES"] )
        self.tel_detector_for_ades.grid( row=5, column = 10, columnspan=4, sticky = W)

        

        
        Button( self.mp, text='Reload Obs80', command=self.reloadObs80Button ).grid(row=9, column=18, columnspan=2, sticky=W+E)
        Label( self.mp, text='Use').grid(row=10, column=0)
        Label( self.mp, text='Permid').grid(row=10, column=2, sticky=W)
        Label( self.mp, text='Provid').grid(row=10, column=4, sticky=W)
        Label( self.mp, text='NEOCP(trkSub)').grid(row=10, column=6, sticky=W)
        Label( self.mp, text='Mag').grid(row=10, column=8, sticky=W)
        Label( self.mp, text='FWHM').grid(row=10, column=10, sticky=W)
        Label( self.mp, text='Obs80').grid(row=10, column=12, sticky=W+E)
        Label( self.mp, text='FWHM', width=10).grid(row=10, column=14, sticky=W+E)
        Label( self.mp, text='SNR', width=10).grid(row=10, column=16, sticky=W+E)
        Label( self.mp, text='POS_UNC', width=10).grid(row=10, column=18, sticky=W+E)
        self.submit_button = Button( self.mp, text='Submit Obs', command=self.submit_obs, bg='Grey' )
        self.submit_button.grid(row=50, column=18, columnspan=2, sticky=W+E)
        Button( self.mp, text='Build ADES', command=self.build_ades ).grid(row=50, column=14, columnspan=2, sticky=W)
        Button( self.mp, text='Delete ADES File', command=self.delete_ades_file ).grid(row=50, column=0, columnspan=2, sticky=W+E)

        
        self.dic = {}
        self.currentNumberOfObs = 0

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

        for count in self.dic:
            #print (count)
            if count in self.obs:
                if self.dic[count]['entry_fwhm'].get() != self.obs[count]['fwhm']: #if the user changes the fwhm value then update the pos_unc

                    usesnr = float( self.obs[count]['phot_snr'] ) #default use the value from the photometry file
                    #if float( self.obs[count]['snr'] ) > float( self.obs[count]['phot_snr'] ): #use the large snr value, if the log file is larger
                    #    usesnr = float( self.obs[count]['snr'] )

                    try: #when typing something could change and error out with the math
                        self.obs[count]['pos_unc']  = round( ( float( self.dic[count]['entry_fwhm'].get() ) / usesnr ) , 2)
                    except:
                        pass
                    self.dic[count]['label_pos_unc'].config(text='%s'%(self.obs[count]['pos_unc'] ) )

                if self.dic[count]['entry_mag'].get() != self.obs[count]['mag']:
                    self.obs[count]['mag'] = self.dic[count]['entry_mag'].get()
            #else:
                #print ('len(self.obs)', len(self.obs) )
            #    for key in self.obs:
                    #print ('key', key)

                




        
        refreshRate = 500
        self.measures_for_ades.after(refreshRate, self.checkIfConfigFileWasUpdated)

    def reloadObs80Button(self):

        self.readObs80()

        #print (len( self.obs ) )

        self.checkBoxList = []
        
        listOfHeaderValues = ["COD", "CON", "OBS", "MEA", "TEL", "ACK", "AC2", "NET", "---"]
        end = 20
        for i in range( 0, end):
            if i in self.dic:
                #print ('destroy', i)
                self.dic[i]['button'].destroy()
                self.dic[i]['entry_permid'].destroy()
                self.dic[i]['entry_provid'].destroy()
                self.dic[i]['entry_trksub'].destroy()
                self.dic[i]['entry_mag'].destroy()
                self.dic[i]['entry_fwhm'].destroy()
                self.dic[i]['label_obs80'].destroy()
                self.dic[i]['label_fwhm'].destroy()
                self.dic[i]['label_snr'].destroy()
                self.dic[i]['label_pos_unc'].destroy()
        #if len( self.obs ) > 20:
        #    end = 20
        #else:
        #    end = len( self.obs )
        #print ('self.currentNumberOfObs', self.currentNumberOfObs)
        #print ('self.obs', self.obs)
        #for key in self.obs:
        #    print ('self.obs[key]', key, type(key) )
            #if i in self.obs
        for i in range( 0, end ):
            useObs = True
            #print (self.obs80[i][0:3])

            
            
            if i < self.currentNumberOfObs : #is i variable greater than the number of obs, this means we need to send destroy commands
                #print ('i', i)
                for j in listOfHeaderValues:
                    
                    if self.obs[i]['obs80'][0:3] == j:
                        useObs = False
                
                if useObs == True:
                    self.dic[i] = {}
                    self.dic[i]['variable'] = IntVar()
                    #self.dic[i]['button'] = Checkbutton( self.mp, text=self.obs80[i], variable = self.dic[i]['variable'], onvalue=1, offvalue=0, height=2, width=100)
                    self.dic[i]['button'] = Checkbutton( self.mp, variable = self.dic[i]['variable'], onvalue=1, offvalue=0, height=2, width=5)
                    row_value = 20 + i
                    self.dic[i]['button'].grid(row=row_value, column=0, columnspan=2, sticky=W+E)
                    self.dic[i]['variable'].set(1)

                    permid, provid, trksub = determinePermidProvidValues( self.obs[i]['name'] )
                    #print (permid, provid)

                    self.dic[i]['entry_permid'] = Entry(  width=15 )
                    self.dic[i]['entry_permid'].grid( row=row_value, column=2, sticky=W+E)
                    if permid != None:
                        self.dic[i]['entry_permid'].delete(0, 'end' )
                        self.dic[i]['entry_permid'].insert(0, permid)
                    

                    self.dic[i]['entry_provid'] = Entry( width=15 )
                    self.dic[i]['entry_provid'].grid( row=row_value, column=4, sticky=W+E)
                    if provid != None:
                        self.dic[i]['entry_provid'].delete(0, 'end' )
                        self.dic[i]['entry_provid'].insert(0, provid)

                    self.dic[i]['entry_trksub'] = Entry( width=15 )
                    self.dic[i]['entry_trksub'].grid( row=row_value, column=6, sticky=W+E)
                    if trksub != None:
                        self.dic[i]['entry_trksub'].delete(0, 'end' )
                        self.dic[i]['entry_trksub'].insert(0, trksub)

                    

                    self.dic[i]['entry_mag'] = Entry( width=8 )
                    self.dic[i]['entry_mag'].grid( row=row_value, column=8, sticky=W+E)
                    self.dic[i]['entry_mag'].delete(0, 'end' )
                    #print ("self.obs[i]['mag']", self.obs[i]['mag'])
                    self.dic[i]['entry_mag'].insert(0, self.obs[i]['mag'])

                    self.dic[i]['entry_fwhm'] = Entry( width=15 )
                    self.dic[i]['entry_fwhm'].grid( row=row_value, column=10, sticky=W+E)
                    #print ('self.currentNumberOfObs', self.currentNumberOfObs, 'len(self.obs)', len(self.obs))
                    #print ('self.obs[i]', self.obs[i])
                    #if i in self.obs: #I don't know yet why this error is occuring
                        #print (self.obs[i] )
                    #print ('self.obs[i]', self.obs[i])
                    self.dic[i]['entry_fwhm'].insert(0, self.obs[i]['fwhm'] )

                    

                    

                    self.dic[i]['label_obs80'] = Label( self.mp, text=self.obs[i]['obs80'] )
                    self.dic[i]['label_obs80'].grid(row=row_value, column=12, sticky=W)

                    if 'fwhm' in self.obs[i]: #if 'fwhm key does not exist there was a fail
                        self.dic[i]['label_fwhm'] = Label( self.mp, text=self.obs[i]['fwhm'] )
                        self.dic[i]['label_snr'] = Label( self.mp, text=self.obs[i]['usesnr'] )
                        self.dic[i]['label_pos_unc'] = Label( self.mp, text=self.obs[i]['pos_unc'] )
                    else:
                        self.dic[i]['label_fwhm'] = Label( self.mp, text='n/a', bg='red' )
                        self.dic[i]['label_snr'] = Label( self.mp, text='n/a', bg='red' )
                        self.dic[i]['label_pos_unc'] = Label( self.mp, text='n/a', bg='red' )
                        self.dic[i]['variable'].set(0)
                        

                    self.dic[i]['label_fwhm'].grid(row=row_value, column=14, sticky=W+E)
                    self.dic[i]['label_snr'].grid(row=row_value, column=16, sticky=W+E)
                    self.dic[i]['label_pos_unc'].grid(row=row_value, column=18, sticky=W+E)

            #else:
                #try:
            #    print (i)
                
                #except:
                #else:
                #    print ('no destory', i)
                    #pass

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
                #print ('self.value', self.value )
                #print ('self.obs', self.obs )
                self.obs[count] = {}
                #from MPCReport.txt File
                #print( self.obs80[i][:-1] )
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
                #print ('time', "0." + self.obs80[i][ (date_start + 11) : (date_start + 17) ].replace(" ", "") ) #get rid of the extra spaces
                self.obs[count]['time'] = "0." + self.obs80[i][ (date_start + 11) : (date_start + 17) ].replace(" ", "") #get rid of the extra spaces
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
                elif catalog == 'Gaia DR3':
                    catalog = "Gaia3" #mpc has changed their requirement
                elif catalog == 'Gaia DR2':
                    catalog = "Gaia2" #mpc has changed their requirement
                elif catalog == 'Gaia DR1':
                    catalog = "Gaia1" #mpc has changed their requirement
                self.header['catalog'] = catalog

                #match information from the photometry File:

                jd = calculateJD( self.obs[count] )
                #print (jd)
                snr_column_number = None
                mag_column_number = None
                for j in range( 0, len( self.phot ) ):
                    if self.phot[j][0] != 'O' and self.phot[j][0] != 'O' and self.phot[j][0] != 'C' and self.phot[j][0] != 'T' and self.phot[j][0] != 'E' and self.phot[j][0] != '-' :

                        #need to determine which order the columns are in.
                        if self.phot[j][0] == ' ': #this is the header line
                            header_line = self.phot[j].split(' ')
                            #print ('header_line', header_line)
                            for mm in range(0, 50):
                                try:
                                    header_line.remove('')
                                except ValueError:
                                    break
                            #print ('header_line', header_line)

                            for mm in range(0, len( header_line ) ):
                                if header_line[mm] == 'SNR':
                                    snr_column_number = mm
                                if header_line[mm] == 'mag':
                                    mag_column_number = mm

                        #print (snr_column_number)
                        #stop
                        
                        if self.phot[j][0] != ' ':
                            #print (self.phot[j][0])
                            #print (self.phot[j])
                            #if self
                            phot_line = self.phot[j].split(' ')
                            #print ('1',phot_line)
                            for mm in range(0, 20):
                                try:
                                    phot_line.remove('') #remove the spaces
                                except ValueError:
                                    break

                            #print ('2',phot_line)
                            #stop
                            #for ll in phot_line:
                            #    if ll == ' ':
                            #        phot_line
                            #length_of_jd = len( jd )
                            
                            #print (type(jd), type(phot_line[0]), float(jd) == float(phot_line[0]) )
                            if float( jd) == float( phot_line[0] ):
                                #print ('jd', jd, phot_line, len(phot_line))
                                if len(phot_line) == 9: #this mean it seperated Gaia and DR2
                                    phot_line[6] = '%s %s'%(phot_line[6], phot_line[7])
                                    phot_line[7] = phot_line[8]
                                    del phot_line[8]
                                #print ('jd', jd, phot_line, len(phot_line))

                                #print ('snr', self.phot[j][30:35])
                                #print ('snr', self.phot[j][29:34])
                                #print ('snr', self.phot[j][28:34])
                                self.obs[count]['phot_snr'] = phot_line[snr_column_number + 1] #there is a V value in there.
                                #self.obs[count]['mag'] = phot_line[mag_column_number ]
                                #self.obs[count]['phot_snr'] = phot_line[5]
                                #self.obs[count]['phot_snr'] = self.phot[j][30:35]
                                #self.obs[count]['phot_snr'] = self.phot[j][26:31]
                            #stop




                #match information from log.log File
                for k in range( 0, len( self.log ) ):
                #print (self.obs[count]['obs80'] )
                #for k in range( 14155, len( self.log ) ): #for testing
                    #print ('count', count, 'k', k)
                    obsMatch = False
                    obsMatch_ra = False
                    obsMatch_dec = False

                    #print('')
                    if self.obs80[i][13] == 'K':
                        #print ('k')
                        obs80_no_k = self.obs80[i][0:13] + " " + self.obs80[i][14:-1]
                        #print ('self.obs80[i][0:13]', self.obs80[i][0:13] )
                        #print ('self.obs80[i][14:-1]', self.obs80[i][14:-1] )
                        #print ('obs80_no_k', obs80_no_k)
                    else:
                        obs80_no_k = self.obs80[i][0:-1]
                    #print ('self.obs80[i]', self.obs80[i][:-1])
                    #print (k, 'self.log[k]', self.log[k][:-1])
                    if obs80_no_k == self.log[k][:-1]:
                        #print ('True')
                        #print( obs80_no_k )
                        #print( self.log[k-2][:-1] )
                        #print( self.log[k-1][:-1] )




                        obs_line = self.log[k-2].split(' ')
                        for mm in range(0, 50):
                            try:
                                obs_line.remove('') #remove the spaces
                            except ValueError:
                                break

                        

                        self.obs[count]['ra_error_arc_minutes']     = self.log[k-1][18:22]
                        self.obs[count]['dec_error_arc_minutes']    = self.log[k-1][41:45]
                        #self.obs[count]['mag']                      = self.log[k-2][48:53]
                        self.obs[count]['mag_error']                = self.log[k-1][57:61]
                        #self.obs[count]['x_pixel']                  = self.log[k-2][64:71]
                        #self.obs[count]['y_pixel']                  = self.log[k-2][73:80]
                        #self.obs[count]['flux']                     = self.log[k-2][81:88]
                        #print ( 'fwhm', self.log[k-2][90:94] )
                        #print ( 'fwhm', self.log[k-2][80:100] )
                        if float( self.log[k-2][90:94] ) == 0.0: #if fwhm is reported to be zero, then assume a 5 for fwhm
                            self.obs[count]['fwhm']                 = float( self.config["IF_NO_FWHM_IS_CALCULTED_USE_VALUE"] )
                        else: 
                            #self.obs[count]['fwhm']                 = self.log[k-2][90:94]
                            self.obs[count]['fwhm']                  = obs_line[ len(obs_line) - 3 ]

                        #print ('testing', self.obs[count]['fwhm'] )
                        
                        #print ( 'self.log[k][90:94]', self.log[k][90:94])
                        #print ( 'self.log[k][85:100]', self.log[k][85:100])
                        #print ('count', count, 'fwhm', self.obs[count]['fwhm'])
                        #self.obs[count]['snr']                      = self.log[k-2][95:102] #not used because of issues with spacing
                        #self.obs[count]['fit_rms']                  = self.log[k-2][103:108]

                        #self.obs[count]['x_pixel']                  = obs_line[ len(obs_line) - 6 ]
                        #self.obs[count]['y_pixel']                  = obs_line[ len(obs_line) - 5 ]
                        #self.obs[count]['flux']                     = obs_line[ len(obs_line) - 4 ]
                        self.obs[count]['snr']                      = obs_line[ len(obs_line) - 2 ]
                        self.obs[count]['fit_rms']                  = obs_line[ len(obs_line) - 1 ]




                        #print ('snr', self.log[k-2][95:102])
                        #print ('snr', self.log[k-2][90:105])
                        
                        usesnr = float( self.obs[count]['phot_snr'] ) #default use the value from the photometry file
                        #if float( self.obs[count]['snr'] ) > float( self.obs[count]['phot_snr'] ): #use the large snr value, if the log file is larger
                        #    usesnr = float( self.obs[count]['snr'] )

                        self.obs[count]['usesnr']                  = usesnr
                        self.obs[count]['pos_unc']                  = round( ( float( self.obs[count]['fwhm'] ) / usesnr ) , 2)
                        break #this will break the k loop
                        #stop
                    
                                


                

                #for key in self.obs[count]:
                #    print (key, self.obs[count][key])

                #stop
                count += 1

        self.currentNumberOfObs = count
        #print ('len(self.obs)', len(self.obs) )
        #print ('self.currentNumberOfObs', self.currentNumberOfObs)

        with open("astrometrica_data.json", "w") as outfile:
            json.dump(self.obs, outfile)

        with open("astrometrica_header.json", "w") as outfile:
            json.dump(self.obs, outfile)

        self.submit_button.config(bg='Grey')

    def update_xml_file_list(self):

        cwd = os.getcwd()
        
        current_prep_list = glob.glob( cwd + "\\prep_xml*.xml")
        #delete the whole xml_files list
        self.xml_files.clear()

        for j in range( 0, len( current_prep_list ) ):

            self.xml_files.append( current_prep_list[j] )

        #self.xml_files_menu.delete(0, "end")
        #for i in self.xml_files:
        if len(self.xml_files) > 0:
            self.xml_val.set( self.xml_files[ len(self.xml_files) -1 ] )
        else:
            self.xml_files.append('None')
            self.xml_val.set( self.xml_files[ len(self.xml_files) -1 ] )

        #self.xml_files_menu.config( self.xml_val, self.xml_files )
        self.xml_files_menu.destroy()
        self.xml_files_menu = OptionMenu(self.mp, self.xml_val, *self.xml_files)
        self.xml_files_menu.grid( row = 50, column = 2, columnspan=10, sticky=W )

        self.xml_val.set( self.xml_files[ len( self.xml_files )-1 ] )

    def delete_ades_file(self):

        current_file = self.xml_val.get()
        newFile = current_file.replace('prep', 'deleted')
        os.rename( current_file, newFile)

        self.update_xml_file_list()

    def build_ades(self):

        self.xml_filename = self.build_xml()

        
        self.update_xml_file_list()

        self.submit_button.config(bg='Grey')
        

        #self.xml_val.

    def submit_obs( self ):

        xml_filename = self.build_xml()
        self.update_xml_file_list()

        #xml_filename = self.xml_val.get()

        obs_type = self.obs_types_val.get()



        ack_line="ack=permid_%s_provid_%s_trkSub_%s"%(self.permid, self.provid, self.trkSub)
        #email_line = "ack=tlinder34@gmail.com,lehorn93@gmail.com,star@astro-research.org"
        email_line = "ac2=%s"%(self.config["LIST_OF_EMAILS_FOR_AC2_LINE"])
        obs_type_field = "obj_type=%s"%(obs_type)

        #print ('ack_line', ack_line)
        #print ('email_line', email_line)
        

        #command = 'curl https://minorplanetcenter.net/submit_xml -F "ack=curl_test" -F "ac2=tlinder34@gmail.com" -F "source=<%s" '%(fileName)
        
        #testing
        command = 'curl https://minorplanetcenter.net/submit_xml_test -F "%s" -F "%s" -F "%s" -F "source=<%s" '%(obs_type_field, ack_line, email_line, xml_filename)

        #real submission
        #command = 'curl https://minorplanetcenter.net/submit_xml -F "%s" -F "%s" -F "%s" -F "source=<%s" '%(obs_type_field, ack_line, email_line, xml_filename)

        print ('len(command)', len(command))
        print (command)
        print ('len(command)', len(command))

        res = os.system( command )

        print ('res', res)
        #print ('len(res)', len(res))

        if res == 0:
            print ('MPC Accepted Submission')
            self.submit_button.config(bg='Green')
            current_file = self.xml_val.get()
            newFile = current_file.replace('prep', 'submitted')
            os.rename( current_file, newFile)

            #remove all current prep_xml_files
            cwd = os.getcwd()
            current_prep_list = glob.glob( cwd + "\\prep_xml*.xml")
            for i in current_prep_list:
                os.remove(i)

            self.update_xml_file_list()
        else:
            print ('MPC Rejected the Submission with curl error of: %s'%(res))
            self.submit_button.config(bg='Red')

    def build_xml( self ):

        current_date_time = datetime.utcnow()
        xml_filename = f"prep_xml_output_{ current_date_time.strftime( '%Y' ) }_{ current_date_time.strftime( '%m' ) }_{ current_date_time.strftime( '%d' ) }_{ current_date_time.strftime( '%H' ) }_{ current_date_time.strftime( '%M' ) }_{ current_date_time.strftime( '%S' ) }.xml"

        #xml_filename = "Catalog.xml"

 

        #build ades_header dictionary
        head_dict = {}
        head_dict["mpcCode"]            = self.config["MPC_CODE"]
        if self.config["FUNDING_AGENCY_FOR_ADES"] != "None":
            head_dict["fundingSource"]  = self.config["FUNDING_AGENCY_FOR_ADES"]

        head_dict["observatoryName"]    = self.config["OBSERVATORY_NAME_FOR_ADES"]
        head_dict["submitter"]          = self.config["NAME_FOR_THE_ADES_SUBMITTER_FIELD"]
        head_dict["observers"]          = self.config["OBSERVERS_FOR_ADES"]
        head_dict["measurers"]          = self.config["MEASURERS_FOR_ADES"]
        head_dict["telescope_design"]   = self.config["TELESCOPE_DESIGN_FOR_ADES"]
        head_dict["telescope_aperture"] = self.config["TELESCOPE_APERTURE_FOR_ADES"]
        head_dict["telescope_detector"] = self.config["TELESCOPE_DETECTOR_FOR_ADES"]
        head_dict["fRatio"]             = self.config["TELESCOPE_FOCAL_RATIO_FOR_ADES"]
        

        #build ades_data dictionary
        data_dic = {}
        data_dic_count = 0
        for i in range( 0, len( self.obs ) ):

            if self.dic[i]['variable'].get() == 1:

                obsTime = calculateObsTime( self.obs[i] )
                
                ra_degs = calculateRa_degs( self.obs[i] )
                
                dec_degs = calculateDec_degs( self.obs[i] )
                

                #print ('obsTime', obsTime)

                #stop
                #calculte ra_degs and dec_degs 

                data_dic[data_dic_count] = {}
                
                permid = self.dic[i]['entry_permid'].get()
                #print ('permid', permid)
                if len( permid ) != 0:
                    data_dic[data_dic_count]['permID']   = permid
                    self.permid = permid
                else:
                    self.permid = None

                provid = self.dic[i]['entry_provid'].get()
                #print ('provid', provid)
                if len( provid ) != 0:
                    data_dic[data_dic_count]['provID']   = provid
                    self.provid = provid
                else:
                    self.provid = None

                trkSub = self.dic[i]['entry_trksub'].get()
                #print ('trkSub', trkSub)
                if len( trkSub ) != 0:
                    data_dic[data_dic_count]['trkSub']   = trkSub
                    self.trkSub = trkSub
                else:
                    self.trkSub = None

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


    



    

    





        
        

if __name__ == "__main__":
    autoOperations()