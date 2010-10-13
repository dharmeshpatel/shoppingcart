#!/usr/bin/python
# -*- encoding: utf-8 -*-
################################################################################
#
#    Copyright (C) 2010 Dharmesh Patel <mr.dlpatel@gmail.com>.
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
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
