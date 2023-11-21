
Updated
November 21st, 2023


Please refer to the software.png file which list values #1-#8 on the software.


#1: Select the config file to be used. Config files in the obs80intoADES folder, any file that starts with config_  the software will detect them on startup. 

#2: Check buttons. If you detect that observations will not be added to the ADES file

#3: If you build an ADES file, this allows you to delete it. Currently, it does not really do anything because when you press submit_obs it will build a new ADES file, submit the obs. Remove all files labeled prep_xml and change the name of the submitted ades file to submitted_xml

#4: If you build an ADES file, this will give you the file name so you can look at what was created.

#5: The MPC's curl submission allows the user to select what type of observations is being selected. The possible options are provided in the drop down menu

#6: Build ADES button allows you to build and inspect the ADES file. However, when you hit the submit_obs button, a new ADES file will be built and submitted. Therefore, any manually changes in an ADES file won't be submitted to the MPC.

#7 Submit Obs: This button will take the config file, the checked observations and build an ADES xml file and then submit that to the MPC via a curl command.

#8 Reload-obs: Press this button to update the software to make current observations in Astrometrica.

The permid, provid, NEOCP(trkSub), mag, and FWHM files allow the user to update values. The values in these box will override anything from the astrometrica files when submiting the ADES XML to the MPC.