%pyspark
# Count the frequency of each route (startingAirport → destinationAirport)
route_counts = df.groupBy("startingAirport", "destinationAirport") \
                 .agg(count("*").alias("route_count")) \
                 .orderBy(desc("route_count"))

# Show Top 10 Most Popular Flight Routes
route_counts.show(10)