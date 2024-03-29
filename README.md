# current-meter-beta-tools
Python 3 tools for accessing and analyzing data from Beta Current Meter Smart Mooring Systems

## Installation
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

You should now be able to run any of the scripts while in `cmbeta`

### Without virtualenv
 `pip install -r requirements.txt`  
 to install required python dependencies in your base installation. _Not recommended._


# Main Programs
### bin_decode_tester.py
This is a simple script to demonstrate decoding raw binary payloads from DVT 1 Current Meter modules. 

### beta1_api_tester.py
This script demonstrates for DVT1 systems: retrieving data from the API, decoding the binary payloads, and plotting the data in `matplotlib`.

### beta2_api_tester.py
This script demonstrates for Beta 2 systems: retrieving data from the API and plotting the data in `matplotlib`.
- Example usage: ```python beta2_api_tester.py <YOUR_SPOTTER_ID> <YOUR_API_TOKEN> -s 2024-01-30T16:00Z -e 2024-01-30T21:00Z```
- For a description of Command Line arguments: ```python beta2_api_tester.py --help```

### rbr_coda_bin_decode_tester.py
Decode raw binary payloads from Feb '24 DVT RBR Coda temperature and pressure modules.

### soft_api_tester.py
Retrieves Feb '24 DVT SOFT module temperature data and plots it in `matplotlib`.

### TODOs
- [ ] Add support for SD card parsing and plotting?
- [ ] Add paging to api_functions for improved performance for long time spans?
- [ ] Add saving and loading of generated data, plots, and API response data to files?