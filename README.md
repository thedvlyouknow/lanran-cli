# lanran-cli
A command line tool to generate random groups of lancer componants for scavenger style play

# A note on data
This tool pulls core resources from `mastiff-press/lancer-data` and is able to support additional data pulled out of compcon.  I'm not including any of that data in this repo, but if you want additional resources from other LCPs pull the json from compcon to your local machine and pass it in.

# Installation
Eventually this will be installable as a standalone cli plugin, but for now:
1. Make sure python3.7 or above is installed
2. Navigate to repo directory
3. `pip install virtualenv && .venv/bin/activate`
4. `pip install setuptools`
5. `pip install --editable .`
From there you should be able to call the script via `lanran` on your terminal.

# Options
Eventually this is actually going to make sense as a console tool, but seeing as how I'm still learning Click we're not there yet.  As such, here's the current flags you can pass into the program.

//TODO add option detailss