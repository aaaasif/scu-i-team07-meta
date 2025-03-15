const path = require('path');  
require('dotenv').config({ path: path.resolve(__dirname, '.env') });

const express = require('express');
const cors = require('cors');
const axios = require('axios');
const fs = require('fs');

const app = express();
app.use(express.json());
app.use(cors());

const PORT = process.env.PORT || 5000;
const OPENROUTER_API_KEY = process.env.OPENROUTER_API_KEY;

// to Validate API Key
if (!OPENROUTER_API_KEY) {
    console.error(" ERROR: OpenRouter API Key is missing. Please set it in the .env file.");
    process.exit(1);
}

// to Load Flight Data JSON
let dataset = {};
const datasetFilePath = path.join(__dirname, 'datasets', 'flight_data.json');

if (!fs.existsSync(datasetFilePath)) {
    console.error(" ERROR: 'flight_data.json' file not found. Ensure it exists in the 'datasets' folder.");
    process.exit(1);
}

try {
    dataset = JSON.parse(fs.readFileSync(datasetFilePath, 'utf8'));
    console.log(`✔ Successfully loaded dataset: flight_data.json`);
} catch (error) {
    console.error(` ERROR: Unable to parse flight_data.json:`, error);
    process.exit(1);
}

// these are helper Function to Normalize Queries
const normalizeQuery = (query) => query.toLowerCase().trim();

// the function to Find Flight Fare Information
const findFlightFareInfo = (startingAirport, destinationAirport, fareType = "cheapestFare") => {
    const flight = dataset.flight_fares.find(entry =>
        normalizeQuery(entry.startingAirport) === normalizeQuery(startingAirport) &&
        normalizeQuery(entry.destinationAirport) === normalizeQuery(destinationAirport)
    );
    return flight ? flight : null;
};

// the Function to Find Layover and Flight Details
const findLayoverInfo = (startingAirport, destinationAirport) => {
    return dataset.layover_info.find(entry =>
        normalizeQuery(entry.startingAirport) === normalizeQuery(startingAirport) &&
        normalizeQuery(entry.destinationAirport) === normalizeQuery(destinationAirport)
    );
};

// this is the Function to Find Busiest Airports
const findBusiestAirport = (query) => {
    if (query.includes('busiest')) {
        const airport = dataset.busiest_airports.sort((a, b) => b.total_flights - a.total_flights)[0];
        return `The busiest airport is ${airport.BussiestAIRPORTS} with ${airport.total_flights} total flights.`;
    } else if (query.includes('least busiest')) {
        const airport = dataset.busiest_airports.sort((a, b) => a.total_flights - b.total_flights)[0];
        return `The least busiest airport is ${airport.BussiestAIRPORTS} with ${airport.total_flights} total flights.`;
    }
    return null;
};






// this Function is  to Find Airport Traffic Data (Departures, Arrivals, Total Flights)
const findAirportTraffic = (airportCode, trafficType) => {
    const airportData = dataset.busiest_airports.find(entry =>
        normalizeQuery(entry.BussiestAIRPORTS) === normalizeQuery(airportCode)
    );

    if (!airportData) return `No data available for airport ${airportCode}.`;

    switch (trafficType) {
        case "departures":
            return `${airportCode} has ${airportData.departures} departures.`;
        case "arrivals":
            return `${airportCode} has ${airportData.arrivals} arrivals.`;
        case "total flights":
            return `${airportCode} has ${airportData.total_flights} total flights.`;
        default:
            return `${airportCode}: Departures = ${airportData.departures}, Arrivals = ${airportData.arrivals}, Total Flights = ${airportData.total_flights}.`;
    }
};






//  it is the Function to Find Popular Routes
const findBusiestRoute = () => {
    const route = dataset.busiest_routes.sort((a, b) => b['route count'] - a['route count'])[0];
    return `The busiest route is ${route.startingAirport} to ${route.destinationAirport}.`;
};

// this Function is to Find Best Booking Time
const findBestBookingTime = (query) => {
    if (query.includes("best month")) {
        const bestMonth = dataset.best_time_to_book.filter(item => item.type === "month").sort((a, b) => a.avgTotalFare - b.avgTotalFare)[0];
        return `The best month to buy tickets is ${bestMonth.value} with an average fare of $${bestMonth.avgTotalFare.toFixed(2)}.`;
    }
    if (query.includes("best time to buy")) {
        const bestTime = dataset.best_time_to_book.filter(item => item.type === "days_before").sort((a, b) => a.avgTotalFare - b.avgTotalFare)[0];
        return `The best time to book a ticket is ${bestTime.value} before departure with an average fare of $${bestTime.avgTotalFare.toFixed(2)}.`;
    }
    return null;
};

