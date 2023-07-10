from enum import Enum

"""
I thought I would put this in its own file but looks
like it takes a bit of work to set up that folder structure that I 
don't feel like doing right now
"""

class Operation_Types(Enum):
    UPDATE = 'u'
    DELETE = 'd'
    INSERT = 't'