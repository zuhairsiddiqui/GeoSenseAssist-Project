<a id="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/zuhairsiddiqui/GeoSenseAssist-Project/blob/main/README.md">
    <img src="images/ReadMeLogo.png" alt="Logo" width="80" height="80">
  </a>

 <h3 align="center">README</h3>

# GeoSenseAssist-Project

<!-- ABOUT THE PROJECT -->
## **About**

[![Product Name Screen Shot][product-screenshot]](https://example.com)


* ### Unlike other applications that focus on identifying generic items, GeoSense Assist is specifically tailored to help students visualize geometric concepts.
* ### It provides text-to-speech descriptions, AI support, and geometric shape detection across devices.
* ### The goal is to help students gain a full understanding of shapes, equations, and graphs.


<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- Tech Stack -->
## **Our Tech Stack:**
Our main libraries and tools that we used:

[![Flask](https://img.shields.io/badge/Flask-4CAF50?logo=flask)](https://flask.palletsprojects.com/)
[![MySQL Connector](https://img.shields.io/badge/MySQL_Connector-005C84?logo=mysql)](https://dev.mysql.com/downloads/connector/python/)
[![NumPy](https://img.shields.io/badge/NumPy-6597AA?logo=numpy)](https://numpy.org/)
[![Python Dotenv](https://img.shields.io/badge/python--dotenv-gray)](https://pypi.org/project/python-dotenv/)
[![Pillow](https://img.shields.io/badge/Pillow-blueviolet?logo=python-imaging-library)](https://pillow.readthedocs.io/en/stable/)
[![Werkzeug](https://img.shields.io/badge/Werkzeug-black)](https://werkzeug.palletsprojects.com/)
[![Google Generative AI](https://img.shields.io/badge/Google_Generative_AI-blueviolet)](https://cloud.google.com/vertex-ai/docs/generative-ai)
[![gTTS](https://img.shields.io/badge/gTTS-orange)](https://pypi.org/project/gTTS/)
[![PyTest](https://img.shields.io/badge/PyTest-red?logo=pytest)](https://docs.pytest.org/en/stable/)
[![PyGame](https://img.shields.io/badge/PyGame-green?logo=pygame)](https://www.pygame.org/)



<p align="right">(<a href="#readme-top">back to top</a>)</p>


## **How to run GeoSense**

**step 1:**
dowload mySQL community
https://dev.mysql.com/downloads/installer/

for macOS you can use homebrew to install mySQL: https://brew.sh/ then once its installed run brew install mySQL in your terminal

**step 2:**
accept all default settings in mySQL, create your root username and password 

**step 3:**
Create a new user with credentials given in Github secrets. 

**step 4:**
 go to google ai studio and create gemini api key.

**step 5:**
create .env file, 
create variable called
API_KEY = insert api key here
HOST_NAME = insert hostname found in group chat here
USER_NAME = insert username found in group chat here
USER_PASSWORD = insert password found in group chat here
DATABASE_NAME = insert database name provided in group chat
(NOTE: do not place the variable data in quotations)

**step 6:**
paste api key, hostname, username, password, and database in .env
 
**step 7:**
run database.py

**step 8:**
run main.py

**step 9:**
use the automated URL link that contains your IP address




<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/zuhairsiddiqui/GeoSenseAssist-Project?style=for-the-badge
[contributors-url]: https://github.com/zuhairsiddiqui/GeoSenseAssist-Project/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/zuhairsiddiqui/GeoSenseAssist-Project?style=for-the-badge
[forks-url]: https://github.com/zuhairsiddiqui/GeoSenseAssist-Project/forks
[stars-shield]: https://img.shields.io/github/stars/zuhairsiddiqui/GeoSenseAssist-Project?style=for-the-badge
[stars-url]: https://github.com/zuhairsiddiqui/GeoSenseAssist-Project/stargazers
[issues-shield]: https://img.shields.io/github/issues/zuhairsiddiqui/GeoSenseAssist-Project?style=for-the-badge
[issues-url]: https://github.com/zuhairsiddiqui/GeoSenseAssist-Project/issues

[product-screenshot]: images/GeoSense.png