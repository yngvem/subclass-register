__author__ = "Yngve Mardal Moe"
__email__ = "yngve.m.moe@gmail.com"


import difflib
from functools import wraps


class NotInRegisterError(BaseException):
    pass


class SubclassRegister:
    """Creates a register instance used to register all subclasses of some base class.

    Use the `SubclassRegister.link` decorator to link a base class with
    the register.

    Examples
    --------
    We create the register as any other class and link it to a base class using
    the ``link_base`` decorator.

    >>> register = SubclassRegister('car')
    >>> @register.link_base
    ... class BaseCar:
    ...     pass
    >>> class SUV(BaseCar):
    ...     def __init__(self, num_seats):
    ...         self.num_seats = num_seats
    >>> class Sedan(BaseCar):
    ...     def __init__(self, num_seats):
    ...         self.num_seats = num_seats

    The ``available_classes`` attribute returns a tuple with the class-names in the register

    >>> register.available_classes
    ('SUV', 'Sedan')
    
    We can also ommit adding a class from the register, using the skip decorator.

    >>> @register.skip
    ... class SportsCar(BaseCar):
    ...     def __init__(self, horse_powers):
    ...         self.horse_powers = horse_powers

    We see thawt the ``SportsCar`` class is not added to the register.

    >>> register.available_classes
    ('SUV', 'Sedan')

    Indexing works as if the register was a dictionary

    >>> register['SUV']
    <class 'subclass_register.subclass_register.SUV'>

    We can also check if elements are in the register

    >>> 'SUV' in register
    True

    And delete them from the register

    >>> del register['SUV']
    >>> 'SUV' in register
    False
    >>> register.available_classes
    ('Sedan',)

    We can also manually add classes to the register

    >>> register['SUV'] = SUV
    >>> 'SUV' in register
    True
    >>> register.available_classes
    ('Sedan', 'SUV')

    But we can not overwrite already existing classes in the register

    >>> register['SUV'] = SUV
    Traceback (most recent call last):
      ...
    ValueError: Cannot register two classes with the same name

    If we use a name that is not in the register, we get an error and a list of the available classes sorted by similarity (using difflib)

    >>> register['sedan'] # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      ...
    NotInRegisterError: sedan is not a valid name for a car.
    Available cars are (in decreasing similarity):
       * Sedan
       * SUV

    Similarly, if we try to access a class that we skipped, we get the same error.

    >>> register['SportsCar'] # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      ...
    NotInRegisterError: SportsCar is not a valid name for a car.
    Available cars are (in decreasing similarity):
       * Sedan
       * SUV

    When we iterate over the register, we iterate over the class names

    >>> for car in register:
    ...     print(car)
    Sedan
    SUV

    We can also iterate over the register using dictionary-style methods

    >>> for car, Car in register.items():
    ...     print(car, Car)
    Sedan <class 'subclass_register.subclass_register.Sedan'>
    SUV <class 'subclass_register.subclass_register.SUV'>
    >>> for Car in register.keys():
    ...     print(Car)
    Sedan
    SUV
    >>> for Car in register.values():
    ...     print(Car)
    <class 'subclass_register.subclass_register.Sedan'>
    <class 'subclass_register.subclass_register.SUV'>
    """

    def __init__(self, class_type="class"):
        """Initiate a class register.

        Arguments
        ---------
        class_type : str
            The name of the classes we register, e.g. layer or model if used for neural networks.
            It is used for pretty error messages.
        """
        self.class_type = class_type
        self.linked_base = None
        self.register = {}

    def link_base(self, cls):
        """Link a base class to the register. Can be used as a decorator.
        """
        if self.linked:
            raise RuntimeError(
                "Cannot link the same register with two different base classes"
            )

        old_init_subclass = cls.__init_subclass__

        @classmethod
        @wraps(old_init_subclass)
        def init_subclass(cls_, *args, **kwargs):
            name = cls_.__name__
            if name in self.register:
                raise ValueError(
                    f"Cannot create two {self.class_type}s with the same name."
                )
            self[name] = cls_
            return old_init_subclass(*args, **kwargs)

        self.linked_base = cls
        cls.__init_subclass__ = init_subclass
        return cls

    def skip(self, cls):
        """Decorator used to signal that the class shouldn't be added to the register.
        """
        if not self.linked:
            raise RuntimeError(
                "The register must be linked to a base class before a subclass can be skipped."
            )
        if not issubclass(cls, self.linked_base):
            raise ValueError(
                f"{cls.__name__} is not a subclass of {self.linked_base.__name__}"
            )
        del self[cls.__name__]

        return cls

    @property
    def available_classes(self):
        """tuple[str]: Tuple of the classes in the register.
        """
        return tuple(self.register.keys())

    @property
    def linked(self):
        """bool: Whether the register is linked to a base class or not.
        """
        if self.linked_base is None:
            return False
        return True

    def items(self):
        """Iterate over class names and classes.
        """
        return self.register.items()

    def values(self):
        """Iterate over classes (not names)
        """
        return self.register.values()

    def keys(self):
        """Iterate over class names
        """
        return self.register.keys()

    def _get_items_by_similarity(self, class_name):
        def get_similarity(class_name_):
            return difflib.SequenceMatcher(
                None, class_name.lower(), class_name_.lower()
            ).ratio()

        return sorted(self.register.keys(), key=get_similarity, reverse=True)

    def _validate_class_in_register(self, class_name):
        if class_name not in self:
            traceback = f"{class_name} is not a valid name for a {self.class_type}."
            traceback = f"{traceback} \nAvailable {self.class_type}s are (in decreasing similarity):"

            sorted_items = self._get_items_by_similarity(class_name)
            for available in sorted_items:
                traceback = f"{traceback}\n   * {available}"

            raise NotInRegisterError(traceback)

    def __contains__(self, class_name):
        """Check if a class name is in the register.
        """
        return class_name in self.register

    def __iter__(self):
        """Iterate over class names.
        """
        return iter(self.register)

    def __getitem__(self, class_name):
        """Get a class from the register.
        """
        self._validate_class_in_register(class_name)
        return self.register[class_name]

    def __setitem__(self, name, class_name):
        """Add a new class to the register. It is impossible to change existing classes.
        """
        if name in self.register:
            raise ValueError(f"Cannot register two classes with the same name")
        self.register[name] = class_name

    def __delitem__(self, class_name):
        """Delete a class from the register.
        """
        self._validate_class_in_register(class_name)
        del self.register[class_name]


if __name__ == "__main__":
    register = SubclassRegister("car")

    @register.link_base
    class BaseCar:
        pass

    class SUV(BaseCar):
        def __init__(self, num_seats):
            self.num_seats = num_seats

    class Sedan(BaseCar):
        def __init__(self, num_seats):
            self.num_seats = num_seats

    @register.skip
    class ToyCar(BaseCar):
        def __init__(self, weight):
            self.weight = weight

    print(register.available_classes)
    print(register["SUV"])  # This works
    print(register["ToyCar"])  # This fails
