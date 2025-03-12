//Zipcode form event listener
document.getElementById("zipcode-form").addEventListener("submit", function(event) {
    event.preventDefault();

    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = ""; // Clear previous results
    
    // Create a loading spinner
    const loadingSpinner = document.createElement("div");
    loadingSpinner.className = "loader";
    resultsDiv.appendChild(loadingSpinner);
    
    // Get the zipcode from the form
    const zipcode = document.getElementById("zipcode").value;

    // Fetch and display the data from the Google Civic API
    const url = "http://localhost:5000/representatives";

    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded" // Important for form data
        },
        body: new URLSearchParams({
            zip_code: zipcode // Send zipcode in the request body
        })
    })
        // Check if the response is OK, then return the JSON data
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })

        //Get the officials from the data and build the table
        .then(data => {
            const officials = data.officials;
            // Check if the officials array is empty
            if (!officials || officials.length === 0) {
                // If no officials are found, alert the user
                const resultsDiv = document.getElementById("results");
                resultsDiv.innerHTML = ""; // Clear previous results
                let noResultsMessage = document.createElement("p");
                noResultsMessage.textContent = "No officials found for this zipcode.";
                resultsDiv.appendChild(noResultsMessage);
                return;
            }
            
            // Create a new table
            let table = document.createElement("table");
            table.id = "officials-table";
            table.className = "officials-table";
            
            // Create the table header
            const headerRow = document.createElement("tr");                    
            const nameHeader = document.createElement("th");
            const partyHeader = document.createElement("th");
            nameHeader.textContent = "Name";
            partyHeader.textContent = "Party";
            headerRow.appendChild(nameHeader);
            headerRow.appendChild(partyHeader);
            
            // Append the header row to the table
            table.appendChild(headerRow);
            
            // Clear the loading spinner
            resultsDiv.innerHTML = "";

            // Add the table to the results div
            resultsDiv.appendChild(table);
            
            // Add officials to the table
            for (let official of data.officials){
                var name = official.name;
                if (name == false){
                    name = "Not Available"
                };

                var party = official.party;
                if (party == false) {
                    party = "Not Available"
                };

                // Add the current official to the table
                const row = table.insertRow();
                const nameCell = row.insertCell(0);
                const partyCell = row.insertCell(1);
                nameCell.textContent = name;
                partyCell.textContent = party;
            };
        })

        // Catch any errors and log them to the console
        .catch(error => {
            console.error('Error fetching data:',error);
        });
});
