import React, { useState, useEffect } from "react";
import { toast } from "react-toastify";
import { useLocation } from "react-router-dom";

// Enhanced BookTicketBox Component (previously imported)
const BookTicketBox = ({ formData, handleFormDataChange, handleFlightSearch }) => {
  return (
    <div className="my-8 bg-gradient-to-br from-blue-50 to-indigo-50 p-6 rounded-2xl shadow-lg border border-blue-100">
      <h2 className="text-2xl font-bold text-center mb-6 text-gray-800">Find Your Perfect Flight</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* From Field */}
        <div className="relative group">
          <div className="absolute -inset-0.5 bg-gradient-to-r from-blue-400 to-indigo-500 rounded-lg blur opacity-30 group-hover:opacity-100 transition duration-500"></div>
          <div className="relative bg-white rounded-lg p-4">
            <label className="block text-xs font-semibold text-gray-600 mb-1">From</label>
            <div className="flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-blue-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
              </svg>
              <input
                type="text"
                name="from"
                value={formData.from}
                onChange={handleFormDataChange}
                placeholder="City or Airport"
                className="w-full border-none focus:ring-0 text-gray-800 placeholder-gray-400 font-medium"
              />
            </div>
          </div>
        </div>
        
        {/* To Field */}
        <div className="relative group">
          <div className="absolute -inset-0.5 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-lg blur opacity-30 group-hover:opacity-100 transition duration-500"></div>
          <div className="relative bg-white rounded-lg p-4">
            <label className="block text-xs font-semibold text-gray-600 mb-1">To</label>
            <div className="flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-purple-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
              </svg>
              <input
                type="text"
                name="to"
                value={formData.to}
                onChange={handleFormDataChange}
                placeholder="City or Airport"
                className="w-full border-none focus:ring-0 text-gray-800 placeholder-gray-400 font-medium"
              />
            </div>
          </div>
        </div>
        
        {/* Date Field */}
        <div className="relative group">
          <div className="absolute -inset-0.5 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg blur opacity-30 group-hover:opacity-100 transition duration-500"></div>
          <div className="relative bg-white rounded-lg p-4">
            <label className="block text-xs font-semibold text-gray-600 mb-1">Departure Date</label>
            <div className="flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-pink-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              <input
                type="date"
                name="departDate"
                value={formData.departDate}
                onChange={handleFormDataChange}
                className="w-full border-none focus:ring-0 text-gray-800 placeholder-gray-400 font-medium"
              />
            </div>
          </div>
        </div>
        
        {/* Flight Type Field */}
        <div className="relative group">
          <div className="absolute -inset-0.5 bg-gradient-to-r from-pink-500 to-red-500 rounded-lg blur opacity-30 group-hover:opacity-100 transition duration-500"></div>
          <div className="relative bg-white rounded-lg p-4">
            <label className="block text-xs font-semibold text-gray-600 mb-1">Class</label>
            <div className="flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-red-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
              </svg>
              <select
                name="flightType"
                value={formData.flightType}
                onChange={handleFormDataChange}
                className="w-full border-none focus:ring-0 text-gray-800 bg-white"
              >
                <option value="Economy">Economy</option>
                <option value="Business">Business</option>
                <option value="First">First Class</option>
              </select>
            </div>
          </div>
        </div>
      </div>
      
      {/* Search Button */}
      <div className="mt-6 flex justify-center">
        <button
          onClick={handleFlightSearch}
          className="group relative inline-flex items-center justify-center px-8 py-3 overflow-hidden font-bold text-white rounded-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 shadow-lg"
        >
          <span className="absolute inset-0 w-full h-full -mt-1 rounded-full opacity-30 bg-gradient-to-b from-white via-transparent to-transparent"></span>
          <span className="relative flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            Search Flights
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 ml-2 transform group-hover:translate-x-1 transition-transform duration-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
            </svg>
          </span>
        </button>
      </div>
    </div>
  );
};

