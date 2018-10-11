:: A simple batch file to facilitate the identifying the potential lifers in a defined hotspot
:: The sequence that it looks to run the associated programs as below.
:: 1. Run Scrapy to scrape the bird sightings from the specified hotspot from eBird
:: 2. Run the Compare program that will produce the output file

echo off

::Capture the directory if invocation of this script
set BASE_DIR=%CD%

::Include the Anaconda3 distrubution as well the other installed utilities such Scrapy in the PATH.
::Change the path if required to suit your specific environment
PATH=%PATH%;C:\Users\tjob\Anaconda3;C:\Users\tjob\Anaconda3\Scripts

::Set the working directory CWD_UTIL. It assumes the following:
::Path for Scrapy crawler that will crawl and scrape eBird is $CWD_UTIL\Scrapy\ebirdscraper\
::Path for the Python code that compares the files is $CWD_UTIL\Python
set CWD_UTIL="D:\Thomas Job\Coding"
::echo %CWD_UTIL%

::Set the URL_TO_SCRP variable to specify the URL to be scraped from eBird. This should correspond to the hotspot that you are wanting to analysis on
set URL_TO_SCRP="https://ebird.org/hotspot/L2357332?yr=all&m=&rank=mrec"
::echo %URL_TO_SCRP%

::Specify the Hotspot name. This will be used to set the output filename for easy identification
set HOTSPOT=Pulicat_Lake
echo Hotspot : %HOTSPOT%

::Specify the Lifer list filename. This variable can be used to make comparison with world, country, region, hotspot as required.Just specify the Lifer list filename of containing that of required
set LIFER_FILENAME=World_Life_List_Names_Only.csv

::Set the CLEAN_FLAG. If set to Y, then the intermediate scraped file will be deleted. If set to N it will be left intact
set CLEAN_FLAG=Y

::Invoke Scrapy with relavent arguments
cd %CWD_UTIL%\Scrapy\ebirdscraper
del %HOTSPOT%.csv
echo Scraping eBird Hotspot URL : %URL_TO_SCRP%
scrapy crawl ebirdbot -a url=%URL_TO_SCRP% -o %HOTSPOT%.csv

::Move the scraped file to the directory where the Compare_2_Files.py resides
move /Y %CWD_UTIL%\Scrapy\ebirdscraper\%HOTSPOT%.csv %CWD_UTIL%\Python\Extract_Target_List

::Run the Compare program
echo Comparing Hotspot list with Lifer list
python %CWD_UTIL%\Python\Extract_Target_List\Compare_2_Files.py -d %CWD_UTIL%\Python\Extract_Target_List -m %LIFER_FILENAME% -c %HOTSPOT%.csv -o %HOTSPOT%_Potential_Lifers.csv

::Move the resulting file to the directory of invocation of this script
move /Y %CWD_UTIL%\Python\Extract_Target_List\%HOTSPOT%_Potential_Lifers.csv "%BASE_DIR%"\

::Delete the intermediate scraped file if CLEAN_FLAG is Y
if %CLEAN_FLAG%==Y (
    echo Deleting the scraped file...
    del %CWD_UTIL%\Python\Extract_Target_List\%HOTSPOT%.csv
)

::Return to the directory of invocation
cd "%BASE_DIR%"
