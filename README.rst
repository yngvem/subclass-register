Subclass Register
=================

.. image:: https://readthedocs.org/projects/subclass-register/badge/?version=latest
:target: https://subclass-register.readthedocs.io/en/latest/?badge=latest
:alt: Documentation Status
      

Motivation
----------

This library implements a simple clas decorator that you can apply to a base class. This decorator then hooks into the way the decorated class is subclassed, adding all new subclasses to a dictionary whose keys are class names and values are the classes themselves.

The motivation for this project was to autogenerate deep learning models from pure JSON files, thus ensuring reproducibility of the results. I do, however, think that it is ideal for any kind of codebase where we want to generate safe code from configuration files.


Installation instructions
-------------------------

The subclass register can be installed with ``pip``:

.. code::

    pip install subclass-register

by cloning this repo and running ``setup.py``

.. code::

    git clone https:\\github.com\yngvem\subclass-register
    cd subclass-register
    python setup.py

or by simply downloading the ``src\subclass_register\subclass_register.py`` file and the ``LISENCE`` file into your project.

Example
-------

Here is a basic example of how to use the subclass register.

.. code:: python

    from subclass_register import SubclassRegister

    
    register = SubclassRegister('car')

    @register.link_base
    class BaseCar:
        pass
    
    class SUV(BaseCar):
        def __init__(self, horse_powers):
            self.horse_powers = horse_powers
    
    suv = register['SUV'](horse_powers = 50)


