%pyspark
from pyspark.sql import functions as F
from pyspark.sql.types import IntegerType

# Define the function to calculate the lowest price for each destination
def find_cheapest_destinations(departure, destinations, time_frame):
    # Convert the 'travelDuration' column to total minutes (handle PTxHyM format)
    def convert_duration_to_minutes(duration):
        import re
        if duration is None:
            return 0  # Return 0 for missing or None duration
        
        # Extract hours and minutes from the 'PTxHyM' format
        match = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?", duration)
        
        # If matching fails, return 0 (invalid format)
        if match is None:
            return 0
        
        hours = int(match.group(1) or 0)
        minutes = int(match.group(2) or 0)
        return hours * 60 + minutes

    # UDF to apply the conversion to the 'travelDuration' column
    convert_duration_udf = F.udf(convert_duration_to_minutes, IntegerType())
    
    # Filter flights based on the departure and travel time
    filtered_flights = df.filter(
        (df['startingAirport'] == departure) &
        (df['destinationAirport'].isin(destinations))
    )
    
    # Add the 'totalMinutes' column for comparison
    filtered_flights = filtered_flights.withColumn('totalMinutes', convert_duration_udf(df['travelDuration']))
    
    # Convert time_frame (e.g., '5h') into minutes (e.g., 300 minutes)
    time_frame_minutes = int(time_frame.replace('h', '')) * 60

    # Filter based on the travel duration (in minutes)
    filtered_flights = filtered_flights.filter(filtered_flights['totalMinutes'] <= time_frame_minutes)
    
    # Find the minimum price for each destination
    cheapest_destinations = filtered_flights.groupBy("destinationAirport").agg(F.min("totalFare").alias("lowestPrice"))
    
    return cheapest_destinations

# Define the list of destinations you are interested in
destinations = ['BOS', 'CLT', 'DEN', 'DFW', 'DTW', 'EWR', 'IAD', 'JFK', 'LAX', 'LGA', 'MIA', 'OAK', 'ORD', 'PHL', 'SFO']

# Run the function for a specific departure airport (ATL) and time frame (for example, '5h')
cheapest = find_cheapest_destinations('ATL', destinations, '5h')

# Show the result
cheapest.show()
