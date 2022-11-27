import math

class CircularTrips():
    def to_int(self,x):
        x = float(x)
        if not math.isnan(x):
            return int(float(x))
        return x

    def convert_distance_to_int(self,trips):
        trips.loc[:, 'distance'] = trips['distance'].apply(self.to_int)
        # print(trips['distance'])
        return trips

    def calculate_percentage_of_circular_trips(self,trips):
        return len(trips[trips['distance'] == 0])/len(trips)
    
    def find_circular_trips(self,trips):
        return trips[trips['distance'] == 0]