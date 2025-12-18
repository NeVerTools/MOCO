Tutorials
=========

This section provides two tutorials on how to use the MOCO tools to convert an autonomous robotic system into a model compatible with existing model checker tools (MOON and SCAn).
The RoaML models generated in the tutorials can be given to any model checker accepting SCXML as input format, but we recommend SCAn.

Prerequisites
-------------

You don't need to install MOCO locally on your machine. You can use the docker container, provided as a package on the `MOCO Github page <https://github.com/NeVerTools/MOCO/pkgs/container/moco>`_

Just pull the container and then run the following command in the root folder to start the docker in an interactive terminal such that you can then run all the commands in the tutorial inside the container.


.. sybil-new-environment: IGNORE

.. code-block:: bash

    $ docker pull ghcr.io/nevertools/moco:latest

.. code-block:: bash

    $ docker compose run --remove-orphans base

Should you wish to install MOCO locally, follow the description in the :ref:`installation guide <installation>`.

.. _full_tutorial:

What you will learn
-------------------

In this tutorial you will learn in about one hour how a robotic example can be expressed in RoaML with ROS and BT tools.
Then, you will use MOCO to translate the model into plain SCXML.
The example models a robot with a simple symbolic fetch and carry task.

We assume some background in computer science or as a robotics developer, but no knowledge about formal methods or model checking is required.


Tutorial 1: Battery Drainer
```````````````````````````

For this tutorial, we use the model defined here: `quick_start_battery_monitor <https://github.com/nevertools/moco/tree/main/examples/quick_start_battery_monitor>`_.
The model consists of a `main.xml` file, referencing the BT files running in the system and the SCXML files modeling the BT plugins, as well as the environment and the ROS nodes.

This example models a simple system with a battery that is continuously drained and, once it reaches a certain level, an alarm is triggered.
A behavior tree continuously monitors the alarm topic and, once it is triggered, recharges the battery to its full level before starting the draining process again.

The image below gives an overview of an exemplary system to be model-checked.

.. image:: graphics/scxml_tutorial_quick_start_battery_monitor.drawio.svg
    :width: 800
    :alt: An image of the complete exemplary system.

In this example, the system is composed by the following nodes modeled in ASCXML:

* a **Battery Drainer**, that at each time step drains the battery by 1%, and each time the charge trigger is received, it recharges the battery to 100%.
* a **Battery Manager**, that at each time the battery level is received checks if it is below 30% and, if so, triggers the alarm.

The **Behavior Tree** continuously checks the alarm topic and, once it is triggered, sends a charge trigger to the battery drainer.

In the `main.xml file <https://github.com/nevertools/moco/blob/main/examples/quick_start_battery_monitor/main.xml>`_ introduced earlier, the maximum run time of the system is specified with ``max_time`` and shared across the components. To make sure that the model-checked property makes sense, the allowed runtime needs to be high enough to have enough time to deplete the battery, i.e., in this example the maximal time needs to be at least 100s because the battery is depleted by 1% per second. Further information about this and other configuration parameters can be found in the :ref:`Available Parameters section <parameters>` of the :ref:`How-To page <howto>`.

In addition, in this main file, all the components of the example are put together, and the property to use is indicated.

Running the Script
`````````````````````

After installing the package as described in the :ref:`installation section <installation>`, a full system RoaML model can be converted into a model-checkable plain SCXML file as follows:

.. sybil-new-environment: quick_start_battery_monitor
    :cwd: .

.. code-block:: bash

    $ cd examples/quick_start_battery_monitor/ && \
      as2fm_roaml_to_jani main.xml

    MOCO - RoAML to SCXML.

    Loading model from main.xml.
    xml_file='./battery_drainer.ascxml'
    xml_file='./battery_manager.ascxml'
    xml_file='./bt_topic_condition.ascxml'
    xml_file='./bt_topic_action.ascxml'
    ...

The output is a folder (./output, unless otherwise specified) containing the plain SCXML files for the model.


Tutorial 2: Fetch & Carry Robot
-------------------------------

For this tutorial we use the model defined here: `tutorial_fetch_and_carry <https://github.com/nevertools/moco/tree/main/examples/tutorial_fetch_and_carry>`_.
A classical fetch and carry task is implemented there. A robot should drive to the pantry where food is stored, pick up snacks, drive to the table and place the snacks there. The robot should be done with this task after at most 100 seconds.

