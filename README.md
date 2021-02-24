# Wallbox Technical Test

## Usage
This repository includes a python library (wallbox) and a bunch of test for it.
You should have tox installed in the python environment you are currently using. Python sould be >= 3.6 
```shell
cd "root_path_of_this_prohect"
tox
```
It will:
- Create a new virtual environment for the python version you are running. (Multiple envs with different python versions can be configured in the tox file to test the library under multiple python versions)
- Install the library, its dependencies and testing dependencies
- Create the library wheel
- Run the tests and generate a junit and a html report
- Run coverage and generate a report
- Run mypy
- Run pylint

## Code comments
### First repeated number
I assume that arrays are not sorted, and we are looking for the repeated value in both arrays with lower indices.
For example: in [0, 1, 2] & [2, 0, 99] the first repeated value is 0 (indices 0,1) and not 2 (indices 2,0)

### Min quantity of permutations
A permutation is when a value changes from 0 to 1 or otherwise. Swapping two values [0, 1, 1] -> [1, 0, 1] requires two permutations.  