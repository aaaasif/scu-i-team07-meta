%pyspark
from pyspark.sql import functions as F
from pyspark.sql.types import IntegerType, StringType, FloatType

# Load the itineraries dataset from HDFS
itineraries_df = spark.read.option("header", "true").csv("hdfs:///datasets/itineraries/itineraries.csv")

# Convert relevant columns to appropriate data types
itineraries_df = itineraries_df.withColumn("totalFare", itineraries_df["totalFare"].cast(FloatType())) \
                               .withColumn("totalTravelDistance", itineraries_df["totalTravelDistance"].cast(IntegerType())) \
                               .withColumn("travelDuration", itineraries_df["travelDuration"].cast(StringType())) \
                               .withColumn("searchDate", F.to_date(itineraries_df["searchDate"], "M/d/yyyy")) \
                               .withColumn("flightDate", F.to_date(itineraries_df["flightDate"], "M/d/yyyy")) \
                               .withColumn("segmentsDepartureTimeRaw", F.to_timestamp(itineraries_df["segmentsDepartureTimeRaw"])) \
                               .withColumn("segmentsArrivalTimeRaw", F.to_timestamp(itineraries_df["segmentsArrivalTimeRaw"]))

# Filter out relevant flights that are either direct (CLT to LAX) or multi-stop
clt_to_lax_df = itineraries_df.filter(
    (itineraries_df["startingAirport"] == "CLT") & (itineraries_df["destinationAirport"] == "LAX")
)

# For multi-stop flights, we need to find those that have CLT as the starting point and LAX as the destination
# And also filter to get only those with layovers
multi_stop_flights_df = itineraries_df.filter(
    (itineraries_df["startingAirport"] == "CLT") & 
    (itineraries_df["destinationAirport"] == "LAX") & 
    (itineraries_df["segmentsArrivalAirportCode"] != "LAX")
)

# Calculate layover time (time between arrival at intermediate airport and departure from it)
multi_stop_flights_df = multi_stop_flights_df.withColumn(
    "layoverTime",
    (F.unix_timestamp(multi_stop_flights_df["segmentsDepartureTimeRaw"]) - F.unix_timestamp(multi_stop_flights_df["segmentsArrivalTimeRaw"])) / 3600
)

# Filter multi-stop flights to meet the minimum layover time (e.g., 1 hour)
min_layover_time = 1  # Layover time in hours
valid_multi_stop_flights_df = multi_stop_flights_df.filter(F.col("layoverTime") >= min_layover_time)

# Now join multi-stop flights with the corresponding intermediate airports
# Add the segment details (i.e., the layover airport)
multi_stop_with_airports_df = valid_multi_stop_flights_df.select(
    "legId",
    "searchDate",
    "flightDate",
    "startingAirport",
    "destinationAirport",
    "travelDuration",
    "isNonStop",
    "totalFare",
    "totalTravelDistance",
    "segmentsDepartureTimeRaw",
    "segmentsArrivalTimeRaw",
    "segmentsArrivalAirportCode",
    "segmentsDepartureAirportCode",
    "segmentsAirlineName",
    "segmentsEquipmentDescription",
    "layoverTime"
)

# Add a null column for 'layoverTime' to the clt_to_lax_df dataframe
from pyspark.sql.functions import lit

clt_to_lax_with_layover_df = clt_to_lax_df.withColumn("layoverTime", lit(None))

# Now perform the union with the multi-stop flights
final_results_df = clt_to_lax_with_layover_df.select(
    "legId", "searchDate", "flightDate", "startingAirport", "destinationAirport", 
    "travelDuration", "isNonStop", "totalFare", "totalTravelDistance", 
    "segmentsDepartureTimeRaw", "segmentsArrivalTimeRaw", 
    "segmentsArrivalAirportCode", "segmentsDepartureAirportCode", 
    "segmentsAirlineName", "segmentsEquipmentDescription", "layoverTime"
).union(multi_stop_with_airports_df)

# Show the final results
final_results_df.show()
