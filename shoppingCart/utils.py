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

def id_from_object(object):
    """
    :return: Id of object or object itself.
    """
    if not isinstance(object, (int, str)):
        object = getattr(object, 'id', object)

    return object

def get_dict_of_ids(object_dict):
    """
    :return: Dict of ids of object dict.
    """
    (keys, values) = ([], [])

    for key, value in object_dict.items():
        keys.append(id_from_object(key))
        if isinstance(value, dict):
            for k, v in value.items():
                values.append({id_from_object(k): v})
        else:
            values.append(id_from_object(value))
            
    return dict(zip(keys, values))

def get_list_of_ids(object_list):
    """
    :return: List of ids of object list.
    """
    return [id_from_object(value) for value in object_list]
            
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
