# PV211 Utils


[![Continuous integration status][ci-badge]][ci]
[![Docker Hub badge][dockerhub-badge]][dockerhub]

 [ci-badge]: https://github.com/MIR-MU/pv211-utils/workflows/Test%20and%20publish/badge.svg
 [ci]: https://github.com/MIR-MU/pv211-utils/actions?query=workflow%3ATest%20and%20publish

 [dockerhub-badge]: https://img.shields.io/docker/pulls/miratmu/pv211-utils
 [dockerhub]: https://hub.docker.com/repository/docker/miratmu/pv211-utils

This is a Python library that provides an object-oriented interface for
Cranfield, TREC 6–8, ARQMath, and Beir collections. The library also provides an
object-oriented interface for building and evaluating information retrieval
search engines for these collections as a part of the [PV211: Introduction to
Information Retrieval][pv211] course taught at [the Faculty of Informatics,
Masaryk University, Brno, Czech Republic][fimu].

 [pv211]: https://is.muni.cz/predmet/fi/PV211?lang=en
 [fimu]: https://www.fi.muni.cz/index.html.en

Here are some examples of how you can use the PV211 Utils library:

- First Term Project: Cranfield Collection (23.24% MAP score)
  [![Open in Colab][colab-badge]][cranfield]
  [![Open in Jupyter Hub][jupyter-badge]][jupyter]

- Second Term Project: Beir CQADupStack Collection (21.96% MAP score)
  [![Open in Colab][colab-badge]][beir]
  [![Open in Jupyter Hub][jupyter-badge]][jupyter]

- Alternative Second Term Project: ARQMath Collection (6.62% MAP score)
  [![Open in Colab][colab-badge]][arqmath]
  [![Open in Jupyter Hub][jupyter-badge]][jupyter]

- Pre-2023 Second Term Project: TREC Collection (43.06% MAP score)
  [![Open in Colab][colab-badge]][trec]
  [![Open in Jupyter Hub][jupyter-badge]][jupyter]


 [colab-badge]: https://colab.research.google.com/assets/colab-badge.svg
 [jupyter-badge]: https://github.com/MIR-MU/pv211-utils/raw/main/jupyterhub-badge.svg

 [jupyter]: https://iirhub.cloud.e-infra.cz/
 [cranfield]: https://colab.research.google.com/github/MIR-MU/pv211-utils/blob/spring2025/notebooks/cranfield.ipynb
 [trec]: https://colab.research.google.com/github/MIR-MU/pv211-utils/blob/main/notebooks/trec.ipynb
 [arqmath]: https://colab.research.google.com/github/MIR-MU/pv211-utils/blob/main/notebooks/arqmath.ipynb
 [beir]: https://colab.research.google.com/github/MIR-MU/pv211-utils/blob/main/notebooks/beir_cqadupstack.ipynb
