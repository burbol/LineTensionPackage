# Steps for analysing trajectory files created with GROMACS (version 5 or above. For earlier versions skip the first steps)

Trajectory files of simulations of water nanodroplets on top of stiff SAM surface. Analysis determines contact angle between water and solid.

## Create density profiles

To create the density profiles run "g_rad_grompi_v2.sh". This program uses a modified GROMACS (version 4) program called "g_rad_density".
To run "g_rad_grompi_v2.sh":
1. First modify "include" commands of .top files to the format of GROMACS version 4 (Run "change_top_files.sh")
2. Run "g_rad_grompi_v2.sh to create radial and planar density profiles (from the planar profiles two types are created, one using mass density and the other one using number density).


### Prerequisites

What things you need to install the software and how to install them

```
Give examples
```

### Installing

A step by step series of examples that tell you have to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone who's code was used
* Inspiration
* etc


