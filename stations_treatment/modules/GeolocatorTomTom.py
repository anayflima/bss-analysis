import sys
sys.path.append('./modules')
sys.path.append('./stations_treatment/modules')
from Geolocator import Geolocator
import requests
 
class GeolocatorTomTom(Geolocator):
    """
        GeolocatorTomTom implements Geolocator using TomTom Routing API.
    """
    apiURL = "https://api.tomtom.com/routing/1/calculateRoute"

    def __init__(self, apiKey):
        """
            The API key is mantadory for using TomTom Routing API.
            Get the key from https://developer.tomtom.com/user/register.
        """
        self.apiKey = apiKey
        self.routePoints = []
    
    def getCoordinates(self, location):
        return super().getCoordinates(location)

    def getRoutePoints(self):
        return self.routePoints 

    def getDistanceFromCoordinates(self, srcLatitude, srcLongitude, dstLatitude, dstLongitude, mode):

        if (mode not in super().transportationModes): 
            return self.badResponse(self.MODERR)


        url = self.__mountUrl(srcLatitude, srcLongitude, dstLatitude, dstLongitude, mode)
        
        parsed = self.__makeRequest(url)

        if (parsed == self.ERR): return self.badResponse(self.ERR)

        lengthInMeters = parsed['routes'][0]['summary']['lengthInMeters']
        travelTimeInSeconds = parsed['routes'][0]['summary']['travelTimeInSeconds']

        return self.goodResponseLenghtTime(lengthInMeters, travelTimeInSeconds)

    def getRoute(self, source, destination, mode):
        
        # Check-ups
        srcLatitude, srcLongitude = super().getCoordinates(source)
        if (srcLatitude, srcLongitude) == super().COORDINATES_NOT_FOUND: 
            return self.badResponse(self.SRCERR)

        dstLatitude, dstLongitude = super().getCoordinates(destination)
        if (dstLatitude, dstLongitude) == super().COORDINATES_NOT_FOUND: 
            return self.badResponse(self.DSTERR)

        if (mode not in super().transportationModes): 
            return self.badResponse(self.MODERR)


        url = self.__mountUrl(srcLatitude, srcLongitude, dstLatitude, dstLongitude, mode)
        
        parsed = self.__makeRequest(url)

        if (parsed == self.ERR): return self.badResponse(self.ERR)

        routePoints = []
        for p in parsed['routes'][0]['legs'][0]['points']:
            routePoints.append([p['longitude'], p['latitude']])
        
        travelTime = parsed['routes'][0]['summary']['travelTimeInSeconds']

        return self.goodResponse(travelTime, routePoints)
    
    def __mountUrl(self, scrLatitude, srcLongitude, dstLatitude, dstLongitude, mode):
        return f'{self.apiURL}/{scrLatitude},{srcLongitude}:{dstLatitude},{dstLongitude}/json?travelMode={mode}&key={self.apiKey}'

    def __makeRequest(self, url):
        """
            This method manages https requests and handles the exceptions that may rise.
        """
        try:
            r = requests.get(url = url)
            parsed = r.json()
            r.raise_for_status()

        except requests.exceptions.HTTPError as errh:
            print ("Http Error: ", errh)
            return self.ERR

        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting: ", errc)
            return self.ERR

        except requests.exceptions.Timeout as errt:
            print ("Timeout Error: ", errt)
            return self.ERR

        except requests.exceptions.RequestException as err:
            print ("Something went wrong while trying to send request to TomTom", err)
            return self.ERR
        else: 
            return parsed