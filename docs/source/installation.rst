.. _installation:

Installation
------------

Docker
^^^^^^

If you cloned the repository, pull the docker image from its' root folder:

.. sybil-new-environment: IGNORE

.. code-block:: bash

    $ docker compose pull
    ...

Or pull it directly from Github container registry:

.. code-block:: bash

    $ docker pull ghcr.io/nevertools/moco:latest
    ...


Then, run it with:

.. code-block:: bash

    $ docker compose run --remove-orphans base
    [+] Creating 1/1
    ...

Local installation
^^^^^^^^^^^^^^^^^^

Requirements
````````````

The scripts have been tested with Python 3.10 and pip version 24.0.

You will need to install ROS. We currently support the following distributions:

* `Humble <https://docs.ros.org/en/humble/index.html>`_
* `Jazzy <https://docs.ros.org/en/jazzy/index.html>`_

Once installed, be sure to source it (ie. via ``$ source /opt/ros/humble/setup.bash``)

 Then run the following command to build the workspace:

.. code-block:: bash

    $ docker compose build base
    ...

And run it with:

.. code-block:: bash

    $ docker compose run --remove-orphans base
    [+] Creating 1/1
    ...