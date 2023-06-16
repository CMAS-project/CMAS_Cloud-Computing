<h1 align="center">
  <img align="center" src="https://github.com/CMAS-project/CMAS_MobileAPP/blob/master/app/src/main/res/drawable/cmas_logo_tok.png"  width="500"></img>
<br>
CMAS CLOUD COMPUTING
</h1>

# Team Profile

### Team ID : C23-PC687

### This is our Members

* (ML) M038DSX0099 - Geraldo Enrico Semen - Institut Teknologi Sepuluh Nopember
* (ML) M340DSY3302 - Gemala Gita Prameswari - Universitas Sebelas Maret
* (ML) M168DSX3690 -  Rendy Ilhamsyah - Universitas Esa Unggul
* (CC) C151DKX3986 - Alif Wahyu Widi Adrian - Universitas Brawijaya
* (CC) C172DKY4104 - Septiyani Nadia Astuti - Universitas Gunadarma
* (MD) A161DKX3846 - Ardena Afif Pratama - Universitas Darussalam Gontor

# CMAS Cloud Computing Project
Our final project for Google Bangkit Academy 2023 revolves around mobile development. It serves as the culmination of our learning and skills acquired during the program.

**Machine Learning:**
[CMAS Machine Learning Apps Development](https://github.com/CMAS-project/CMAS_Machinelearning)

**Mobile Development:**
[CMAS Mobile Development](https://github.com/CMAS-project/CMAS_MobileAPP)

# CMAS Application Endpoints

This repository contains the endpoint implementations to support the features of the CMAS application. The application consists of four endpoints: Chatbot, Emotion Scan, Mental Health Articles, and Nearest Hospitals. Two endpoints, Chatbot and Emotion Scan, utilize machine learning models developed by the team and deployed alongside the other two endpoints, which rely on third-party APIs: News API and Google Maps API.

## Endpoints

The CMAS application features the following endpoints:

1. **Chatbot Endpoint**: This endpoint handles user interactions and provides conversational support. It utilizes a machine learning model developed by the team to generate responses based on user input.

2. **Emotion Scan Endpoint**: This endpoint allows users to analyze their emotions by submitting an image. The endpoint employs a machine learning model developed by the team to recognize emotions from the provided images. The images captured by the Emotion Scan feature are stored in Cloud Storage.

3. **Mental Health Articles Endpoint**: This endpoint retrieves articles related to mental health from the News API. Users can access informative articles, tips, and resources to support their mental well-being.

4. **Nearest Hospitals Endpoint**: This endpoint leverages the Google Maps API to find and display the nearest hospitals based on the user's location. It provides users with essential information such as hospital names, addresses, and contact details.

## Deployment

The endpoints are deployed using App Engine, a fully managed serverless platform provided by Google Cloud. App Engine offers scalability, automatic load balancing, and effortless scaling for web applications.

Additionally, Cloud Storage is utilized as the storage solution for images captured through the Emotion Scan feature. Cloud Storage provides a reliable and scalable storage infrastructure for the application.

## Getting Started

To run the CMAS application locally or deploy it to the cloud, follow these steps:

1. Clone this repository to your local machine.

2. Install the required dependencies.

3. Configure the necessary API credentials.
- Obtain the API key for the News API and add it to the configuration.
- Ensure you have access to the Google Maps API and add the API key to the configuration.

4. Update the configuration file with the API credentials and other relevant settings.

5. Run the application locally or deploy it to App Engine.

For detailed instructions on running and deploying the CMAS application, refer to the documentation.
