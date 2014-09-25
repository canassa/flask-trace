Flask Trace
===========

A Simple logging decorator for Flask applications

Usage
-----

Simply import the trace decorator and apply it to any function you want to log.

.. code-block:: python

    from flask_trace import trace

    @trace
    def my_awesome_function(arg1, arg2):
        pass


Now, any call to the my_awesome_function will be logged like this::

    TRACE: trace_uuid=44f64962-3468-4273-bcd7-1c2067faacdf func_name=my_awesome_function arg1=1 arg2=2
