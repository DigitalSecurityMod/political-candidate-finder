//Zipcode form event listener
document.getElementById("zipcode-form").addEventListener("submit", function(event) {
    event.preventDefault();

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

        //Get the officials from the data and build the table (if it doesn't exist)
        .then(data => {
            const officials = data.officials;
            
            for (let official of data.officials){
                var name = official.name;
                if (name == false){
                    name = "Not Available"
                };

                var party = official.party;
                if (party == false) {
                    party = "Not Available"
                };

                // Find or create the table
                let table = document.getElementById("officials-table");

                if (!table) {
                    // Clear the results div and create a table
                    const resultsDiv = document.getElementById("results");
                    resultsDiv.innerHTML = "";
                    table = document.createElement("table");
                    table.id = "officials-table";
                    table.className = "officials-table";
                    const headerRow = table.insertRow();
                    const nameHeader = headerRow.insertCell(0);
                    const partyHeader = headerRow.insertCell(1);
                    nameHeader.textContent = "Name";
                    partyHeader.textContent = "Party";
                    resultsDiv.appendChild(table);
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
}
);
