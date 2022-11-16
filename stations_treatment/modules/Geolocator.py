from abc import ABC, abstractmethod
from geopy.geocoders import Nominatim

class Geolocator(ABC):
    """ 
        Geolocator class computes the time spent in a route with Nominatim support.
        Nominatim is a geocoder which uses the OpenStreetMap dataset.
    """
    locator = Nominatim(user_agent="geocoder") 

    COORDINATES_NOT_FOUND = (-1,-1) # when coordinated not found
    ERR = -1                        # generic error return value
    SRCERR = -10                    # source location error return value
    DSTERR = -20                    # destination location error return value
    MODERR = -30                    # transportation mode error return value

    # transportation modes available
    transportationModes = [
        "car",
        "truck",
        "taxi",
        "bus",
        "van",
        "motorcycle",
        "bicycle",
        "pedestrian"
    ]

    @classmethod
    def getCoordinates(self, location):
        """
            This method uses Nominatim locator to obtain the latitude and longitude
            of a given location.
            Location should be a string such as "USP" or "Avenida Paulista, 119, Bela Vista".
        """
        
        geolocated = self.locator.geocode(location)

        if (geolocated == None):
            return self.COORDINATES_NOT_FOUND
        else:
            return (geolocated.latitude, geolocated.longitude)
    
    @classmethod
    def badResponse(self, code):
        """
            Assemble an error response according to the error type.
            Returns a dictionary containing an error code and its description.
        """
        message = ""

        if (code == self.ERR):
            message = "something went wrong in Geolocator"
        elif (code == self.SRCERR):
            message = "source location not found"
        elif (code == self.DSTERR):
            message = "destination location not found"
        elif (code == self.MODERR):
            message = "transportation mode not available"

        return { 'code' : code, 'message' : message }
    
    @classmethod
    def goodResponse(self, travelTime, routePoints):
        """
            Assemble a successful response.
            Returns a dictionary containing a successful code, the travel time and the route points.
        """
        return { 'code' : 0, 'travelTime' : travelTime, 'routePoints' : routePoints}
    
    @classmethod
    def goodResponseLenghtTime(self, lengthInMeters,travelTimeInSeconds):
        """
            Assemble a successful response.
            Returns a dictionary containing a successful code, the travel time and the route points.
        """
        return { 'code' : 0, 'lengthInMeters' : lengthInMeters, 'travelTimeInSeconds': travelTimeInSeconds}
    
    @abstractmethod
    def getRoute(self, source, destination, mode):
        """
            This method should be implemented to return the travel time 
            between source and destination locations using the given transportation mode
            and its route points.
            If something goes wrong, it returns a bad response.

            Transportation modes avaliable:
                car
                truck
                taxi
                bus
                van
                motorcycle
                bicycle
                pedestrian
            
            If any of the arguments are wrong, the method should return an erro code: 
                SRCERR - for incorrect source input
                DSTERR - for incorrect destination input
                MODERR - for incorrect mode input
            
            If another error occured, it returns ERR

        """
        pass

