.. Subclass Register documentation master file, created by
   sphinx-quickstart on Fri Aug 16 08:47:27 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Subclass Register
=================

Motivation
----------

This library implements a simple class decorator that you can apply to a base class. This decorator then hooks into the way the decorated class is subclassed, adding all new subclasses to a dictionary whose keys are class names and values are the classes themselves.

The motivation for this project was to autogenerate deep learning models from pure JSON files, thus ensuring reproducibility of the results. I do, however, think that it is ideal for any kind of codebase where we want to generate safe code from configuration files.


Installation instructions
-------------------------

The subclass register can be installed with ``pip``:

.. code::

    pip install subclass-register

by cloning this repo and running ``setup.py``

.. code::

    git clone https://github.com/yngvem/subclass-register
    cd subclass-register
    python setup.py

or by simply downloading the ``src\subclass_register\subclass_register.py`` file and the ``LISENCE`` file into your project.

Documentation
-------------

.. autoclass:: subclass_register.SubclassRegister
    :members: __init__, link_base, skip, linked, available_classes, items, keys, values, __iter__, __getitem__, __setitem__, __delitem__, __contains__
