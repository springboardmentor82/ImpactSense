
// GLOBAL VARIABLES

let userLat = null;
let userLon = null;

// 📍 GET LOCATION FUNCTION

function getLocation(){
    if(navigator.geolocation){
        document.getElementById("result").innerText = "Fetching location...";
        navigator.geolocation.getCurrentPosition(showPosition);
    } else {
        alert("Geolocation not supported");
    }
}

function showPosition(position){
    userLat = position.coords.latitude;
    userLon = position.coords.longitude;

    fetch(`https://nominatim.openstreetmap.org/reverse?lat=${userLat}&lon=${userLon}&format=json`)
    .then(response => response.json())
    .then(data => {

        let address = data.address;

        // ✅ Better city detection
        let city = address.city || address.town || address.village || address.state_district || address.state || "Unknown";
        let country = address.country || "";

        document.getElementById("result").innerText =
            "📍 Location: " + city + ", " + country;

    })
    .catch(() => {
        // fallback
        document.getElementById("result").innerText =
            "📍 Location: " + userLat.toFixed(2) + ", " + userLon.toFixed(2);
    });
}
//PREDICTION FUNCTION

function predictImpact(){

    console.log("Clicked");

    let magnitude = parseFloat(document.getElementById("magnitude").value);
    let depth = parseFloat(document.getElementById("depth").value);
    let mmi = parseFloat(document.getElementById("mmi").value);
    let cdi = parseFloat(document.getElementById("cdi").value);
    let sig = parseFloat(document.getElementById("sig").value);

    if(magnitude && depth && mmi && cdi && sig){

        let resultText = "";
        let color = "";

        //LOCATION BONUS (SMART LOGIC)
        let locationBonus = 0;

        if(userLat !== null){
            if(userLat > 8 && userLat < 35){
                locationBonus = 0.5;
            }
        }

        let finalMagnitude = magnitude + locationBonus;

        //IMPACT LOGIC
        if(finalMagnitude < 4){
            resultText = "Low Impact (Safe Zone)";
            color = "#2ecc71";
        }
        else if(finalMagnitude < 6){
            resultText = "Moderate Impact (Warning Zone)";
            color = "#f1c40f";
        }
        else{
            resultText = "High Impact (Danger Zone)";
            color = "#e74c3c";
        }

        let result = document.getElementById("result");

        result.innerText = resultText;
        result.style.background = color;
        result.style.color = "black";

    } else {
        document.getElementById("result").innerText = "Enter all values";
    }
}