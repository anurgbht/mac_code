let originMap;
let destinationMap;
let originMarker;
let destinationMarker;

const API_KEY = "AIzaSyB-eiaxb0wClN178akMm4xTb7yAOOG14J8";


function initMap() {
    // Initialize the origin and destination maps
    destinationMap = new google.maps.Map(document.getElementById('destination-map'), {
        center: { lat: 34.0522, lng: -118.2437 }, // Default to Los Angeles, CA
        zoom: 10
    });

    destinationMarker = new google.maps.Marker({
        position: { lat: 34.0522, lng: -118.2437 },
        map: destinationMap,
        draggable: true
    });

    // Update the origin and destination input fields when markers are dragged
    destinationMarker.addListener('dragend', updateLocation);
}

function updateLocation() {
    var points = [];
    var drivingTimes = [];

    const destinationLat = destinationMarker.getPosition().lat();
    const destinationLng = destinationMarker.getPosition().lng();

    // Update input fields with the new coordinates
    console.log(`${destinationLat}, ${destinationLng}`);
    document.getElementById('destination').value = `${destinationLat}, ${destinationLng}`;
    points = calculatePointsAroundDestination(4, 10);
    drivingTimes = calculateDrivingTimes(destinationMarker.getPosition(), points);
    console.log(drivingTimes);
}

// Load the Maps JavaScript API with your API key
function loadMaps() {
    const API_KEY = "AIzaSyB-eiaxb0wClN178akMm4xTb7yAOOG14J8";
    const script = document.createElement('script');
    script.src = `https://maps.googleapis.com/maps/api/js?key=${API_KEY}&libraries=places&callback=initMap`;
    script.defer = true;
    script.async = true;
    document.body.appendChild(script);
}


// Function to calculate driving time from the destination to a list of points
async function calculateDrivingTimes(destination, points) {
    const drivingTimes = [];

    for (const point of points) {
        const origin = `${point.lat()},${point.lng()}`;
        const destinationStr = `${destination.lat()},${destination.lng()}`;
        const url = `https://maps.googleapis.com/maps/api/directions/json?origin=${origin}&destination=${destinationStr}&key=${API_KEY}`;

        console.log(`origin: ${origin}`);
        console.log(`destination: ${destination}`);
        console.log(url);

        const response = await fetch(url);
        console.log(response);
        // const data = response.json();

        // if (data.status === 'OK') {
        //     const duration = data.routes[0].legs[0].duration.text;
        //     drivingTimes.push({ point, duration });
        //     console.log(drivingTimes);
        // } else {
        //     console.error('Error: Unable to calculate driving time for point', point);
        // }

    }

    return drivingTimes;
}


function calculatePointsAroundDestination(numberOfPoints, radiusInKiloMeters) {
    var radiusInMeters = 1000 * radiusInKiloMeters;
    const points = [];
    const destinationLatLng = destinationMarker.getPosition();

    for (let i = 0; i < numberOfPoints; i++) {
        const angle = (360 / numberOfPoints) * i;
        const x = radiusInMeters * Math.cos(angle * (Math.PI / 180));
        const y = radiusInMeters * Math.sin(angle * (Math.PI / 180));

        const newPoint = new google.maps.LatLng(
            destinationLatLng.lat() + y / 111325,
            destinationLatLng.lng() + x / (111325 * Math.cos(destinationLatLng.lat()))
        );

        points.push(newPoint);
    }
    console.log(points);
    return points;
}


loadMaps();
