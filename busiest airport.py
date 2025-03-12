%pyspark
# Count the frequency of each airport appearing as a starting and destination airport
from pyspark.sql.functions import col, count, desc

# Count occurrences for startingAirport
starting_airports = df.groupBy("startingAirport").agg(count("*").alias("departures"))

# Count occurrences for destinationAirport
destination_airports = df.groupBy("destinationAirport").agg(count("*").alias("arrivals"))

# Merge both counts
busiest_airports = starting_airports.join(destination_airports, 
                                          starting_airports["startingAirport"] == destination_airports["destinationAirport"], 
                                          "outer") \
                                   .fillna(0) \
                                   .withColumn("total_flights", col("departures") + col("arrivals")) \
                                   .select(col("startingAirport").alias("airport"), "departures", "arrivals", "total_flights") \
                                   .orderBy(desc("total_flights"))

# Show Top 10 Busiest Airports
busiest_airports.show(10)
