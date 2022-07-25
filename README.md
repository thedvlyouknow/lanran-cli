# lanran-cli
A command line tool to generate random groups of lancer componants for scavenger style play

# A note on data
This tool pulls core resources from `mastiff-press/lancer-data` and is able to support additional data pulled out of compcon.  I'm not including any of that data in this repo, but if you want additional resources from other LCPs pull the `extra_resources.json` file from compcon to your local storage and pass it in using the `-d` argument.

# Installation
Using python 3.7 or above:
You can install this from ```pip3 install -i https://test.pypi.org/simple/ lancer-randomizer```, as I haven't published it via pypy quite yet. 

# Installation from repo
Eventually this will be installable as a standalone cli plugin, but for now:
1. Make sure python3.7 or above is installed
2. Navigate to repo directory
3. `pip install virtualenv && .venv/bin/activate`
4. `pip install setuptools`
5. `pip install --editable .`
From there you should be able to call the script via `lanran` on your terminal.

# Options
There are two commands, both with their own help options (```---help```)

```lanran randomize``` - This generates random frames, weapons, and systems.  

Notes:
  - Core data is currently imported automatically, but if you want to use additinal data from either official or custom LCP files grab your ```extra_content.json``` file from comp/con and import that to this command using the ```--lcp-data``` or ```-d``` flags.  I've tested this with offical lcp files as well as intercorp's lcp, but additional custom content should be supported by default (although without a snazzy color).
  - You can save your file using the ```-s``` flag! Use this to be able to use the ```lanran details``` suite of commands.
  - Currently 1 of each type of frame (artillery, support, etc) is generated assuming the number of frames requested is high enough.  
  - No integrated weapons/systems will be selected
  - There are options to limit the max LL of random weapons/systems generated, should you choose to use this early.

```lanran details``` - This allows you to examine previous runs if you saved them to file, and generates slightly useful text reports that may prevent your players from going insane from trying to find the details on all the disparate weapons/systems in books/comp-con.

Notes:
  - Currently the format for the details files is bad.  Would love if someone made them more readible.
