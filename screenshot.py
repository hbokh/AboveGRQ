#
# screenshot.py
#
# kevinabrandon@gmail.com
#
# edit by simon@sandm.co.uk to use Chromedriver
# edit by scott@ladewig.com to work for either Selenium 4.3.0+ or older version originally used
# edit by hbokh to use geckodriver

import time
from selenium import webdriver
from selenium.common import exceptions as seleniumexceptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from configparser import ConfigParser

import util
import datasource

# Read the configuration file for this application.
parser = ConfigParser()
parser.read('config.ini')

# Assign AboveTustin variables.
abovetustin_image_width = int(parser.get('abovetustin', 'image_width'))
abovetustin_image_height = int(parser.get('abovetustin', 'image_height'))
sleep_time = int(parser.get('abovetustin', 'sleep_time'))
wait_time = int(parser.get('abovetustin', 'wait_time'))
request_timeout = int(parser.get('abovetustin', 'request_timeout'))

capabilities = webdriver.DesiredCapabilities.FIREFOX.copy()
capabilities['firefox.page.settings.resourceTimeout'] = "20000"

driver_path = parser.get("apps", "driver_path")
browser_path = parser.get("apps", "browser_path")


# Using geckodriver
options = webdriver.FirefoxOptions()
options.add_argument("--headless")

# Checking to see if we need to use Selenium 4.3.0+ commands or pre4.3.0.
webdriverversion = (webdriver.__version__).split(".")
webdriverversionmajor = int(webdriverversion[0])
webdriverversionminor = int(webdriverversion[1])

#  Check for Crop settings
if parser.has_section('crop'):
    do_crop = parser.getboolean('crop', 'do_crop')
    crop_x = parser.getint('crop', 'crop_x')
    crop_y = parser.getint('crop', 'crop_y')
    crop_width = parser.getint('crop', 'crop_width')
    crop_height = parser.getint('crop', 'crop_height')
    if do_crop:
        try:
            from PIL import Image
            from io import BytesIO
            print('Will crop')
        except ImportError:
            print('Image manipulation module "Pillow" not found, cropping disabled')
            do_crop = False
else:
    do_crop = False

# Assign dump1090 variables.
g_request_timeout = float(parser.get('abovetustin', 'request_timeout'))


class AircraftDisplay(object):
    def __init__(self, url):
        self.url = url
        self.browser = None
        self.loadmap()

    def loadmap(self):
        raise NotImplementedError

    def reload(self):
        self.browser.quit()
        self.browser = None
        self.loadmap()

    def screenshot(self, name):
        '''
        screenshot()
        Takes a screenshot of the browser
        '''
        if do_crop:
            print('Cropping screenshot')
            #  Grab screenshot rather than saving
            im = self.browser.get_screenshot_as_png()
            im = Image.open(BytesIO(im))

            #  Crop to specifications
            im = im.crop((crop_x, crop_y, crop_width, crop_height))
            im.save(name)
        else:
            self.browser.save_screenshot(name)
        print("Success saving screenshot: %s" % name)
        return name

    def ClickOnAirplane(self, ident):
        raise NotImplementedError


class Dump1090Display(AircraftDisplay):
    def loadmap(self):
        '''
        loadmap()
        Creates a browser object and loads the webpage.
        It sets up the map to the proper zoom level.

        Returns the browser on success, None on fail.
        '''

        browser = webdriver.Firefox(options=options)
        browser.set_window_size(abovetustin_image_width, abovetustin_image_height)

        print("Getting web page {}".format(self.url))
        browser.set_page_load_timeout(15)
        browser.get(self.url)

        # Need to wait for the page to load
        timeout = g_request_timeout
        print("Waiting for page to load...")
        wait = WebDriverWait(browser, timeout)
        try:
            element = wait.until(EC.element_to_be_clickable((By.ID, 'tar1090_version')))
        except seleniumexceptions.TimeoutException:
            util.error("Loading %s timed out.  Check that you're using the "
                       "correct driver in the .ini file." % (self.url,))
            browser.save_screenshot('timeout.png')
            util.error('Saved screenshot at timeout.png')
            raise

        print("Reset map")
        resetbutton = browser.find_elements(By.XPATH, '//*[contains(@title,"Reset Map")]')
        resetbutton[0].click()

        # Zoom in on the map. If you need more zoom, uncomment some of the zoomin.click().
        print("Zoom in")
        try:
            # First look for the Open Layers map zoom button.
            zoomin = browser.find_element(By.CLASS_NAME, 'ol-zoom-in')
            # print("Zoom: ", zoomin)
        except seleniumexceptions.NoSuchElementException as e:
            # Doesn't seem to be Open Layers, so look for the Google
            # maps zoom button.
            zoomin = browser.find_elements(By.XPATH, '//*[@title="Zoom in"]')
            if zoomin:
                zoomin = zoomin[0]
        zoomin.click()
        zoomin.click()
        # zoomin.click()
        self.browser = browser

# Screen capture only tracked plane
# Image grabbed at time of alert not on preload

    def clickOnAirplane(self, hex):
        '''
        clickOnAirplane()
        Clicks on the airplane with the name text, and then takes a screenshot
        '''
        browser = webdriver.Firefox(options=options)
        browser.set_window_size(abovetustin_image_width, abovetustin_image_height)
        browser.set_page_load_timeout(15)
        self.browser = browser

        try:
            url = f"{self.url}?icao={hex}"
            url += datasource.g_map_parameters
            print(f"Opening {url}")
            self.browser.get(url)
            try:
                time.sleep(wait_time)
                element = WebDriverWait(self.browser, request_timeout).until(
                    EC.presence_of_element_located((By.ID, "selected_icao"))
                )
            except Exception as err:
                print('Exception: %s' % err)
            if self.browser:
                time.sleep(wait_time)
                self.screenshot('screenshot.png')
                browser.close()
            else:
                print('Could not find browser')
                return None
        except Exception as err:
            print('Exception: %s' % err)
            return None


class VRSDisplay(AircraftDisplay):
    def loadmap(self):
        '''
        loadmap()
        Creates a browser object and loads the webpage.
        It sets up the map to the proper zoom level.

        Returns the browser on success, None on fail.
        '''

        browser = webdriver.Firefox(executable_path=driver_path, desired_capabilities=capabilities, options=options)
        browser.set_window_size(abovetustin_image_width, abovetustin_image_height)

        print("Getting web page {}".format(self.url))
        browser.set_page_load_timeout(15)
        browser.get(self.url)

        # Need to wait for the page to load
        timeout = g_request_timeout
        print("Waiting for page to load...")
        wait = WebDriverWait(browser, timeout)
        element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'vrsMenu')))
        self.browser = browser

    def clickOnAirplane(self, text):
        '''
        clickOnAirplane()
        Clicks on the airplane with the name text, and then takes a screenshot
        '''
        try:
            aircraft = self.browser.find_element(By.XPATH, "//tr[@id='%s']" % text)
            aircraft.click()
            time.sleep(0.5)  # if we don't wait a little bit the airplane icon isn't drawn.
            show_on_map = self.browser.find_element_by_link_text('Show on map')
            show_on_map.click()
            time.sleep(3.0)
            return self.screenshot('screenshot.png')
        except Exception as e:
            util.error("Unable to click on airplane: {}'".format(e))
            return None