The model consists of a `main.xml <https://github.com/nevertools/moco/blob/main/examples/tutorial_fetch_and_carry/main.xml>`_ file, referencing the BT `bt_tree.xml <https://github.com/nevertools/moco/blob/main/examples/tutorial_fetch_and_carry/bt_tree.xml>`_ running in the system and the SCXML files modeling the BT plugins for navigating `bt_navigate_action.scxml <https://github.com/nevertools/moco/blob/main/examples/tutorial_fetch_and_carry/bt_navigate_action.scxml>`_, picking `bt_pick_action.scxml <https://github.com/nevertools/moco/blob/main/test/roaml_generator/_test_data/tutorial_fetch_and_carry/bt_pick_action.scxml>`__, and placing `bt_place_action.scxml <https://github.com/nevertools/moco/blob/main/examples/tutorial_fetch_and_carry/bt_place_action.scxml>`_, as well as the world model `world.scxml <https://github.com/nevertools/moco/blob/main/examples/tutorial_fetch_and_carry/world.scxml>`_.

All of those components are summarized and collected in the `main.xml <https://github.com/nevertools/moco/blob/main/examples/tutorial_fetch_and_carry/main.xml>`_ file.

For the rest of the tutorial it is assumed the container is running and you have navigated to the model's folder - mounted from the cloned repository:

.. code-block:: bash

    $ cd examples/tutorial_fetch_and_carry

* First, some parameters configuring generic properties of the system are defined. In this example we bound the maximum execution time to 100 seconds, and configure unbounded arrays to contain at most 10 elements.

    .. code-block:: xml

        <parameters>
            <max_time value="100" unit="s" />
            <max_array_size value="10" />
        </parameters>

* Afterwards the Behavior Tree is fully specified in terms of the BT in the BT.cpp XML format and the used BT plugins in ASCXML for navigating, picking, and placing. We will go into the details of the individual files later.

    .. code-block:: xml

        <behavior_tree>
            <input type="bt.cpp-xml" src="./bt_tree.xml" />
            <input type="bt-plugin-ascxml" src="./bt_navigate_action.scxml" />
            <input type="bt-plugin-ascxml" src="./bt_pick_action.scxml" />
            <input type="bt-plugin-ascxml" src="./bt_place_action.scxml" />
        </behavior_tree>

* In addition, the model of the environment, also known as world, is given in SCXML. We will go into the details of the environment model later.

    .. code-block:: xml

        <node_models>
            <input type="node-ascxml" src="./world.scxml" />
        </node_models>

The behavior tree specified in `bt_tree.xml <https://github.com/nevertools/moco/blob/main/examples/tutorial_fetch_and_carry/bt_tree.xml>`_ looks as depicted in the image below. The SequenceWithMemory node ticks each child in order until all of them have returned Success. Those who already returned Success are not ticked in the next cycle again.
The location is encoded as 0 = in the pantry and 1 = at the table. The snack object has id 0.

.. image:: graphics/scxml_tutorial_ros_fetch_and_carry_bt.drawio.svg
    :width: 600
    :alt: An image of the behavior tree of the fetch and carry example.

The next image depicts the behavior of the BT plugin `bt_navigate_action.scxml <https://github.com/nevertools/moco/blob/main/examples/tutorial_fetch_and_carry/bt_navigate_action.scxml>`_. It is used to navigate to a certain location given by the id, either 0 or 1 in this example, stored in `data`. When the BT is ticked it assigns `loc_id = data`. When the BT is halted or the action is aborted `tmp_result` is set to `false`, otherwise it is set to `true`. Based on that the return status of the tree is then published.

.. image:: graphics/scxml_tutorial_ros_fetch_and_carry_bt_navigate.drawio.png
    :width: 600
    :alt: An image of the BT navigate action plugin.

The next image depicts the behavior of the BT plugin `bt_pick_action.scxml <https://github.com/nevertools/moco/blob/main/examples/tutorial_fetch_and_carry/bt_pick_action.scxml>`_ in a very similar fashion. The action is used to pick a certain item with a given id, stored in `data`. When the BT is ticked it assigns `object_id = data`. When the BT is halted or the action is aborted `tmp_result` is set to `false`, otherwise it is set to `true`. Based on that the return status of the tree is then published.

.. image:: graphics/scxml_tutorial_ros_fetch_and_carry_bt_pick.drawio.png
    :width: 600
    :alt: An image of the BT pick action plugin.

