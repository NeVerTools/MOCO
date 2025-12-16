.. _installation:

Installation
------------

Docker
^^^^^^

In the root folder of the repository, pull the necessary docker image:

.. sybil-new-environment: IGNORE

.. code-block:: bash

    $ docker compose pull
    ...

Then verify that the correct versions are installed

.. code-block:: bash

    $ docker compose run --remove-orphans base
    [+] Creating 1/1
    ...

Local installation
^^^^^^^^^^^^^^^^^^

Requirements
````````````

The scripts have been tested with Python 3.10 and pip version 24.0.

You need to install ROS. We currently support the following distributions:

* `Humble <https://docs.ros.org/en/humble/index.html>`_
* `Jazzy <https://docs.ros.org/en/jazzy/index.html>`_

Don't forget to source ROS, e.g.:

.. sybil-new-environment: IGNORE

.. code-block:: bash

    $ source /opt/ros/humble/setup.bash
