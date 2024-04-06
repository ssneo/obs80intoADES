

1) To run all tests in a folder
pytest folderName/
Example
pytest tests/

2) To run all tests in a single file
pytest nameOfFile.py
Example
pytest test_basic_timer.py

3) To run a specific function in a speicifc file
pytest -k nameOfFunction NnmeOfFile.py
Example
pytest -k test_basic_timer_1 test_basic_timer.py

4) To print the output of print statements from the pytest add a -s to the end of the command
pytest -k nameOfFucntion nameOfFile.py -s