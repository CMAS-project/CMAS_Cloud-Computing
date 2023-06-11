from flask import Flask, jsonify, request
import googlemaps

app = Flask(__name__)

API_KEY = 'AIzaSyChZ6SVW7w4pyTvnx7vNP36Q73tfhJxWGc'
gmaps = googlemaps.Client(key=API_KEY)

@app.route('/nearby_hospitals', methods=['GET'])
def get_nearby_hospitals():
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')

    try:
        # Membuat permintaan ke Google Places API untuk mendapatkan rumah sakit terdekat
        places_result = gmaps.places_nearby(
            location=(latitude, longitude),
            radius=5000,
            type='hospital'
        )

        hospitals = []
        for place in places_result['results']:
            hospital = {
                'name': place['name'],
                'latitude': place['geometry']['location']['lat'],
                'longitude': place['geometry']['location']['lng']
            }
            hospitals.append(hospital)

        return jsonify({'hospitals': hospitals})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
