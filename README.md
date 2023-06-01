# M25-napari

[![License](https://img.shields.io/pypi/l/m25-napari.svg?color=green)](https://github.com/SaraLab-Group/m25-napari/blob/main/LICENSE.md)
[![PyPI](https://img.shields.io/pypi/v/m25-napari.svg?color=green)](https://pypi.org/project/m25-napari)
[![Python Version](https://img.shields.io/pypi/pyversions/m25-napari.svg?color=green)](https://python.org)
[![tests](https://github.com/SaraLab-Group/m25-napari/workflows/tests/badge.svg)](https://github.com/SaraLab-Group/m25-napari/actions)
[![codecov](https://codecov.io/gh/SaraLab-Group/m25-napari/branch/main/graph/badge.svg)](https://codecov.io/gh/SaraLab-Group/m25-napari)
[![napari hub](https://img.shields.io/endpoint?url=https://api.napari-hub.org/shields/m25-napari)](https://napari-hub.org/plugins/m25-napari)
[![DOI](https://zenodo.org/badge/443224520.svg)](https://zenodo.org/badge/latestdoi/443224520)

## 🦠🔬 25 plane-camera array mutlifocus microscopy (M25) Controls and Image Visualization 
GUI for M25 control of 25 cameras for live-data visualization, control and acquisition. 

![m25-napari plugin and napari viewer with Celegans data](https://github.com/SaraLab-Group/m25-napari/blob/main/docs/image/m25-napari-plugin.png)

The GUI requires separate installation of the [M25 Acquisition engine](https://github.com/SaraLab-Group/M25_Acqusition_Engine) to communitcate with PSoC Timing Controller and cameras.

----------------------------------

This [napari] plugin was generated with [Cookiecutter] using [@napari]'s [cookiecutter-napari-plugin] template.

<!--
Don't miss the full getting started guide to set up your new package:
https://github.com/napari/cookiecutter-napari-plugin#getting-started

and review the napari docs for plugin developers:
https://napari.org/plugins/stable/index.html
-->

## Installation
This repository was tested with CUDA 11.2 and cuDNN 8.1 pre-installed on Windows 10. 
You can install `m25-napari` via [pip]:

    pip install m25-napari

To install latest development version :

    pip install git+https://github.com/SaraLab-Group/m25-napari.git


## Contributing

Contributions are very welcome. Tests can be run with [tox], please ensure
the coverage at least stays the same before you submit a pull request.

## License

Distributed under the terms of the [BSD-3] license,
"m25-napari" is free and open source software

## Issues

If you encounter any problems, please [file an issue] along with a detailed description.

[napari]: https://github.com/napari/napari
[Cookiecutter]: https://github.com/audreyr/cookiecutter
[@napari]: https://github.com/napari
[MIT]: http://opensource.org/licenses/MIT
[BSD-3]: http://opensource.org/licenses/BSD-3-Clause
[GNU GPL v3.0]: http://www.gnu.org/licenses/gpl-3.0.txt
[GNU LGPL v3.0]: http://www.gnu.org/licenses/lgpl-3.0.txt
[Apache Software License 2.0]: http://www.apache.org/licenses/LICENSE-2.0
[Mozilla Public License 2.0]: https://www.mozilla.org/media/MPL/2.0/index.txt
[cookiecutter-napari-plugin]: https://github.com/napari/cookiecutter-napari-plugin

[file an issue]: https://github.com/SaraLab-Group/m25-napari/issues

[napari]: https://github.com/napari/napari
[tox]: https://tox.readthedocs.io/en/latest/
[pip]: https://pypi.org/project/pip/
[PyPI]: https://pypi.org/
