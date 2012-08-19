xtensions.py approach
=====================

The best place for use xadrpy extras, define your own plugins, tools is the xtension.py of your module.
This contains xadrpy or xadrpy module configuration.
The xadrpy autodiscover (when application started - before first request) traverses all xtensions.py if the package of xtensions.py in listed on INSTALLED_APPS.

Project level xtensions.py
--------------------------

You can define project level xtensions.py in your settings.

.. code-block:: python

	XTENSIONS = "<project_name>.xtensions"

Loading order
-------------
The applications order in INSTALLED_APPS gives the primary loading order. 
The autodiscover load project xtensions.py after load applications xtensions.py, so you can redefine, reset some values in that.
 

