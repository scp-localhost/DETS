<p align="center">
  <a href="http://192.168.0.15/scp-localhost/honeyPig">
    <img src="images/logo.png" alt="Logo" width="600" height="300">
  </a>
  <h3 align="center">honeyPig</h3>
  <p align="center">
    Low interaction listener and port scan logger...visualization and web reporting (and management)
    <br />
    <a href="http://192.168.0.15/scp-localhost/honeyPig"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="http://192.168.0.15/scp-localhost/honeyPig">View Demo</a>
    ·
    <a href="http://192.168.0.15/scp-localhost/honeyPig/issues">Report Bug</a>
    ·
    <a href="http://192.168.0.15/scp-localhost/honeyPig/issues">Request Feature</a>
  </p>
</p>
<!-- ToC -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About honeyPig...</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>
<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](http://192.168.0.15/scp-localhost/honeyPig)

...Why

### Built With

* [Bootstrap](https://getbootstrap.com)
* [JQuery](https://jquery.com)
* [Python](https://www.python.org/)
* [Flask](https://flask.palletsprojects.com/en/1.1.x/)
* [Rick](https://youtu.be/dQw4w9WgXcQ)


<!-- GETTING STARTED -->
## Getting Started

HoneyPig is meant to run with minimal effort and resources.
It is written mostly in Python3 and should run in ~Debian like environments without fuss.:smile:

Each instance of honeyPig can be set to listen to only one port or they can be ~spawned
to look for their own place in the list.
It will bootstrap its own db but needs a data dir in PWD (this is for your own good!)

### Prerequisites

Python3 assumed?

* sqlite3
  ```sh
  sudo apt-get install sqlite3
  ```
* missing module
  ```sh
  sudo python3 -m pip install [whatever]
  ```

### Installation

1. Python, Firewall allows for listen ports. 
2. Clone the repo
   ```sh
   git clone http://192.168.0.15/scp-localhost/honeyPig.git
   ```
3. Install sqlite packages
   ```sh
   sudo apt-get install sqlite3
  ```
4. Edit JS? `config.js`
   ```JS
   alert('the world needs lerts!');
   ```

<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_



<!-- ROADMAP -->
## Roadmap

See the [open issues](http://192.168.0.15/scp-localhost/honeyPig/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

scp - [@scp15487477](https://twitter.com/scp15487477) - steve.pote@protonmail.com

[![LinkedIn][linkedin-shield]][linkedin-url]

Project Link: [http://192.168.0.15/scp-localhost/honeyPig](http://192.168.0.15/scp-localhost/honeyPig)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
* [??](https://www.google.com/)


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://img.shields.io/static/v1?label=<LABEL>&message=<MESSAGE>&color=<COLOR> -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/steve-pote/
[product-screenshot]: images/screenshot.png