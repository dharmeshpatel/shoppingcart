#!/usr/bin/python
# -*- encoding: utf-8 -*-
################################################################################
#
#    Copyright (C) 2010 - 2015 Dharmesh Patel <mr.dlpatel@gmail.com>.
#    Licence : BSD, see LICENSE for more details.
#
################################################################################

from datetime import datetime

class DiscountCoupon(object):
    """
    DiscountCoupon Object.
    """

    def __init__(self, code, discount=0.0, type='amount', expiry_date=None, multi_usage=False):
        """            
        :param code: Unique code of the discount coupon.
        :param expiry_date: Expiry date of the discount coupon(FORMAT: %Y-%m-%d [%H[:%M[:%S]]]).
        :param type: Discount coupon type like 'amount' or 'percentage'(default amount).
        :param discount: Discount amount according to discount type.
        :param multi_usage: Multi usage(default False).
        """
        if expiry_date and not isinstance(expiry_date, datetime):
            try: # Hours, Minutes and Seconds are optional, so try converting hours, minutes and seconds first.
                expiry_date = datetime.strptime(expiry_date, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                try: # Try without seconds.
                    expiry_date = datetime.strptime(expiry_date, '%Y-%m-%d %H:%M')
                except ValueError:
                    try: # Try without minutes and seconds.
                        expiry_date = datetime.strptime(expiry_date, '%Y-%m-%d %H')
                    except ValueError:
                        try: # Try without hours, minutes and seconds.
                            expiry_date = datetime.strptime(expiry_date, '%Y-%m-%d')
                        except ValueError, error_message:
                            raise error_message
                
        if type not in ('percentage', 'amount'):
            raise ValueError('type field value must be `percentage` or `amount`', 'type')
            
        if not isinstance(discount, (int, float)):
            raise TypeError('discount field value must be integer or float type', 'discount')
            
        self.code = code
        self.__is_used = False
        self.discount = discount
        self.type = type
        self.expiry_date = expiry_date
        self.multi_usage = multi_usage

    def is_expired(self):
        """
        :return: True if coupon expired on today and False if its not expired.
        """
        if self.expiry_date and cmp(self.expiry_date, datetime.today()) is -1:
            return True
            
        return False

    def _get_is_used(self):
        """
        :return: True if coupon is already used and False if still not used.
        """
        return self.__is_used

    def _set_is_used(self, value):
        """
        To set "member:`is_used` property value.
        """
        self.__is_used = value

    is_used = property(_get_is_used, _set_is_used)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:    
