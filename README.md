<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->


<!-- PROJECT LOGO -->
<br />
<div align="center">

<h3 align="center">MVP Greedy Bot</h3>

  <p align="center">
    An Etimo Diamonds Bot with Greedy Algoritm
    <br />
    <a href="https://github.com/ValentinoTriadi/Tubes1_MVP"><strong>Explore the docs »</strong></a>
    ·
    <a href="https://github.com/ValentinoTriadi/Tubes1_MVP/issues">Report Bug</a>
    <br/>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#Usage/Examples">Usage/Examples</a></li>
      </ul>
    </li>
    <li><a href="#Project-Status">Project Status</a></li>
    <li><a href="#Room-for-Improvement">Room for Improvement</a></li>
    <li><a href="#Acknowledgments">Acknowledgments</a></li>
  </ol>
</details>


## About The Project
The greedy algorithm used to solve the diamond game seeks the best local solution at each step. In each iteration, the algorithm selects the most advantageous diamond based on certain criteria, such as closest distance or the number of points it offers. Additionally, the algorithm leverages additional features within the game, such as red buttons and teleporters, to gain even greater advantages.

The main algorithm that we use is the DirectAttack algorithm located in the file game/logic/direct_attack.py
<br>
<br>
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

### Prerequisites
* <a href="https://nodejs.org/en">Node.js</a>
* Python Dependencies
  ```sh
  cd src/tubes1-IF2211-bot-starter-pack-1.0.1
  ```
  ```sh
  pip install -r requirement.txt
  ```
* <a href="https://www.docker.com/products/docker-desktop/">Docker dekstop</a>
* Yarn
  ```sh
  npm install --global yarn
  ```
* Game Engine

### Usage/Examples

1. <a href="https://github.com/valentinotriadi/Tubes1_MVP/releases/tag/v1">Download source code (.zip)</a>
2. Extract zip and open the file
3. Go to root directory
  ```sh
  cd tubes1-IF2110-bot-starter-pack-1.0.1
  ```
4. Install dependencies using pip
  ```sh
  pip install -r requirements.txt
  ```
5. Run bot
  For 1 bot:
  ```sh
  python main.py --logic DirectAttack --email=your_email@example.com --name=your_name --password=your_password --team etimo
  ```
  For running more than 1 bots:
  
  a. Edit run script in ```run-bots.bat``` or ```run-bots.sh```
  
  b. Run script in the terminal

  - Windows
  ```sh
  ./run-bots.bat
  ```
  - Linux / macOS
  ```sh
  ./run-bots.sh
  ```
  NOTE : email and name in the script must be different each other and never used before
<br/>
<br/>
 
<p align="right">(<a href="#readme-top">back to top</a>)</p>




<!-- PROJECT STATUS -->
## Project Status
Project status: _complete_ 
<br/>
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROOM FOR IMPROVEMENT -->
## Room for Improvement
Room for improvement:
- Improve speed of process
- Improve code's efficiency 
<br/>
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments
- [Maulvi Ziadinda Maulana](https://www.github.com/maulvi-zm)
- [Satriadhikara Panji Yudhistira](https://www.github.com/satriadhikara)
- [Valentino Chryslie Triadi](https://www.github.com/valentinotriadi)


<p align="right">(<a href="#readme-top">back to top</a>)</p>
