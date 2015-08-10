#!/usr/bin/python
# -*- encoding: utf-8 -*-
################################################################################
#
#    Copyright (C) 2010 - 2015 Dharmesh Patel <mr.dlpatel@gmail.com>.
#    Licence : BSD, see LICENSE for more details.
#
################################################################################

class Option(object):
    """
    Option Object.
    """

    def __init__(self, id, name, code=None, values=[]):
        """
        :param id: Unique Id.
        :param name: Option Name.
        :param code: Option Code.
        :param values: Option Values.
        """
        self.id = id
        self.name = name
        self.code = code
        self.values = values

    def add_value(self, *values):
        self.values.extend(values)

class OptionValue(object):
    """
    OptionValue Object.
    """

    def __init__(self, id, name, code=None, price=0.0):
        """
        :param id: Unique Id.
        :param name: Option Value Name.
        :param code: Option Value Code.
        :param price: Option Value Price.
        """    
        self.id = id
        self.name = name
        self.code = code
        self.price = price

class Product(object):
    """
    Product Object.
    """
    
    def __init__(self, id, name, code, price, options=[]):
        """
        :param id: Unique Id.
        :param name: Product Name.
        :param code: Prodcuct Code.
        :param price: Real Price of Product.
        """
        self.id = id
        self.code = code
        self.price = price
        self.name = name
        self.options = options

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