// overall  Dataset Search Function for Multiple Queries by users
const searchDataset = (query) => {
    query = normalizeQuery(query);

    // Flight Fares
    const fareMatch = query.match(/(cheapest|lowest|average)?\s*(fare|price|cost)?\s*from\s*(\w{3})\s*to\s*(\w{3})/);
    if (fareMatch) {
        const [_, fareType, priceType, startingAirport, destinationAirport] = fareMatch;
        const fareKey = fareType && fareType.includes("average") ? "averageFare" : "cheapestFare";
        const flightInfo = findFlightFareInfo(startingAirport, destinationAirport, fareKey);

        if (flightInfo) {
            return `${startingAirport} → ${destinationAirport}: ${fareType || 'Cheapest'} Fare = $${flightInfo[fareKey]}, Airline = ${flightInfo.cheapestAirline}`;
        }
    }

    
      // for multiple queries and keywords
      const airportTrafficMatch = query.match(/(?:what is|write the|tell me the|can you please tell me|can you tell me|what|how many)\s+(departures|arrivals|total flights)\s+(\w{3})\s*has\??/i);
      if (airportTrafficMatch) {
          const [_, trafficType, airportCode] = airportTrafficMatch;
          return findAirportTraffic(airportCode, trafficType);
      }


  

    // Flight Layover Details
const layoverMatch = query.match(/(?:layover|transit|connecting flight|multistop flight location|non-stop|flight type).*from\s+(\w{3})\s+to\s+(\w{3})/i);
if (layoverMatch) {
    const [_, startingAirport, destinationAirport] = layoverMatch;
    const layoverInfo = findLayoverInfo(startingAirport, destinationAirport);

    if (layoverInfo) {
        const layoverStops = layoverInfo.layover && layoverInfo.layover.length > 0 ? ` (via ${layoverInfo.layover.join(" | ")})` : " (Non-Stop)";
        const fare = layoverInfo.fare ? `Fare = $${layoverInfo.fare}` : "Fare data unavailable";
        const travelTime = layoverInfo["Travel time"] ? `Travel Time = ${layoverInfo["Travel time"]}` : "Travel time unavailable";
        const airline = layoverInfo.Airlines ? `Airline = ${layoverInfo.Airlines}` : "Airline information unavailable";

        return `${startingAirport} → ${destinationAirport}${layoverStops}: ${fare}, ${travelTime}, ${airline}`;
    }
}


    // Busiest Airport
    const busiestAirportAnswer = findBusiestAirport(query);
    if (busiestAirportAnswer) return busiestAirportAnswer;

    // Busiest Route
    if (query.includes("busiest route")) return findBusiestRoute();

    // Best Booking Time
    const bestBookingAnswer = findBestBookingTime(query);
    if (bestBookingAnswer) return bestBookingAnswer;


     // Fixed Answers
     const fixedAnswers = {
        "which months are the best to buy the tickets?": "May tends to have the lowest average fare compared to April and June.",
        "which day has the lowest ticket fare?": "Wednesdays have the lowest average fares ($297.82), making them the best days to fly!",
        "which day has the highest ticket fare?": "Mondays are the most expensive days to fly ($428.12).",
        "what is the best time to book flights?": "Book around 22 days before departure (Lowest fare: $283.07). Fly on Wednesdays (Cheapest travel day: $297.82).",
        "which days has the most expensive ticket fare?":"Mondays are the most expensive days to fly ($428.12) and  Weekends (Saturday & Sunday) tend to be more expensive than midweek flights.",
        "what is the worst  time to book flights?" : "Booking only 6 days before departure (Highest fare- $429.61).Flying on Mondays (Most expensive day- $428.12).Last-minute bookings (0-30 days) result in higher ticket prices.",
        "write top 10 most popular route?": "LGA to LAX,LAX  to LGA,LAX to ATL,LAX to BOS,LAX to EWR,ATL to LAX,BOS to LAX,LAX to JFK,CLT to LAX,JFK to LAX",
        "write top 10 most popular Airport?": "LAX,LGA,BOS,DFW,ORD,MIA,SFO,ATL,CLT,DEN.",
        "what is the best time to fly?":"Book around 22 days before departure (Lowest fare- $283.07). Fly on Wednesdays (Cheapest travel day- $297.82).May tends to have the lowest average fare compared to April and June.April and June have slightly higher fares.Booking flights 31-60 days before departure gives better deals than last-minute bookings.Last-minute bookings (0-30 days) tend to be expensive.",
        "what is the best time to book tickets?":"Book around 22 days before departure (Lowest fare- $283.07). Fly on Wednesdays (Cheapest travel day- $297.82).May tends to have the lowest average fare compared to April and June.April and June have slightly higher fares.Booking flights 31-60 days before departure gives better deals than last-minute bookings.Last-minute bookings (0-30 days) tend to be expensive.",
        "what is the best time to fly from LAX to LGA?":"Book around 22 days before departure (Lowest fare- $283.07). Fly on Wednesdays (Cheapest travel day- $297.82).May tends to have the lowest average fare compared to April and June.April and June have slightly higher fares.Booking flights 31-60 days before departure gives better deals than last-minute bookings.Last-minute bookings (0-30 days) tend to be expensive.",
      
    };

    if (fixedAnswers[query]) return fixedAnswers[query];

    return null;
};

// Chatbot API Endpoint
app.post('/chat', async (req, res) => {
    const userQuery = req.body.query;

    if (!userQuery) {
        return res.status(400).json({ answer: " ERROR: Query cannot be empty." });
    }

    console.log(` User asked: ${userQuery}`);

    // to Search in Dataset
    const datasetAnswer = searchDataset(userQuery);
    if (datasetAnswer) return res.json({ answer: datasetAnswer });

    // if not find Fallback to DeepSeek AI
    try {
        const response = await axios({
            method: 'post',
            url: 'https://openrouter.ai/api/v1/chat/completions',
            headers: {
                'Authorization': "Bearer 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",
                'Content-Type': 'application/json',
                'HTTP-Referer': "https://www.deepseek.com",
                'X-Title': "DeepSeekChatbot"
            },
            data: {
                model: 'deepseek/deepseek-r1-zero:free',
                messages: [{ role: 'user', content: userQuery }]
            }
        });

        let aiAnswer = response.data.choices?.[0]?.message?.content || "No response from AI";

        // to Remove unwanted prefixes
        aiAnswer = aiAnswer.replace(/\\boxed\{|\}/g, '').trim();

        console.log(`AI Response: ${aiAnswer}`);

        res.json({ answer: aiAnswer });
    } catch (error) {
        console.error("❌ DeepSeek API Error:", error.response?.data || error.message);
        res.status(500).json({ answer: "❌ ERROR: Unable to connect to AI service." });
    }
});

// **Start Server**
app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));





































































































































































          