The next image depicts the behavior of the BT plugin `bt_place_action.scxml <https://github.com/nevertools/moco/blob/main/examples/tutorial_fetch_and_carry/bt_place_action.scxml>`_. When called, the action just immediately tries to successfully execute, no matter if there is an object in the gripper or not, when the BT is ticked. When the BT is halted or the action is aborted `tmp_result` is set to `false`, otherwise it is set to `true`. Based on that the return status of the tree is then published.

.. image:: graphics/scxml_tutorial_ros_fetch_and_carry_bt_place.drawio.png
    :width: 600
    :alt: An image of the BT place action plugin.

As a last step, we take a closer look at the environment model in `world.scxml <https://github.com/nevertools/moco/blob/main/examples/tutorial_fetch_and_carry/world.scxml>`_.

* First, it is indicated that the model makes use of the interfaces from the `fetch_and_carry_msgs <https://github.com/nevertools/moco/tree/main/ros_support_interfaces/fetch_and_carry_msgs>`_ package, where custom ROS actions are defined. In line 21 the ROS topic publisher for the snack type is declared.

    .. code-block:: xml

        <ros_action_server name="act_nav" action_name="/go_to_goal" type="fetch_and_carry_msgs/Navigate" />
        <ros_action_server name="act_pick" action_name="/pick_object" type="fetch_and_carry_msgs/Pick" />
        <ros_action_server name="act_place" action_name="/place_object" type="fetch_and_carry_msgs/Place" />
        <ros_topic_publisher name="pub_snacks0" topic="/snacks0_loc" type="std_msgs/Int32" />

* The next block defines and initializes the variables used: An array of integers for the objects' locations, an integer for the robot's location, a flag indicating if the robot is holding something (-1 = no, otherwise the object's id), a variable saying where the object should be brought to, i.e., the `goal_id`, and two helper variables `req_obj_idx` and `req_loc_idx` for the id of the object which is requested to be picked up and the location to which the robot is requested to navigate to.

    .. code-block:: xml

        <datamodel>
            <data id="obj_locs" type="int32[1]" expr="[0]" />
            <data id="robot_loc" type="int32" expr="1" />
            <data id="robot_holding" type="int32" expr="-1" />
            <!-- Additional support variable for the goal_id -->
            <data id="goal_id" type="int32" expr="0" />
            <data id="req_obj_idx" type="int32" expr="0" />
            <data id="req_loc_idx" type="int32" expr="0" />
        </datamodel>

* The actual functionality of the world model is depicted in the graph below. When trying to navigate to a goal the location is first stored in the helper variable and from there the robot location is set to the goal location id.  For the moment, in this file it is assumed that this operation always succeeds. When trying to pick an object, the requested object's id is again stored in a helper variable. Afterwards, it is checked if the object's location is the same as the robot's location. It is recorded in the `robot_holding` variable that the robot now holds the object with a certain id. The location of the object is reset to -1 indicating that it is in the robot's gripper. This procedure can succeed or be aborted. In case an object should be placed, it is checked if the robot is holding an object (by `robot_holding != -1`). In this case the location of the object is replaced with the robot's location and `robot_holding` is set to -1 again because the gripper is empty now. This procedure can also be aborted if it does not succeed.

    .. image:: graphics/scxml_tutorial_ros_fetch_and_carry_world.drawio.png
        :width: 800
        :alt: An image of the world behavior of the fetch and carry example.



Model Translation with MOCO
---------------------------

You can translate this RoaML model in SCXML just as easily as the first one.
Assuming you are in the ``examples/tutorial_fetch_and_carry`` folder:

.. sybil-new-environment: first_model_checking
    :cwd: examples/tutorial_fetch_and_carry

.. code-block:: bash

    $ moco_roaml_to_scxml main.xml

    MOCO - RoAML to SCXML.

    Loading model from main.xml.
    xml_file='./world.ascxml'
    xml_file='./bt_navigate_action.ascxml'
    xml_file='./bt_pick_action.ascxml'
    xml_file='./bt_place_action.ascxml'
    ...

This produces an equivalent model in the plain `SCXML format <https://www.w3.org/TR/scxml/>`_ and saves it to the `./output` folder.
You may specify a different output folder with the `--generated-scxml-dir` argument.


Should you wish to learn more about RoaML, its' tags and their handling, check the :ref:`RoaML to SCXML conversion <_roaml_scxml_conversion>`.