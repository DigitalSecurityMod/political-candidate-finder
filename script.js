//broken. needs api key from server

const apiKey = 'abc123';

document.getElementById("zipcode-form").addEventListener("submit", function(event) {
    event.preventDefault();
    const zipcode = document.getElementById("zipcode").value;
    const url = `https://www.googleapis.com/civicinfo/v2/representatives?address=${zipcode}&key=${apiKey}`;
    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
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
                console.log(`Name: ${name}, Party: ${party}`);
            };
        })
        .catch(error => {
            console.error('Error fetching data:',error);
        });
}
);
