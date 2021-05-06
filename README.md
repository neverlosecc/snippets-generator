[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![GPL-3.0 License][license-shield]][license-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/neverlosecc/snippets-generator">
    <img src="https://forum.neverlose.cc/uploads/default/original/1X/c7436ed0aebdb99328a52a65f2ece15a2c58a9be.png" alt="Logo" height="80">
  </a>

<h3 align="center">Neverlose.cc Lua API snippets generator</h3>
</p>



<!-- TABLE OF CONTENTS -->

## Table of Contents

* [Getting Started](#getting-started)
    * [Prerequisites](#prerequisites)
    * [Installation](#installation)
* [Usage](#usage)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)

<!-- GETTING STARTED -->

## Getting Started

### Prerequisites

First of all you need to install:

* python3

```sh
sudo apt-get install python3-pip
```

### Installation

1. Clone the repo

```sh
git clone https://github.com/neverlosecc/snippets-generator.git --recursive
```

2. Open cloned repo

```sh
cd snippets-generator
```

3. Install python libraries

```sh
sudo pip3 install -r requirements.txt
```

4. Enter your repo owner and repo name of documentation to config.json

```py3
{
    "owner": "YOUR_REPO_OWNER",
    "repo": "YOUR_REPO_NAME"
}
```

<!-- USAGE EXAMPLES -->

## Usage

1. Exit from project folder

```sh
cd ../
```

2. Run python project

```sh
python3 -m snippets-generator
```

3. Check out output.json

```sh
cd snippets-generator
cat output.json | tail
```

<!-- CONTRIBUTING -->

## Contributing

Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<!-- LICENSE -->

## License

Distributed under the GPL-3.0 License. See `LICENSE` for more information.



<!-- CONTACT -->

## Contact

Arsenii Esenin - me@es3n.in - es3n1n#3573

Project Link: [https://github.com/neverlosecc/snippets-generator](https://github.com/neverlosecc/snippets-generator)




<!-- MARKDOWN LINKS & IMAGES -->

[contributors-shield]: https://img.shields.io/github/contributors/neverlosecc/snippets-generator.svg?style=flat-square

[contributors-url]: https://github.com/neverlosecc/snippets-generator/graphs/contributors

[forks-shield]: https://img.shields.io/github/forks/neverlosecc/snippets-generator.svg?style=flat-square

[forks-url]: https://github.com/neverlosecc/snippets-generator/network/members

[stars-shield]: https://img.shields.io/github/stars/neverlosecc/snippets-generator.svg?style=flat-square

[stars-url]: https://github.com/neverlosecc/snippets-generator/stargazers

[issues-shield]: https://img.shields.io/github/issues/neverlosecc/snippets-generator.svg?style=flat-square

[issues-url]: https://github.com/neverlosecc/snippets-generator/issues

[license-shield]: https://img.shields.io/github/license/neverlosecc/snippets-generator.svg?style=flat-square

[license-url]: https://github.com/neverlosecc/snippets-generator/blob/master/LICENSE.txt