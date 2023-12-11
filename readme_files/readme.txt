
Dec 10th, 2023

Began adding PyTest for all of the function. This includes test files of the Astrometrica.log, MPCReport, and MPCPhot files so that the PyTest can use these files

Astrometrica sometimes thinks an NEOCP name is a comet and uses an N as the filter. Therefore, to allow the user to correct this or to auto correct it,
if an N is detected as the fitler value. It is changed or allows the user to change the filter.

November 2023:
The purpose of this code is to provide a user interface that will read Astrometrica's Obs80 information, extract more information about the observations from astrometrica.log file
and then calculate a pos_unc. After all of the data is extracted, give the user a one-click option to submit the observation including the uncertainty information to the minor planet center via ADES.

