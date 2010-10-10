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

def calculate(amount, taxes, tax_type, currency_rate=1, price_accuracy=2):
    """
    :return: Tax amount according to currency rate.
    """
    total_tax = 0.0

    if tax_type == 'tax_included':
        tax_percentage = sum([tax['amount'] for tax in taxes if tax['type'] == 'percentage'])

    for tax in taxes:        
        if tax['type'] == 'percentage':
            if tax_type == 'tax_included':
                total_tax += round((float(amount) / (1 + (float(tax_percentage) / 100))) * (float(tax['amount']) / 100), price_accuracy)
            else:
                total_tax += round(float(amount) * (float(tax['amount']) / 100), price_accuracy)
        elif tax['type'] == 'fixed':
            total_tax+=round(float(tax['amount']) * currency_rate, price_accuracy)
            
    return round(total_tax, price_accuracy)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
