# Website monitor

Website monitor written in Python 3. The script first checks for status errors (e.g 500 Internal server error) after that it checks for changes in website itself. I only check the body because I want to check some websites that change the header every request. The script downloads the websites and write a hash from the body in a file. Next time the script runs it compares the current hash with the previous one. If there is a status error or the hashes don't match it sends an e-mail message.


## Prerequisites

Python >= 3.4 must be installed.

tzlocal Must be [installed](https://pypi.org/project/tzlocal/).
On most Linux systems you can install tzlocal with your package manager.

BeautifulSoup must be [installed](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup).


## Installing

*         git clone https://github.com/githubbauman/website-monitor.git
   or download and extract the zip file.
* The created directory must be writable by the script.
* Edit "config.py.example".
* Rename "config.py.example" to "config<span>.</span>py".
* "config<span>.</span>py" Should only readable by the script! 
   Linux example:
         chmod 700 config<span>.</span>py


## Running

Call:

```
python3 website-monitor.py
```
or:
```
./website-monitor
```

Preferable called by Cron or Windows Task Scheduler.

Cron example:
```
0,15,30,45 * * * * /home/johndoe/bin/website-monitor/website-monitor.py >> /home/johndoe/bin/website-monitor/website-monitor.log 2>&1
```

## Built With

* [Visual Studio Code](https://code.visualstudio.com/) - Code Editing Redefined.
* [Pylint](https://www.pylint.org/) - Code analysis for Python.
* [Pycodestyle](https://github.com/PyCQA/pycodestyle) - Python style guide checker.


## Authors

**Arthur Bauman** - https://bauman.nu


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


## Acknowledgments

My second Python script.