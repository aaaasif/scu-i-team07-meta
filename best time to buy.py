%pyspark
from pyspark.sql import functions as F
from pyspark.sql.types import IntegerType

# Load the dataset from HDFS
itineraries_df = spark.read.option("header", "true").csv("hdfs:///datasets/itineraries/itineraries.csv")

# Convert relevant columns to appropriate data types
itineraries_df = itineraries_df.withColumn("totalFare", itineraries_df["totalFare"].cast(FloatType())) \
                               .withColumn("totalTravelDistance", itineraries_df["totalTravelDistance"].cast(IntegerType())) \
                               .withColumn("travelDuration", itineraries_df["travelDuration"].cast(StringType())) \
                               .withColumn("searchDate", F.to_date(itineraries_df["searchDate"], "M/d/yyyy")) \
                               .withColumn("flightDate", F.to_date(itineraries_df["flightDate"], "M/d/yyyy")) \
                               .withColumn("segmentsDepartureTimeRaw", F.to_timestamp(itineraries_df["segmentsDepartureTimeRaw"])) \
                               .withColumn("segmentsArrivalTimeRaw", F.to_timestamp(itineraries_df["segmentsArrivalTimeRaw"]))

# Filter out any irrelevant rows (if necessary)
itineraries_df = itineraries_df.filter(F.col("searchDate").isNotNull() & F.col("flightDate").isNotNull())

# Adding a new column to calculate the booking lead time (days between search and flight date)
itineraries_df = itineraries_df.withColumn("bookingLeadTime", F.datediff(itineraries_df["flightDate"], itineraries_df["searchDate"]))

# Seasonal trends: Extract month and day of the week from the flightDate
itineraries_df = itineraries_df.withColumn("month", F.month(itineraries_df["flightDate"])) \
                               .withColumn("dayOfWeek", F.dayofweek(itineraries_df["flightDate"]))

# Calculate average total fare for each month to detect seasonal trends
seasonal_fare_trends = itineraries_df.groupBy("month").agg(F.avg("totalFare").alias("avgTotalFare"))

# Calculate the average total fare by booking lead time to analyze booking patterns
booking_lead_fare = itineraries_df.groupBy("bookingLeadTime").agg(F.avg("totalFare").alias("avgFareByBookingLead"))

# Calculate the average fare by day of the week to analyze price fluctuations
day_of_week_fare = itineraries_df.groupBy("dayOfWeek").agg(F.avg("totalFare").alias("avgFareByDayOfWeek"))

# Detect patterns by comparing prices with different lead times (within 30 days, 31-60 days, etc.)
lead_time_bins = itineraries_df.withColumn("leadTimeCategory", 
                                           F.when(F.col("bookingLeadTime") <= 30, "0-30 days")
                                           .when((F.col("bookingLeadTime") > 30) & (F.col("bookingLeadTime") <= 60), "31-60 days")
                                           .when(F.col("bookingLeadTime") > 60, "60+ days"))

lead_time_fare = lead_time_bins.groupBy("leadTimeCategory").agg(F.avg("totalFare").alias("avgFareByLeadTimeCategory"))

# Show the results for each analysis
seasonal_fare_trends.show()
booking_lead_fare.show()
day_of_week_fare.show()
lead_time_fare.show()

# You can use the below line to save the results to a new location or create a view for further analysis
# seasonal_fare_trends.write.option("header", "true").csv("hdfs:///path/to/save/seasonal_fare_trends.csv")
