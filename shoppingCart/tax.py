#!/usr/bin/python
# -*- encoding: utf-8 -*-
################################################################################
#
#    Copyright (C) 2010 - 2015 Dharmesh Patel <mr.dlpatel@gmail.com>.
#    Licence : BSD, see LICENSE for more details.
#
################################################################################

def calculate(amount, taxes, tax_type, currency_rate=1, price_accuracy=2):
    """
    :return: Tax amount according to currency rate.
    """
    total_tax = 0.0

    if tax_type == 'included':
        tax_percentage = sum([tax['amount'] for tax in taxes if tax['type'] == 'percentage'])

    for tax in taxes:        
        if tax['type'] == 'percentage':
            if tax_type == 'included':
                total_tax += round((float(amount) / (1 + (float(tax_percentage) / 100))) * (float(tax['amount']) / 100), price_accuracy)
            else:
                total_tax += round(float(amount) * (float(tax['amount']) / 100), price_accuracy)
        elif tax['type'] == 'fixed':
            total_tax+=round(float(tax['amount']) * currency_rate, price_accuracy)
            
    return round(total_tax, price_accuracy)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
