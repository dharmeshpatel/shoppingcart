#!/usr/bin/python
# -*- encoding: utf-8 -*-
################################################################################
#
#    Copyright (C) 2010 - 2015 Dharmesh Patel <mr.dlpatel@gmail.com>.
#    Licence : BSD, see LICENSE for more details.
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
