# PSG Admin panel (Demo)

![PSG Admin panel logo](/images/gateway-packing-stationAdmin-dark.svg)

![PSG Admin panel screenshot](/images/gateway-packing-stationAdmin%20presentation.png)

This is a PSG admin panel (Demo) for managing PSG-API. It is built using React and CoreUI components, and it uses Vite for building and serving the application. :3

This project should be use with [PSG](https://github.com/beam7894123/gateway-packing-station) & [PSG-API](https://github.com/beam7894123/gateway-packing-station/tree/api).



## Installation

1. Clone the repository

2. Navigate to the project directory and install the dependencies:
    ``` bash
    $ npm install
    ```

    or

    ``` bash
    $ yarn install
    ```

3. Set the environment variables by creating a `.env` file in the root directory of the project. The `.env.example` file contains the list of environment variables that need to be set.

## Basic usage

``` bash
# dev server with hot reload at http://localhost:3030
$ npm start 
```

or 

``` bash
# dev server with hot reload at http://localhost:3030
$ yarn start
```

Navigate to [http://localhost:3030](http://localhost:3030). The app will automatically reload if you change any of the source files.

## Build

Run `build` to build the project. The build artifacts will be stored in the `build/` directory.

```bash
# build for production with minification
$ npm run build
```

or

```bash
# build for production with minification
$ yarn build
```

## For Docker

To build and run the application using Docker, follow these steps:

1. Edit the `.env` file to set the environment variable

2. Run the Docker container:

    ```bash
    docker compose up
    ```



## Creators

**BezaTheCat**

* <https://bezathecat.com>


## CoreUI Creators

**Łukasz Holeczek**

* <https://twitter.com/lukaszholeczek>
* <https://github.com/mrholek>

**Andrzej Kopański**

* <https://github.com/xidedix>

**CoreUI Team**

* <https://twitter.com/core_ui>
* <https://github.com/coreui>
* <https://github.com/orgs/coreui/people>

## Support CoreUI Development

CoreUI is an MIT-licensed open source project and is completely free to use. However, the amount of effort needed to maintain and develop new features for the project is not sustainable without proper financial backing. You can support development by buying the [CoreUI PRO](https://coreui.io/pricing/?framework=react&src=github-coreui-free-react-admin-template) or by becoming a sponsor via [Open Collective](https://opencollective.com/coreui/).

## Copyright and License

copyright 2025 BezaTheCat & CreativeLabs
Code released under [the MIT license](/LICENSE).