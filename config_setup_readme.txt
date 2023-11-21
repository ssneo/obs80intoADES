Updated Nov 21st, 2023

1) All values should be enclosed in double-quotes. 
2) The last value in the config file will not have a comma at the end. This will make the file JSON compliant.

The software will read all files that start with a filename of "config_" therefore, you can setup config files for different telescopes and then you 
can select any of the config file in the OBS80-ADES software

"MPC_CODE": "807",  #mpc_observatory_code

"NAME_FOR_THE_ADES_SUBMITTER_FIELD": "F. Lastname",  This should be the CON line from the normal Obs80 header. This is critical as it is tied to the program code for the MPC_code in line one. If you change this name a new program code will be issued by the MPC

"OBSERVERS_FOR_ADES" : "F. Lastname1, F. Lastname2",

"MEASURERS_FOR_ADES" : "F. Lastname1, F. Lastname2",

"LIST_OF_EMAILS_FOR_AC2_LINE": "email@email.org, email1@gmail.com, star@astro-research.org", #list all emails that should receive the acknowledgment emails when ADES is submitted

"IF_NO_FWHM_IS_CALCULTED_USE_VALUE": "5.0", #Sometimes Astrometrica does not calculate a FWHM value for faint measures. This will be the default value displayed in the software.

"FUNDING_AGENCY_FOR_ADES": "NASA", #funding agency, this can be left blank

"OBSERVATORY_NAME_FOR_ADES": "Cerro Tololo Inter-American Observatory", #name of the observatory

"TELESCOPE_DESIGN_FOR_ADES": "Ritchey-Chretien", #telescope design, that are requirements in the ADES documentation

"TELESCOPE_APERTURE_FOR_ADES": "0.61", #telescope aperture. Do not include the m for meters in this number

"TELESCOPE_FOCAL_RATIO_FOR_ADES" : "11", #telescope focal length, do not include the f/11 only the number

"TELESCOPE_DETECTOR_FOR_ADES": "CCD", #detector for the measures. ADES-documentation list the possible options.

"LOCATION_OF_ASTROMETRICA_LOG_FILES" : "C:\\Astrometrica\\!EIU Astrometrica (outputfile)", #go to Astrometrica Config file, Under Environment Tab, this should match the Outfile line. This will allow the software to read the Astrometrica files

"LOCATION_TO_SAVE_XML_FILES": "C:\\Astrometrica\\obs80intoADES" #where you want the xml files saved. Right now everything is saved into the main folder.