const TicketSearchPage = () => {
  const location = useLocation();
  const searchParams = new URLSearchParams(location.search);

  const [formData, setFormData] = useState({
    from: searchParams.get("from") || "",
    to: searchParams.get("to") || "",
    departDate: searchParams.get("departDate") || "",
    flightType: "Economy",
  });

  const [cheapestFlight, setCheapestFlight] = useState(null);
  const [searchStatus, setSearchStatus] = useState("");
  const [flightData, setFlightData] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  // Fetch the JSON data when the page loads
  useEffect(() => {
    const fetchFlightData = async () => {
      try {
        const response = await fetch("/searchquery.json");
        const data = await response.json();
        setFlightData(data);
      } catch (error) {
        console.error("Error fetching flight data:", error);
        toast.error("Error fetching flight data.");
      }
    };
    fetchFlightData();
  }, []);

  const handleFormDataChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevFormData) => ({
      ...prevFormData,
      [name]: value,
    }));
  };

  const handleFlightSearch = () => {
    if (!formData.from || !formData.to) {
      setSearchStatus("Enter flight details to search flights");
      setCheapestFlight(null);
      return;
    }
  
    setIsLoading(true);
    
    // Simulate loading time
    setTimeout(() => {
      const filteredFlights = flightData.filter(
        (flight) =>
          flight.startingAirport.toUpperCase() === formData.from.toUpperCase() &&
          flight.destinationAirport.toUpperCase() === formData.to.toUpperCase()
      );
  
      if (filteredFlights.length === 0) {
        setSearchStatus("No flights found for the selected route");
        setCheapestFlight(null);
      } else {
        // Use the averageFare from the JSON data instead of calculating it
        const cheapest = filteredFlights.reduce((prev, current) =>
          prev.cheapestFare < current.cheapestFare ? prev : current
        );
        
        // Get the averageFare from the JSON directly
        // This assumes each flight record has its own averageFare value
        const averageFare = Math.round(cheapest.averageFare);
  
        setCheapestFlight({
          ...cheapest,
          // Keep the original averageFare from the JSON
          averageFare: averageFare,
        });
  
        setSearchStatus(
          <>
            <b>Average Fare:</b> <b>${averageFare}</b>
            <br />
            <b>{cheapest.cheapestAirline}</b> offers the cheapest fare of <b>${cheapest.cheapestFare}</b> from <b>{formData.from}</b> to <b>{formData.to}</b>
          </>
        );
      }
      
      setIsLoading(false);
    }, 800);
  };
    

  return (
    <div className="px-[30px] md:px-[30px] max-w-[1400px] mx-auto py-8 bg-gray-50 min-h-screen">
      {/* Page Title */}
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-800">Find Your Perfect Flight</h1>
        <div className="h-1 w-24 bg-blue-600 mx-auto mt-2 rounded-full"></div>
      </div>
      
      {/* Enhanced Book Ticket Box */}
      <BookTicketBox
        formData={formData}
        handleFormDataChange={handleFormDataChange}
        handleFlightSearch={handleFlightSearch}
      />
      
      {/* Loading State */}
      {isLoading && (
        <div className="flex justify-center my-12">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-600"></div>
        </div>
      )}
      
      {/* Results Section */}
            {cheapestFlight && !isLoading && (
        <div className="mt-8">
          {/* Section Title */}
          <div className="text-center mb-6">
            <h2 className="text-2xl font-bold text-gray-800">Best Flight Deal</h2>
            <div className="h-1 w-16 bg-green-500 mx-auto mt-2 rounded-full"></div>
          </div>
          
          <div 
            className="flex justify-center items-center gap-5 flex-wrap w-full"
            style={{ 
              animation: "fadeIn 1s ease-in-out",
            }}
          >
            {/* Reduced width for smaller screens to prevent overflow */}
            <div className="w-full sm:w-[85%] md:w-[70%] lg:w-[50%] xl:w-[40%] relative overflow-visible">
              {/* Card with glass morphism effect */}
              <div className="relative bg-white bg-opacity-40 backdrop-filter backdrop-blur-lg p-6 rounded-2xl shadow-xl border border-white border-opacity-20 hover:shadow-2xl transform hover:-translate-y-2 transition-all duration-500 ease-in-out">
                
                {/* Best Deal Badge */}
                <div className="absolute -top-4 -right-4 bg-gradient-to-r from-red-500 to-pink-500 text-white px-6 py-1 rounded-full font-bold text-sm shadow-lg transform rotate-12 hover:rotate-0 transition-all duration-300 z-10">
                  Best Deal!
                </div>
                
                {/* Decorative Elements */}
                <div className="absolute -bottom-16 -right-16 w-32 h-32 bg-blue-500 rounded-full opacity-10"></div>
                <div className="absolute -top-16 -left-16 w-32 h-32 bg-purple-500 rounded-full opacity-10"></div>
                
                {/* Airline logo placeholder */}
                <div className="flex justify-center mb-4">
                  <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-full flex items-center justify-center text-white text-xl font-bold shadow-lg transform hover:rotate-12 transition-all duration-300">
                    {cheapestFlight.cheapestAirline.charAt(0)}
                  </div>
                </div>
                
                {/* Title */}
                <h3 className="text-xl font-bold text-center mb-4 text-gray-800 relative">
                  Cheapest Flight
                  <div className="h-1 w-12 bg-blue-500 mx-auto mt-2 rounded-full"></div>
                </h3>
                
                {/* Flight Route Visualization */}
                <div className="flight-path relative flex items-center justify-between mb-6 px-2">
                  <div className="text-center z-10">
                    <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-1">
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                      </svg>
                    </div>
                    <p className="text-xs text-gray-500">From</p>
                    <p className="font-bold text-lg text-blue-600">{formData.from}</p>
                  </div>
                  
                  <div className="flex-1 mx-4">
                    <div className="h-0.5 w-full bg-gradient-to-r from-blue-200 via-purple-200 to-pink-200 relative">
                      {/* Animated Plane */}
                      <div className="absolute -top-3 left-0 plane-animation">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-indigo-600 transform rotate-90" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                        </svg>
                      </div>
                      
                      <style jsx>{`
                        @keyframes flyPlane {
                          0% { left: 0; }
                          100% { left: calc(100% - 24px); }
                        }
                        .plane-animation {
                          animation: flyPlane 3s infinite alternate ease-in-out;
                        }
                      `}</style>
                    </div>
                  </div>
                  
                  <div className="text-center z-10">
                    <div className="w-10 h-10 bg-pink-100 rounded-full flex items-center justify-center mx-auto mb-1">
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-pink-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                      </svg>
                    </div>
                    <p className="text-xs text-gray-500">To</p>
                    <p className="font-bold text-lg text-pink-600">{formData.to}</p>
                  </div>
                </div>
                
                {/* Display the Average Fare */}
                <div className="mb-4 bg-gradient-to-r from-yellow-50 to-yellow-100 p-3 rounded-lg hover:shadow-md transition-all duration-300">
                  <p className="text-base font-semibold text-gray-700 flex justify-between items-center">
                    <span>Average Fare:</span> 
                    <span className="font-bold text-yellow-600 text-xl">${cheapestFlight.averageFare}</span>
                  </p>
                </div>
                
                {/* Display Cheapest Flight Details */}
                <div className="mb-4 bg-gradient-to-r from-blue-50 to-indigo-50 p-3 rounded-lg hover:shadow-md transition-all duration-300">
                  <p className="text-base font-semibold text-gray-700 flex justify-between items-center">
                    <span>Airline:</span> 
                    <span className="font-bold text-blue-600">{cheapestFlight.cheapestAirline}</span>
                  </p>
                </div>
                
                <div className="mb-4 bg-gradient-to-r from-green-50 to-emerald-50 p-3 rounded-lg hover:shadow-md transition-all duration-300">
                  <p className="text-base font-semibold text-gray-700 flex justify-between items-center">
                    <span>Fare:</span> 
                    <span className="font-bold text-green-600 text-xl">${cheapestFlight.cheapestFare}</span>
                  </p>
                </div>
                
                {/* Other information */}
                {formData.departDate && (
                  <div className="mb-4 bg-gradient-to-r from-purple-50 to-pink-50 p-3 rounded-lg hover:shadow-md transition-all duration-300">
                    <p className="text-base font-semibold text-gray-700 flex justify-between items-center">
                      <span>Date:</span> 
                      <span className="font-bold text-purple-600">{formData.departDate}</span>
                    </p>
                  </div>
                )}
                
                <div className="mb-4 bg-gradient-to-r from-amber-50 to-yellow-50 p-3 rounded-lg hover:shadow-md transition-all duration-300">
                  <p className="text-base font-semibold text-gray-700 flex justify-between items-center">
                    <span>Class:</span> 
                    <span className="font-bold text-amber-600">{formData.flightType}</span>
                  </p>
                </div>
                
                <div className="flex justify-center mt-6">
                  <button className="group relative inline-flex items-center justify-center px-6 py-2 overflow-hidden font-bold text-white rounded-full">
                    <span className="absolute inset-0 w-full h-full bg-gradient-to-br from-blue-600 to-indigo-600 transition-all duration-300 ease-out group-hover:from-indigo-600 group-hover:to-blue-600"></span>
                    <span className="absolute bottom-0 right-0 block w-64 h-64 mb-32 mr-4 transition duration-500 origin-bottom-left transform rotate-45 translate-x-24 bg-pink-500 opacity-30 group-hover:rotate-90 ease"></span>
                    <span className="relative flex items-center">
                      Book Now
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 ml-2 transform group-hover:translate-x-1 transition-transform duration-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
                      </svg>
                    </span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default TicketSearchPage;