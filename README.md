# current-meter-beta-tools
Python 3 tools for accessing and analyzing data from Beta Current Meter Smart Mooring Systems

You can either use a virtualenv, or install the requirements in your base python installation.

Python's virtualenv tool allows you to make separate environments in which you can run programs.
By making a virtualenv specifically for running these tools, you avoid changing your base python
distribution and potentially breaking other other codes you run.

> Note: depending on your system, you many need to use `pip3` and `python3` instead of `pip` and `python` to access Python 3

### With virtualenv
To install or update the virtual environment:
```
pip install virtualenv

python -m venv cmbeta

source cmbeta/bin/activate
pip install -r requirements.txt
```

To activate the virtual environment (from the repository root):
```
$ source cmbeta/bin/activate
```

To deactivate the virtual environment:
```
(cmbeta)$ deactivate
```

You should now be able to run any of the scripts while in <name_of_env>

### Without virtualenv
 `pip install -r requirements.txt` to install required python dependencies in your base installation.  
 _Not recommended._


# Main Programs
### smart_mooring_api_tool.py
This program pulls data from the Smart Mooring API and offer a number of plotting/analysis option through a simple terminal UI.
No command line args needed, prompt will gather unit info via terminal.

Optional command line arg (-r) to skip prompts and load unit info from a text file (see smart_mooring_info_example.txt)

### sd_data_plotter.py
This program is for plotting Smart Mooring SD data. It has a UI similar to smart_mooring_api_tool.py and is ready to go.
This program filters out data without GPS time.

### bucket_of_water_test.py
SD data plotting program ONLY for V1 eboxes flashed with BCMD_SDLOG_AVR. Mostly for pressure vessel testing and 10 minute test.
Same functionalities as sd_sm_data_plotte.py and pluteus_sd_data_plotter.py
(It was faster to make these all separate programs and make small changes than to make one program that could do the job of all three.)

## Other Programs
### motecfg_calculator.py
A quick command line interface for calculating motecfg hex strings from settings, or
settings from motecfg hex string. 

##Supporting programs
### Handlers:
Each of the main programs has a companion 'handler' program. These handlers usually do the data read-in and give the main programs a formatted pandas dataframe.




# TODOs
