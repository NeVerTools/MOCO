.. _installation:

Installation
------------

Docker
^^^^^^

In the root folder of the repository, pull the necessary docker image:

.. sybil-new-environment: IGNORE

.. code-block:: bash

    $ docker compose pull moco:latest
    ...

Then run it with:

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

Once installed, source it:

.. sybil-new-environment: IGNORE

.. code-block:: bash

    $ source /opt/ros/humble/setup.bash

 Then run the following command to build the workspace:
 .. code-block:: bash
    $ sudo docker compose build base

    (compiling output...)

And you can now run it with:
 .. code-block:: bash
    $ sudo docker compose run --remove-orphans base
    [+] Creating 1/1
    ...