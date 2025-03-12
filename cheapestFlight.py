%pyspark
from pyspark.sql import functions as F
from pyspark.sql.types import IntegerType

# Define the function to calculate the lowest price for each destination
def find_cheapest_destinations(departure, destinations):
    # Filter flights based on the departure and destination (no time frame)
    filtered_flights = df.filter(
        (df['startingAirport'] == departure) & 
        (df['destinationAirport'].isin(destinations))
    )
    
    # Find the minimum price for each destination
    cheapest_destinations = filtered_flights.groupBy("destinationAirport").agg(F.min("totalFare").alias("lowestPrice"))
    
    return cheapest_destinations

# Define the list of destinations you are interested in
destinations = ['BOS', 'CLT', 'DEN', 'DFW', 'DTW', 'EWR', 'IAD', 'JFK', 'LAX', 'LGA', 'MIA', 'OAK', 'ORD', 'PHL', 'SFO']

# Run the function for a specific departure airport (ATL)
cheapest = find_cheapest_destinations('ATL', destinations)

# Show the result
cheapest.show()