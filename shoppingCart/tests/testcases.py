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

import datetime
import unittest

from shoppingCart.tests.product import Product, Option, OptionValue
from shoppingCart.tests.discount_coupon import DiscountCoupon
from shoppingCart import Cart

class CartTestCase(unittest.TestCase):

    def test_add_update_remove_find_item(self):
        cart_obj = Cart()
        self.assertEqual(cart_obj.is_empty, True)
        self.assertEqual(cart_obj.count(), 0)
#        self.assertRaises(ValueError, cart_obj.add_item(product=1, quantity=1))
        cart_obj.add_item(product=1, price=10.00, quantity=1)
        cart_obj.add_item(product=2, price=12.25, quantity=2.5)
        self.assertEqual(cart_obj.is_empty, False)
        self.assertEqual(cart_obj.count(), 3.5)
        self.assertEqual([{'price': item.price, 'options': item.get_options(), 'product': item.product, 'quantity': item.quantity} for item in cart_obj.get_items()], [{'price': 10.0, 'options': {}, 'product': 1, 'quantity': 1}, {'price': 12.25, 'options': {}, 'product': 2, 'quantity': 2.5}])
        cart_obj.add_item(product=1, quantity=1)
        self.assertEqual([{'price': item.price, 'options': item.get_options(), 'product': item.product, 'quantity': item.quantity} for item in cart_obj.get_items()], [{'price': 10.0, 'options': {}, 'product': 1, 'quantity': 2}, {'price': 12.25, 'options': {}, 'product': 2, 'quantity': 2.5}])
        cart_obj.update_item(product=1, quantity=3)
        self.assertEqual([{'price': item.price, 'options': item.get_options(), 'product': item.product, 'quantity': item.quantity} for item in cart_obj.get_items()], [{'price': 10.0, 'options': {}, 'product': 1, 'quantity': 3}, {'price': 12.25, 'options': {}, 'product': 2, 'quantity': 2.5}])
        cart_obj.remove_item(product=1)
        self.assertEqual([{'price': item.price, 'options': item.get_options(), 'product': item.product, 'quantity': item.quantity} for item in cart_obj.get_items()], [{'price': 12.25, 'options': {}, 'product': 2, 'quantity': 2.5}])
        self.assertEqual(cart_obj.find_item(1), None)
        self.assertEqual([{'price': item.price, 'options': item.get_options(), 'product': item.product, 'quantity': item.quantity} for item in [cart_obj.find_item(2)]], [{'price': 12.25, 'options': {}, 'product': 2, 'quantity': 2.5}])
        self.assertEqual(cart_obj.count(), 2.5)
        cart_obj.clear()
        self.assertEqual(cart_obj.get_items(), [])
    
    def test_add_update_remove_options(self):
        cart_obj = Cart()
        self.assertEqual(cart_obj.is_empty, True)
        self.assertEqual(cart_obj.count(), 0)
        cart_obj.add_item(product=1, price=10.00, quantity=1, taxes=[{'amount':19.6, 'type': 'percentage'}, {'amount':2.1, 'type': 'fixed'}])
        cart_obj.add_item(product=2, price=12.25, quantity=2.5, options={'color': {'red': {'price': 10.00}}})
        self.assertEqual([{'product': item.product, 'quantity': item.quantity, 'price': item.price, 'options': item.get_options()} for item in cart_obj.get_items()], [{'product': 1, 'options': {}, 'price': 10.0, 'quantity': 1}, {'product': 2, 'options': {'color': {'red': {'price': 10.0}}}, 'price': 12.25, 'quantity': 2.5}])
        self.assertEqual(cart_obj.count(), 3.5)
        self.assertEqual('%s %s'%(cart_obj.sub_total(), cart_obj.currency_symbol), '65.63 €')
        self.assertEqual('%s %s'%(cart_obj.total_untaxed_amount(), cart_obj.currency_symbol), '65.63 €')
        self.assertEqual('%s %s'%(cart_obj.total_tax(), cart_obj.currency_symbol), '4.06 €')
        self.assertEqual('%s %s'%(cart_obj.total(), cart_obj.currency_symbol), '69.69 €')
                            
    def test_apply_remove_discount(self):
        cart_obj = Cart()
        self.assertEqual(cart_obj.is_discount_applied, False)
        discount_coupon = DiscountCoupon(code='ByQ343X', expiry_date='2010-11-30 12:00:00', type='percentage', discount=30)
        self.assertEqual(cart_obj.add_discount(discount_coupon.discount, discount_coupon.type), True)
        discount_coupon = DiscountCoupon(code='Ax9812Y', expiry_date='2010-12-31 12:00', type='percentage', discount=30)
        self.assertEqual(cart_obj.add_discount(discount_coupon.discount, discount_coupon.type), True)
        self.assertEqual(cart_obj.is_discount_applied, True)
        self.assertEqual([discount for discount in cart_obj.get_discounts()], [{'amount': 30, 'type': 'percentage'}, {'amount': 30, 'type': 'percentage'}])

    def test_apply_remove_tax(self):
        cart_obj = Cart()
        self.assertEqual(cart_obj.add_tax(19.6, type='percentage'), True)
        self.assertEqual(cart_obj.add_tax(20.1, type='fixed'), True)
        self.assertEqual(cart_obj.add_tax(19.6, type='percentage'), False)
        self.assertEqual(cart_obj.get_taxes(), [{'amount': 19.600000000000001, 'type': 'percentage'}, {'amount': 20.100000000000001, 'type': 'fixed'}])
        self.assertEqual(cart_obj.remove_tax(10), False)
        self.assertEqual(cart_obj.remove_tax(20.1, type='fixed'), True)
        self.assertEqual(cart_obj.get_taxes(), [{'amount': 19.600000000000001, 'type': 'percentage'}])
        
    def test_discount_amount(self):
        discount_coupon = DiscountCoupon(code='Ax9812Y', expiry_date='2010-12-31 12:00', type='percentage', discount=30)
        cart_obj = Cart()
        cart_obj.currency_rate = 1
        cart_obj.price_accuracy = 2
        cart_obj.currency_symbol = '€'
        cart_obj.currency_code = 'EUR' 
        cart_obj.add_item(product=1, price=10.00, quantity=1)
        cart_obj.add_item(product=2, price=12.25, quantity=2.5)
        self.assertEqual('%s %s'%(cart_obj.sub_total(), cart_obj.currency_symbol), '40.63 €')
        cart_obj.add_discount(discount_coupon.discount, discount_coupon.type)
        self.assertEqual('%s %s'%(cart_obj.total_discount(), cart_obj.currency_symbol), '12.19 €')

    def test_sub_total(self):
        cart_obj = Cart()
        cart_obj.currency_rate = 1
        cart_obj.price_accuracy = 2
        cart_obj.currency_symbol = '€'
        cart_obj.currency_code = 'EUR'
        cart_obj.add_item(product=1, price=10.00, quantity=1)
        cart_obj.add_item(product=2, price=12.25, quantity=2.5)
        self.assertEqual('%s %s'%(cart_obj.sub_total(), cart_obj.currency_symbol), '40.63 €')
        cart_obj.currency_rate = 1.2714
        cart_obj.price_accuracy = 2
        cart_obj.currency_symbol = '$'
        cart_obj.currency_code = 'USD'
        self.assertEqual('%s%s'%(cart_obj.currency_symbol, cart_obj.sub_total()), '$51.63')

    def test_total_taxed_amount(self):
        cart_obj = Cart()
        cart_obj.currency_rate = 1
        cart_obj.price_accuracy = 2
        cart_obj.currency_symbol = '€'
        cart_obj.currency_code = 'EUR'
        cart_obj.add_item(product=1, price=10.00, quantity=1)
        cart_obj.add_item(product=2, price=12.25, quantity=2.5)
        self.assertEqual(cart_obj.add_tax(19.6, type='percentage'), True)
        cart_obj.type = 'tax_excluded'
        self.assertEqual('%s %s'%(cart_obj.total_tax(), cart_obj.currency_symbol), '7.96 €')
        cart_obj.type = 'tax_included'
        self.assertEqual('%s %s'%(cart_obj.total_tax(), cart_obj.currency_symbol), '6.66 €')
        
    def test_untaxed_amount(self):
        discount_coupon = DiscountCoupon(code='Ax9812Y', expiry_date='2010-12-31 12:00', type='percentage', discount=30)
        cart_obj = Cart()
        cart_obj.currency_rate = 1
        cart_obj.price_accuracy = 2
        cart_obj.currency_symbol = '€'
        cart_obj.currency_code = 'EUR'        
        cart_obj.add_item(product=1, price=10.00, quantity=1)
        cart_obj.add_item(product=2, price=12.25, quantity=2.5)
        self.assertEqual('%s %s'%(cart_obj.sub_total(), cart_obj.currency_symbol), '40.63 €')
        self.assertEqual(cart_obj.add_discount(discount_coupon.discount, discount_coupon.type), True)
        self.assertEqual('%s %s'%(cart_obj.total_discount(), cart_obj.currency_symbol), '12.19 €')        
        self.assertEqual(cart_obj.add_tax(19.6, type='percentage'), True)
        cart_obj.type = 'tax_excluded'
        self.assertEqual('%s %s'%(cart_obj.total_tax(), cart_obj.currency_symbol), '5.57 €')        
        self.assertEqual('%s %s'%(cart_obj.total_untaxed_amount(), cart_obj.currency_symbol), '28.44 €')
        cart_obj.type = 'tax_included'
        self.assertEqual('%s %s'%(cart_obj.total_tax(), cart_obj.currency_symbol), '4.66 €')        
        self.assertEqual('%s %s'%(cart_obj.total_untaxed_amount(), cart_obj.currency_symbol), '23.78 €')
        
    def test_total(self):
        discount_coupon = DiscountCoupon(code='Ax9812Y', expiry_date='2010-12-31', type='percentage', discount=30)
        cart_obj = Cart()
        cart_obj.currency_rate = 1
        cart_obj.price_accuracy = 2
        cart_obj.currency_symbol = '€'
        cart_obj.currency_code = 'EUR'
        cart_obj.shipping_charge = 10.21
        cart_obj.add_item(product=1, price=10.00, quantity=1)
        cart_obj.add_item(product=2, price=12.25, quantity=2.5)
        self.assertEqual('%s %s'%(cart_obj.sub_total(), cart_obj.currency_symbol), '40.63 €')
        self.assertEqual(cart_obj.add_discount(discount_coupon.discount, discount_coupon.type), True)
        self.assertEqual('%s %s'%(cart_obj.total_discount(), cart_obj.currency_symbol), '12.19 €')        
        self.assertEqual(cart_obj.add_tax(19.6, type='percentage'), True)
        cart_obj.type = 'tax_excluded' # set type with `tax_excluded`
        self.assertEqual('%s %s'%(cart_obj.total_untaxed_amount(), cart_obj.currency_symbol), '28.44 €')
        self.assertEqual('%s %s'%(cart_obj.total_tax(), cart_obj.currency_symbol), '5.57 €')
        self.assertEqual('%s %s'%(cart_obj.shipping_charge, cart_obj.currency_symbol), '10.21 €')
        self.assertEqual('%s %s'%(cart_obj.total(), cart_obj.currency_symbol), '44.22 €') # TAX EXLCUDED TOTAL
        cart_obj.type = 'tax_included' # set type with `tax_included`
        self.assertEqual('%s %s'%(cart_obj.total_untaxed_amount(), cart_obj.currency_symbol), '23.78 €')        
        self.assertEqual('%s %s'%(cart_obj.total_tax(), cart_obj.currency_symbol), '4.66 €')        
        self.assertEqual('%s %s'%(cart_obj.shipping_charge, cart_obj.currency_symbol), '10.21 €')        
        self.assertEqual('%s %s'%(cart_obj.total(), cart_obj.currency_symbol), '38.65 €') # TAX INCLUDED TOTAL
        cart_obj.currency_rate = 1.2714 # change CURRENCY_RATE
        cart_obj.price_accuracy = 2 # change PRICE_ACCURACY
        cart_obj.currency_symbol = '$'
        cart_obj.currency_code = 'USD'
        cart_obj.type = 'tax_excluded' # set type with `tax_excluded`
        self.assertEqual('%s%s'%(cart_obj.currency_symbol, cart_obj.total_untaxed_amount()), '$36.14')
        self.assertEqual('%s%s'%(cart_obj.currency_symbol, cart_obj.total_tax()), '$7.08')
        self.assertEqual('%s%s'%(cart_obj.currency_symbol, cart_obj.shipping_charge), '$12.98')
        self.assertEqual('%s%s'%(cart_obj.currency_symbol, cart_obj.total()), '$56.2') # TAX EXLCUDED TOTAL
        cart_obj.type = 'tax_included' # set type with `tax_included`
        self.assertEqual('%s%s'%(cart_obj.currency_symbol, cart_obj.total_untaxed_amount()), '$30.22')
        self.assertEqual('%s%s'%(cart_obj.currency_symbol, cart_obj.total_tax()), '$5.92')
        self.assertEqual('%s%s'%(cart_obj.currency_symbol, cart_obj.shipping_charge), '$12.98')
        self.assertEqual('%s%s'%(cart_obj.currency_symbol, cart_obj.total()), '$49.12') # TAX INCLUDED TOTAL
        
if __name__ == '__main__':
#    unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(CartTestCase)
    unittest.TextTestRunner().run(suite)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
