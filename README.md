# STRAPY :warning: *Wildly unstable* :construction:

For cycling geek and self privacy lovers. This project is less usefull than the original -by far- but it should be useful to monitor the gpx tracks and stats of a few cyclists (there is no authentification). 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system. --In construction--

### Prerequisites

Strapy is based on the following libraries : 

Python :

```

gpxpy : https://github.com/tkrajina/gpxpy
mplleaflet : https://github.com/jwass/mplleaflet
pandas : https://github.com/pandas-dev/pandas
matplotlib : https://github.com/matplotlib/matplotlib
pygal (for now) : https://github.com/Kozea/pygal

```

Html/CSS :

```
skeleton : https://github.com/dhg/Skeleton

```

### Installing

Install the prerequisites. (pip install for all ...). You don't need Skeleton, a version is included in the repo.  

Download this repo : 

```
git clone https://github.com/ThmsP/strapy.git
```


## Running the code

Use some of your gps or get them from Strava. 

### Bulk export from Strava

    Log in to Strava
    Select "Settings" from the main drop-down menu at top right of the screen
    Select "Download all your activities" from lower right of screen
    Wait for an email to be sent
    Click the link in email to download zipped folder containing activities
    Unzip files

Please put your files in this arborescence, where name is hard coded in parser.py (to be improved).

```
Data/GPX_name
```

### Running

```
python wbs.py test
```

test is mandatory but will evolve. And then go to :

```
http://localhost:8080/1
```

A page is generated for each users defined in parser.py (to be improved).

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* https://ocefpaf.github.io/python4oceanographers/blog/2014/08/18/gpx/
* http://pikebishop.github.io/pages/Notes/GpxVisualization/GpxVisualization

