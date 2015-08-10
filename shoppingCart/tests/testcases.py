#!/usr/bin/python
# -*- encoding: utf-8 -*-
################################################################################
#
#    Copyright (C) 2010 - 2015 Dharmesh Patel <mr.dlpatel@gmail.com>.
#    Licence : BSD, see LICENSE for more details.
#
################################################################################

import unittest

from shoppingCart.tests.product import Product, Option, OptionValue
from shoppingCart.tests.discount_coupon import DiscountCoupon
from shoppingCart import Cart

class CartTestCase(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        #Created `Cart` object instance.
        self.cart = Cart()
        self.cart.currency_rate = 1
        self.cart.price_accuracy = 2
        self.cart.currency_symbol = '€'
        self.cart.currency_code = 'EUR'
        self.cart.shipping_charge = 10.21
        #Created `Option` and `OptionValue` object instances.
        self.option_value1 = OptionValue(id=1, name='option_value-1', code='ov1', price=05.00)
        self.option_value2 = OptionValue(id=2, name='option_value-2', code='ov2', price=10.00)
        self.option_value3 = OptionValue(id=3, name='option_value-3', code='ov3', price=15.00)
        self.option_value4 = OptionValue(id=4, name='option_value-4', code='ov4', price=20.00)
        self.option1 = Option(id=1, name='option-1', code='o1', values=[self.option_value1, self.option_value2])
        self.option2 = Option(id=2, name='option-2', code='o2', values=[self.option_value3, self.option_value4])
        #Created `Product` object instances.
        self.product1 = Product(id=1, name='product-1', code='p1', price=10.00)
        self.product2 = Product(id=2, name='product-2', code='p2', price=12.25, options=[self.option1, self.option2])
        self.product3 = Product(id=3, name='product-3', code='p3', price=20.00)
        #Created `DiscountCoupon` object instances.
        self.discount_coupon1 = DiscountCoupon(code='ByQ343X', expiry_date='2010-11-30 12:00:00', type='percentage', discount=30)
        self.discount_coupon2 = DiscountCoupon(code='Ax9812Y', expiry_date='2010-12-31', type='amount', discount=20)
        
    def tearDown(self):
        unittest.TestCase.tearDown(self)
        del self.cart
        del self.product1
        del self.product2
        del self.product3
        del self.option_value1
        del self.option_value2
        del self.option_value3
        del self.option_value4
        del self.option1
        del self.option2
        del self.discount_coupon1
        del self.discount_coupon2

    def test_add_item(self):
        self.assertTrue(self.cart.is_empty)
        self.assertEqual(self.cart.count(), 0)
        #
        #TEST : By passing unique id in `product` parameter.
        #
        self.cart.add_item(product=1, price=10.00, quantity=1)
        self.cart.add_item(product=2, price=12.25, quantity=2.5)
        self.assertFalse(self.cart.is_empty)
        self.assertEqual(self.cart.count(), 3.5)
        self.assertEqual([{'product': item.product, 'quantity': item.quantity} for item in self.cart.get_items()], [{'product': 1, 'quantity': 1}, {'product': 2, 'quantity': 2.5}])
        self.cart.clear()
        self.assertEqual(self.cart.get_items(), [])
        #
        #TEST: By passing unique string(i.e. 'Product Name') in `product` parameter.
        #
        self.cart.remove_items()
        self.cart.add_item(product='product-1', price=10.00, quantity=1)
        self.cart.add_item(product='product-2', price=12.25, quantity=2.5)
        self.assertFalse(self.cart.is_empty)
        self.assertEqual(self.cart.count(), 3.5)
        self.assertEqual([{'product': item.product, 'quantity': item.quantity} for item in self.cart.get_items()], [{'product': 'product-1', 'quantity': 1}, {'product': 'product-2', 'quantity': 2.5}])
        self.cart.clear()
        self.assertEqual(self.cart.get_items(), [])
        #
        #TEST: By passing object instance(i.e. Instance of `Product` object) IN `product` parameter.
        #
        self.cart.remove_items()
        self.cart.add_item(product=self.product1, price=10.00, quantity=1)
        self.cart.add_item(product=self.product2, price=12.25, quantity=2.5)
        self.assertFalse(self.cart.is_empty)
        self.assertEqual(self.cart.count(), 3.5)
        self.assertEqual([{'product': item.product.name, 'quantity': item.quantity} for item in self.cart.get_items()], [{'product': 'product-1', 'quantity': 1}, {'product': 'product-2', 'quantity': 2.5}])
        self.cart.clear()
        self.assertEqual(self.cart.get_items(), [])
        
    def test_update_item(self):
        #
        #TEST : By passing unique id in `product` parameter.
        #
        self.cart.add_item(product=1, price=10.00, quantity=1)
        self.cart.add_item(product=2, price=12.25, quantity=2.5)
        self.assertEqual(self.cart.count(), 3.5)
        self.cart.update_item(product=1, quantity=3)
        self.cart.update_item(product=2, quantity=1.5)
        self.assertEqual(self.cart.count(), 4.5)
        self.assertEqual([{'product': item.product, 'quantity': item.quantity} for item in self.cart.get_items()], [{'product': 1, 'quantity': 3}, {'product': 2, 'quantity': 1.5}])
        self.cart.clear()
        self.assertEqual(self.cart.get_items(), [])
        #
        #TEST: By passing unique string(i.e. 'Product Name') in `product` parameter.
        #
        self.cart.remove_items()
        self.cart.add_item(product='product-1', price=10.00, quantity=1)
        self.cart.add_item(product='product-2', price=12.25, quantity=2.5)
        self.assertEqual(self.cart.count(), 3.5)
        self.cart.update_item(product='product-1', quantity=3)
        self.cart.update_item(product='product-2', quantity=1.5)
        self.assertEqual(self.cart.count(), 4.5)
        self.assertEqual([{'product': item.product, 'quantity': item.quantity} for item in self.cart.get_items()], [{'product': 'product-1', 'quantity': 3}, {'product': 'product-2', 'quantity': 1.5}])
        self.cart.clear()
        self.assertEqual(self.cart.get_items(), [])
        #
        #TEST: By passing object instance(i.e. Instance of `Product` object) IN `product` parameter.
        #
        self.cart.remove_items()
        self.cart.add_item(product=self.product1, price=10.00, quantity=1)
        self.cart.add_item(product=self.product2, price=12.25, quantity=2.5)
        self.assertEqual(self.cart.count(), 3.5)
        self.cart.update_item(product=self.product1, quantity=3)
        self.cart.update_item(product=self.product2, quantity=1.5)
        self.assertEqual(self.cart.count(), 4.5)
        self.assertEqual([{'product': item.product.name, 'quantity': item.quantity} for item in self.cart.get_items()], [{'product': 'product-1', 'quantity': 3}, {'product': 'product-2', 'quantity': 1.5}])
        self.cart.clear()
        self.assertEqual(self.cart.get_items(), [])
        
    def test_remove_item(self):
        #
        #TEST : By passing unique id in `product` parameter.
        #
        self.cart.add_item(product=1, price=10.00, quantity=1)
        self.cart.add_item(product=2, price=12.25, quantity=2.5)
        self.assertEqual(self.cart.count(), 3.5)
        self.cart.remove_item(product=1)
        self.assertEqual(self.cart.count(), 2.5)
        self.assertEqual([{'product': item.product, 'quantity': item.quantity} for item in self.cart.get_items()], [{'product': 2, 'quantity': 2.5}])
        self.cart.clear()
        self.assertEqual(self.cart.get_items(), [])
        #
        #TEST: By passing unique string(i.e. 'Product Name') in `product` parameter.
        #
        self.cart.remove_items()
        self.cart.add_item(product='product-1', price=10.00, quantity=1)
        self.cart.add_item(product='product-2', price=12.25, quantity=2.5)
        self.assertEqual(self.cart.count(), 3.5)
        self.cart.remove_item(product='product-1')
        self.assertEqual(self.cart.count(), 2.5)
        self.assertEqual([{'product': item.product, 'quantity': item.quantity} for item in self.cart.get_items()], [{'product': 'product-2', 'quantity': 2.5}])
        self.cart.clear()
        self.assertEqual(self.cart.get_items(), [])
        #
        #TEST: By passing object instance(i.e. Instance of `Product` object) IN `product` parameter.
        #
        self.cart.remove_items()
        self.cart.add_item(product=self.product1, price=10.00, quantity=1)
        self.cart.add_item(product=self.product2, price=12.25, quantity=2.5)
        self.assertEqual(self.cart.count(), 3.5)
        self.cart.remove_item(product=self.product1)
        self.assertEqual(self.cart.count(), 2.5)
        self.assertEqual([{'product': item.product.name, 'quantity': item.quantity} for item in self.cart.get_items()], [{'product': 'product-2', 'quantity': 2.5}])
        self.cart.clear()
        self.assertEqual(self.cart.get_items(), [])
        
    def test_find_item(self):
        #
        #TEST : By passing unique id in `product` parameter.
        #
        self.cart.add_item(product=1, price=10.00, quantity=1)
        self.cart.add_item(product=2, price=12.25, quantity=2.5)
        self.assertEqual(self.cart.find_item(3), None)
        self.assertEqual([{'product': item.product, 'quantity': item.quantity} for item in [self.cart.find_item(1)]], [{'product': 1, 'quantity': 1}])
        self.cart.clear()
        self.assertEqual(self.cart.get_items(), [])
        #
        #TEST: By passing unique string(i.e. 'Product Name') in `product` parameter.
        #
        self.cart.remove_items()
        self.cart.add_item(product='product-1', price=10.00, quantity=1)
        self.cart.add_item(product='product-2', price=12.25, quantity=2.5)
        self.assertEqual(self.cart.find_item('product-3'), None)
        self.assertEqual([{'product': item.product, 'quantity': item.quantity} for item in [self.cart.find_item('product-1')]], [{'product': 'product-1', 'quantity': 1}])
        self.cart.clear()
        self.assertEqual(self.cart.get_items(), [])
        #
        #TEST: By passing object instance(i.e. Instance of `Product` object) IN `product` parameter.
        #
        self.cart.remove_items()
        self.cart.add_item(product=self.product1, price=10.00, quantity=1)
        self.cart.add_item(product=self.product2, price=12.25, quantity=2.5)
        self.assertEqual(self.cart.find_item(self.product3), None)
        self.assertEqual([{'product': item.product.name, 'quantity': item.quantity} for item in [self.cart.find_item(self.product1)]], [{'product': 'product-1', 'quantity': 1}])
        self.cart.clear()
        self.assertEqual(self.cart.get_items(), [])
    
    def test_add_item_with_options(self):
        self.assertTrue(self.cart.is_empty)
        self.assertEqual(self.cart.count(), 0)
        #
        #TEST : By passing unique id in `product` and 'options' parameters.
        #        
        #Added product and specific taxes related to it
        self.cart.add_item(product=1, price=10.00, quantity=1, taxes=[{'amount': 19.6, 'type': 'percentage'}, {'amount': 2.1, 'type': 'fixed'}])
        #Added product and related options
        self.cart.add_item(product=2, price=12.25, quantity=2.5)
        self.cart.add_item(product=2, price=12.25, quantity=1, options={2: {4: {'price': 20.00}}})
        self.cart.add_item(product=2, price=12.25, quantity=2, options={1: {1: {'price': 05.00}}, 2: {3: {'price': 15.00}}})
        self.cart.add_item(product=2, price=12.25, quantity=3.5, options={1: {2: {'price': 10.00}}, 2: {4: {'price': 20.00}}})
        self.assertEqual([{'product': item.product, 'quantity': item.quantity, 'price': item.price, 'options': item.get_options()} for item in self.cart.get_items()], [{'product': 1, 'options': {}, 'price': 10.0, 'quantity': 1}, {'product': 2, 'options': {}, 'price': 12.25, 'quantity': 2.5}, {'product': 2, 'options': {2: {4: {'price': 20.0}}}, 'price': 12.25, 'quantity': 1}, {'product': 2, 'options': {1: {1: {'price': 5.0}}, 2: {3: {'price': 15.0}}}, 'price': 12.25, 'quantity': 2}, {'product': 2, 'options': {1: {2: {'price': 10.0}}, 2: {4: {'price': 20.0}}}, 'price': 12.25, 'quantity': 3.5}])
        self.assertEqual(self.cart.count(), 10.0)
        #Cart tax type
        self.assertEqual('%s'%(self.cart.tax_type,), 'excluded')
        #Sub Total
        self.assertEqual('%s %s'%(self.cart.sub_total(), self.cart.currency_symbol), '285.26 €')
        #Total Untaxed Amount
        self.assertEqual('%s %s'%(self.cart.total_untaxed_amount(), self.cart.currency_symbol), '285.26 €')
        #Total Tax
        self.assertEqual('%s %s'%(self.cart.total_tax(), self.cart.currency_symbol), '4.06 €')
        #Shipping Charge
        self.assertEqual('%s %s'%(self.cart.shipping_charge, self.cart.currency_symbol), '10.21 €')
        #Total
        self.assertEqual('%s %s'%(self.cart.total(), self.cart.currency_symbol), '299.53 €')
        #
        #TEST: By passing unique string(i.e. 'Product Name', 'Option Name' and 'OptionValue Name') in `product` and `options` parameters.
        #
        self.cart.remove_items()
        #Added product and specific taxes related to it
        self.cart.add_item(product='product-1', price=10.00, quantity=1, taxes=[{'amount': 19.6, 'type': 'percentage'}, {'amount': 2.1, 'type': 'fixed'}])
        #Added product and related options
        self.cart.add_item(product='product-2', price=12.25, quantity=2.5)
        self.cart.add_item(product='product-2', price=12.25, quantity=1, options={'option-2': {'option_value-4': {'price': 20.00}}})
        self.cart.add_item(product='product-2', price=12.25, quantity=2, options={'option-1': {'option_value-1': {'price': 05.00}}, 'option-2': {'option_value-3': {'price': 15.00}}})
        self.cart.add_item(product='product-2', price=12.25, quantity=3.5, options={'option-1': {'option_value-2': {'price': 10.00}}, 'option-2': {'option_value-4': {'price': 20.00}}})
        self.assertEqual([{'product': item.product, 'quantity': item.quantity, 'price': item.price, 'options': item.get_options()} for item in self.cart.get_items()], [{'product': 'product-1', 'options': {}, 'price': 10.0, 'quantity': 1}, {'product': 'product-2', 'options': {}, 'price': 12.25, 'quantity': 2.5}, {'product': 'product-2', 'options': {'option-2': {'option_value-4': {'price': 20.0}}}, 'price': 12.25, 'quantity': 1}, {'product': 'product-2', 'options': {'option-1': {'option_value-1': {'price': 5.0}}, 'option-2': {'option_value-3': {'price': 15.0}}}, 'price': 12.25, 'quantity': 2}, {'product': 'product-2', 'options': {'option-1': {'option_value-2': {'price': 10.0}}, 'option-2': {'option_value-4': {'price': 20.0}}}, 'price': 12.25, 'quantity': 3.5}])
        self.assertEqual(self.cart.count(), 10.0)
        #Cart tax type
        self.assertEqual('%s'%(self.cart.tax_type,), 'excluded')
        #Sub Total
        self.assertEqual('%s %s'%(self.cart.sub_total(), self.cart.currency_symbol), '285.26 €')
        #Total Untaxed Amount
        self.assertEqual('%s %s'%(self.cart.total_untaxed_amount(), self.cart.currency_symbol), '285.26 €')
        #Total Tax
        self.assertEqual('%s %s'%(self.cart.total_tax(), self.cart.currency_symbol), '4.06 €')
        #Shipping Charge
        self.assertEqual('%s %s'%(self.cart.shipping_charge, self.cart.currency_symbol), '10.21 €')
        #Total
        self.assertEqual('%s %s'%(self.cart.total(), self.cart.currency_symbol), '299.53 €')
        #
        #TEST: By passing object instance(i.e. Instance of `Product`, `Option` and `OptionValue` objects) IN `product`, `options` parameters.
        #
        self.cart.remove_items()
        #Added product and specific taxes related to it
        self.cart.add_item(product=self.product1, price=10.00, quantity=1, taxes=[{'amount': 19.6, 'type': 'percentage'}, {'amount': 2.1, 'type': 'fixed'}])
        #Added product and related options
        self.cart.add_item(product=self.product2, price=12.25, quantity=2.5)
        self.cart.add_item(product=self.product2, price=12.25, quantity=1, options={self.option1: {self.option_value4: {'price': 20.00}}})
        self.cart.add_item(product=self.product2, price=12.25, quantity=2, options={self.option1: {self.option_value1: {'price': 05.00}}, self.option2: {self.option_value3: {'price': 15.00}}})
        self.cart.add_item(product=self.product2, price=12.25, quantity=3.5, options={self.option1: {self.option_value2: {'price': 10.00}}, self.option2: {self.option_value4: {'price': 20.00}}})
        options={}
#        self.assertEqual([{'product': item.product.name, 'quantity': item.quantity, 'price': item.price, 'options': item.has_options and [options.update({option.name: [{key.name: value} for key, value in option_value.items()][0]}) for option, option_value in item.get_options().items()] and options or {}} for item in self.cart.get_items()], [{'product': 'product-1', 'options': {}, 'price': 10.0, 'quantity': 1}, {'product': 'product-2', 'options': {}, 'price': 12.25, 'quantity': 2.5}, {'product': 'product-2', 'options': {'option-2': {'option_value-4': {'price': 20.0}}}, 'price': 12.25, 'quantity': 1}, {'product': 'product-2', 'options': {'option-1': {'option_value-1': {'price': 5.0}}, 'option-2': {'option_value-3': {'price': 15.0}}}, 'price': 12.25, 'quantity': 2}, {'product': 'product-2', 'options': {'option-1': {'option_value-2': {'price': 10.0}}, 'option-2': {'option_value-4': {'price': 20.0}}}, 'price': 12.25, 'quantity': 3.5}])
        self.assertEqual(self.cart.count(), 10.0)
        #Cart tax type
        self.assertEqual('%s'%(self.cart.tax_type,), 'excluded')
        #Sub Total
        self.assertEqual('%s %s'%(self.cart.sub_total(), self.cart.currency_symbol), '285.26 €')
        #Total Untaxed Amount
        self.assertEqual('%s %s'%(self.cart.total_untaxed_amount(), self.cart.currency_symbol), '285.26 €')
        #Total Tax
        self.assertEqual('%s %s'%(self.cart.total_tax(), self.cart.currency_symbol), '4.06 €')
        #Shipping Charge
        self.assertEqual('%s %s'%(self.cart.shipping_charge, self.cart.currency_symbol), '10.21 €')
        #Total
        self.assertEqual('%s %s'%(self.cart.total(), self.cart.currency_symbol), '299.53 €')

    def test_update_item_with_options(self):
        #
        #TEST : By passing unique id in `product` and 'options' parameters.
        #        
        #Added product and specific taxes related to it
        self.cart.add_item(product=1, price=10.00, quantity=1, taxes=[{'amount': 19.6, 'type': 'percentage'}, {'amount': 2.1, 'type': 'fixed'}])
        #Added product and related options
        self.cart.add_item(product=2, price=12.25, quantity=2.5)
        self.cart.add_item(product=2, price=12.25, quantity=1, options={2: {4: {'price': 20.00}}})
        self.cart.add_item(product=2, price=12.25, quantity=2, options={1: {1: {'price': 05.00}}, 2: {3: {'price': 15.00}}})
        self.cart.add_item(product=2, price=12.25, quantity=3.5, options={1: {2: {'price': 10.00}}, 2: {4: {'price': 20.00}}})
        self.assertEqual(self.cart.count(), 10)
        #Product updated
        self.cart.update_item(product=1, quantity=3)
        #To update item which has option need to pass option values only in `option_values` parameter
        self.cart.update_item(product=2, quantity=1.5)        
        self.cart.update_item(product=2, quantity=2, option_values=[4])
        self.cart.update_item(product=2, quantity=3, option_values=[1, 3])
        self.cart.update_item(product=2, quantity=4, option_values=[2, 4])
        self.assertEqual(self.cart.count(), 13.5)
        self.assertEqual([{'product': item.product, 'quantity': item.quantity} for item in self.cart.get_items()], [{'product': 1, 'quantity': 3}, {'product': 2, 'quantity': 1.5}, {'product': 2, 'quantity': 2}, {'product': 2, 'quantity': 3}, {'product': 2, 'quantity': 4}])
        self.cart.clear()
        self.assertEqual(self.cart.get_items(), [])
        #
        #TEST: By passing unique string(i.e. 'Product Name', 'Option Name' and 'OptionValue Name') in `product` and `options` parameters.
        #
        self.cart.remove_items()
        self.cart.add_item(product='product-1', price=10.00, quantity=1, taxes=[{'amount': 19.6, 'type': 'percentage'}, {'amount': 2.1, 'type': 'fixed'}])
        #Added product and related options
        self.cart.add_item(product='product-2', price=12.25, quantity=2.5)
        self.cart.add_item(product='product-2', price=12.25, quantity=1, options={'option-2': {'option_value-4': {'price': 20.00}}})
        self.cart.add_item(product='product-2', price=12.25, quantity=2, options={'option-1': {'option_value-1': {'price': 05.00}}, 'option-2': {'option_value-3': {'price': 15.00}}})
        self.cart.add_item(product='product-2', price=12.25, quantity=3.5, options={'option-1': {'option_value-2': {'price': 10.00}}, 'option-2': {'option_value-4': {'price': 20.00}}})
        self.assertEqual(self.cart.count(), 10)
        #Product updated        
        self.cart.update_item(product='product-1', quantity=3)
        #To update item which has option need to pass option values only in `option_values` parameter
        self.cart.update_item(product='product-2', quantity=1.5)
        self.cart.update_item(product='product-2', quantity=2, option_values=['option_value-4'])
        self.cart.update_item(product='product-2', quantity=3, option_values=['option_value-1', 'option_value-3'])
        self.cart.update_item(product='product-2', quantity=4, option_values=['option_value-2', 'option_value-4'])
        self.assertEqual(self.cart.count(), 13.5)
        self.assertEqual([{'product': item.product, 'quantity': item.quantity} for item in self.cart.get_items()], [{'product': 'product-1', 'quantity': 3}, {'product': 'product-2', 'quantity': 1.5}, {'product': 'product-2', 'quantity': 2}, {'product': 'product-2', 'quantity': 3}, {'product': 'product-2', 'quantity': 4}])
        self.cart.clear()
        self.assertEqual(self.cart.get_items(), [])
        #
        #TEST: By passing object instance(i.e. Instance of `Product`, `Option` and `OptionValue` objects) IN `product`, `options` parameters.
        #
        self.cart.remove_items()
        self.cart.add_item(product=self.product1, price=10.00, quantity=1)
        #Added product and related options
        self.cart.add_item(product=self.product2, price=12.25, quantity=2.5)
        self.cart.add_item(product=self.product2, price=12.25, quantity=1, options={self.option1: {self.option_value4: {'price': 20.00}}})
        self.cart.add_item(product=self.product2, price=12.25, quantity=2, options={self.option1: {self.option_value1: {'price': 05.00}}, self.option2: {self.option_value3: {'price': 15.00}}})
        self.cart.add_item(product=self.product2, price=12.25, quantity=3.5, options={self.option1: {self.option_value2: {'price': 10.00}}, self.option2: {self.option_value4: {'price': 20.00}}})
        self.assertEqual(self.cart.count(), 10.0)
        #Product updated
        self.cart.update_item(product=self.product1, quantity=3)
        #To update item which has option need to pass option values only in `option_values` parameter
        self.cart.update_item(product=self.product2, quantity=1.5)
        self.cart.update_item(product=self.product2, quantity=2, option_values=[self.option_value4])
        self.cart.update_item(product=self.product2, quantity=3, option_values=[self.option_value1, self.option_value3])
        self.cart.update_item(product=self.product2, quantity=4, option_values=[self.option_value2, self.option_value4])
        self.assertEqual(self.cart.count(), 13.5)
        self.assertEqual([{'product': item.product.name, 'quantity': item.quantity} for item in self.cart.get_items()], [{'product': 'product-1', 'quantity': 3}, {'product': 'product-2', 'quantity': 1.5}, {'product': 'product-2', 'quantity': 2}, {'product': 'product-2', 'quantity': 3}, {'product': 'product-2', 'quantity': 4}])
        self.cart.clear()
        self.assertEqual(self.cart.get_items(), [])
        
    def test_remove_item_with_options(self):
        #
        #TEST : By passing unique id in `product` and 'options' parameters.
        #        
        #Added product and specific taxes related to it
        self.cart.add_item(product=1, price=10.00, quantity=1, taxes=[{'amount': 19.6, 'type': 'percentage'}, {'amount': 2.1, 'type': 'fixed'}])
        #Added product and related options
        self.cart.add_item(product=2, price=12.25, quantity=2.5)
        self.cart.add_item(product=2, price=12.25, quantity=1, options={2: {4: {'price': 20.00}}})
        self.cart.add_item(product=2, price=12.25, quantity=2, options={1: {1: {'price': 05.00}}, 2: {3: {'price': 15.00}}})
        self.cart.add_item(product=2, price=12.25, quantity=3.5, options={1: {2: {'price': 10.00}}, 2: {4: {'price': 20.00}}})
        self.assertEqual(self.cart.count(), 10)
        #Product removed
        self.cart.remove_item(product=1)
        #To remove item which has option need to pass option values only in `option_values` parameter
        self.cart.remove_item(product=2, option_values=[2, 4])
        self.assertEqual(self.cart.count(), 5.5)
        self.assertEqual([{'product': item.product, 'quantity': item.quantity} for item in self.cart.get_items()], [{'product': 2, 'quantity': 2.5}, {'product': 2, 'quantity': 1}, {'product': 2, 'quantity': 2}])
        self.cart.clear()
        self.assertEqual(self.cart.get_items(), [])
        #
        #TEST: By passing unique string(i.e. 'Product Name', 'Option Name' and 'OptionValue Name') in `product` and `options` parameters.
        #
        self.cart.remove_items()
        self.cart.add_item(product='product-1', price=10.00, quantity=1, taxes=[{'amount': 19.6, 'type': 'percentage'}, {'amount': 2.1, 'type': 'fixed'}])
        #Added product and related options
        self.cart.add_item(product='product-2', price=12.25, quantity=2.5)
        self.cart.add_item(product='product-2', price=12.25, quantity=1, options={'option-2': {'option_value-4': {'price': 20.00}}})
        self.cart.add_item(product='product-2', price=12.25, quantity=2, options={'option-1': {'option_value-1': {'price': 05.00}}, 'option-2': {'option_value-3': {'price': 15.00}}})
        self.cart.add_item(product='product-2', price=12.25, quantity=3.5, options={'option-1': {'option_value-2': {'price': 10.00}}, 'option-2': {'option_value-4': {'price': 20.00}}})
        self.assertEqual(self.cart.count(), 10)
        #Product removed
        self.cart.remove_item(product='product-1')
        #To remove item which has option need to pass option values only in `option_values` parameter
        self.cart.remove_item(product='product-2', option_values=['option_value-2', 'option_value-4'])
        self.assertEqual(self.cart.count(), 5.5)
        self.assertEqual([{'product': item.product, 'quantity': item.quantity} for item in self.cart.get_items()], [{'product': 'product-2', 'quantity': 2.5}, {'product': 'product-2', 'quantity': 1}, {'product': 'product-2', 'quantity': 2}])
        self.cart.clear()
        self.assertEqual(self.cart.get_items(), [])
        #
        #TEST: By passing object instance(i.e. Instance of `Product`, `Option` and `OptionValue` objects) IN `product`, `options` parameters.
        #
        self.cart.remove_items()
        self.cart.add_item(product=self.product1, price=10.00, quantity=1)
        #Added product and related options
        self.cart.add_item(product=self.product2, price=12.25, quantity=2.5)
        self.cart.add_item(product=self.product2, price=12.25, quantity=1, options={self.option1: {self.option_value4: {'price': 20.00}}})
        self.cart.add_item(product=self.product2, price=12.25, quantity=2, options={self.option1: {self.option_value1: {'price': 05.00}}, self.option2: {self.option_value3: {'price': 15.00}}})
        self.cart.add_item(product=self.product2, price=12.25, quantity=3.5, options={self.option1: {self.option_value2: {'price': 10.00}}, self.option2: {self.option_value4: {'price': 20.00}}})
        self.assertEqual(self.cart.count(), 10.0)
        #Product removed
        self.cart.remove_item(product=self.product1)
        #To remove item which has option need to pass option values only in `option_values` parameter
        self.cart.remove_item(product=self.product2, option_values=[self.option_value2, self.option_value4])
        self.assertEqual(self.cart.count(), 5.5)
        self.assertEqual([{'product': item.product.name, 'quantity': item.quantity} for item in self.cart.get_items()], [{'product': 'product-2', 'quantity': 2.5}, {'product': 'product-2', 'quantity': 1}, {'product': 'product-2', 'quantity': 2}])
        self.cart.clear()
        self.assertEqual(self.cart.get_items(), [])

    def test_find_item_with_options(self):
        #
        #TEST : By passing unique id in `product` and 'options' parameters.
        #        
        #Added product and specific taxes related to it
        self.cart.add_item(product=1, price=10.00, quantity=1, taxes=[{'amount': 19.6, 'type': 'percentage'}, {'amount': 2.1, 'type': 'fixed'}])
        #Added product and related options
        self.cart.add_item(product=2, price=12.25, quantity=2.5)
        self.cart.add_item(product=2, price=12.25, quantity=1, options={2: {4: {'price': 20.00}}})
        self.cart.add_item(product=2, price=12.25, quantity=2, options={1: {1: {'price': 05.00}}, 2: {3: {'price': 15.00}}})
        self.cart.add_item(product=2, price=12.25, quantity=3.5, options={1: {2: {'price': 10.00}}, 2: {4: {'price': 20.00}}})
        #To find item which has option need to pass option values only in `option_values` parameter
        self.assertEqual(self.cart.find_item(3), None)
        self.assertEqual([{'product': item.product, 'quantity': item.quantity} for item in [self.cart.find_item(1)]], [{'product': 1, 'quantity': 1}])
        self.assertEqual([{'product': item.product, 'quantity': item.quantity} for item in [self.cart.find_item(2)]], [{'product': 2, 'quantity': 2.5}])
        self.assertEqual([{'product': item.product, 'quantity': item.quantity} for item in [self.cart.find_item(2, option_values=[1, 3])]], [{'product': 2, 'quantity': 2}])
        self.cart.clear()
        self.assertEqual(self.cart.get_items(), [])
        #
        #TEST: By passing unique string(i.e. 'Product Name', 'Option Name' and 'OptionValue Name') in `product` and `options` parameters.
        #
        self.cart.remove_items()
        self.cart.add_item(product='product-1', price=10.00, quantity=1, taxes=[{'amount': 19.6, 'type': 'percentage'}, {'amount': 2.1, 'type': 'fixed'}])
        #Added product and related options
        self.cart.add_item(product='product-2', price=12.25, quantity=2.5)
        self.cart.add_item(product='product-2', price=12.25, quantity=1, options={'option-2': {'option_value-4': {'price': 20.00}}})
        self.cart.add_item(product='product-2', price=12.25, quantity=2, options={'option-1': {'option_value-1': {'price': 05.00}}, 'option-2': {'option_value-3': {'price': 15.00}}})
        self.cart.add_item(product='product-2', price=12.25, quantity=3.5, options={'option-1': {'option_value-2': {'price': 10.00}}, 'option-2': {'option_value-4': {'price': 20.00}}})
        #To find item which has option need to pass option values only in `option_values` parameter
        self.assertEqual(self.cart.find_item('product-3'), None)
        self.assertEqual([{'product': item.product, 'quantity': item.quantity} for item in [self.cart.find_item('product-1')]], [{'product': 'product-1', 'quantity': 1}])
        self.assertEqual([{'product': item.product, 'quantity': item.quantity} for item in [self.cart.find_item('product-2')]], [{'product': 'product-2', 'quantity': 2.5}])
        self.assertEqual([{'product': item.product, 'quantity': item.quantity} for item in [self.cart.find_item('product-2', option_values=['option_value-1', 'option_value-3'])]], [{'product': 'product-2', 'quantity': 2}])
        self.cart.clear()
        self.assertEqual(self.cart.get_items(), [])
        #
        #TEST: By passing object instance(i.e. Instance of `Product`, `Option` and `OptionValue` objects) IN `product`, `options` parameters.
        #
        self.cart.remove_items()
        self.cart.add_item(product=self.product1, price=10.00, quantity=1)
        #Added product and related options
        self.cart.add_item(product=self.product2, price=12.25, quantity=2.5)
        self.cart.add_item(product=self.product2, price=12.25, quantity=1, options={self.option1: {self.option_value4: {'price': 20.00}}})
        self.cart.add_item(product=self.product2, price=12.25, quantity=2, options={self.option1: {self.option_value1: {'price': 05.00}}, self.option2: {self.option_value3: {'price': 15.00}}})
        self.cart.add_item(product=self.product2, price=12.25, quantity=3.5, options={self.option1: {self.option_value2: {'price': 10.00}}, self.option2: {self.option_value4: {'price': 20.00}}})
        #To find item which has option need to pass option values only in `option_values` parameter
        self.assertEqual(self.cart.find_item(self.product3), None)
        self.assertEqual([{'product': item.product.name, 'quantity': item.quantity} for item in [self.cart.find_item(self.product1)]], [{'product': 'product-1', 'quantity': 1}])
        self.assertEqual([{'product': item.product.name, 'quantity': item.quantity} for item in [self.cart.find_item(self.product2)]], [{'product': 'product-2', 'quantity': 2.5}])
        self.assertEqual([{'product': item.product.name, 'quantity': item.quantity} for item in [self.cart.find_item(self.product2, option_values=[self.option_value1, self.option_value3])]], [{'product': 'product-2', 'quantity': 2}])
        self.cart.clear()
        self.assertEqual(self.cart.get_items(), [])

    def test_add_multi_discount(self):
        self.assertFalse(self.cart.is_discount_applied)
        #
        #TEST : By passing amount in `amount` parameter.
        #
        self.cart.add_discount(amount=30, type='percentage')
        self.cart.add_discount(amount=20, type='amount')
        self.assertTrue(self.cart.is_discount_applied)
        self.assertEqual([discount for discount in self.cart.get_discounts()], [{'amount': 30, 'type': 'percentage'}, {'amount': 20, 'type': 'amount'}])
        #
        #TEST: Using object instance(i.e. Instance of `DiscountCoupon` object).
        #
        self.cart.remove_discounts()
        self.cart.add_discount(amount=self.discount_coupon1.discount, type=self.discount_coupon1.type)
        self.cart.add_discount(amount=self.discount_coupon2.discount, type=self.discount_coupon2.type)
        self.assertTrue(self.cart.is_discount_applied)
        self.assertEqual([discount for discount in self.cart.get_discounts()], [{'amount': 30, 'type': 'percentage'}, {'amount': 20, 'type': 'amount'}])
        
    def test_add_multi_tax(self):
        #Added tax specific to product only
        self.cart.add_item(product=1, price=10.00, quantity=1, taxes=[{'amount':10.00, 'type': 'percentage'}, {'amount':5.0, 'type': 'fixed'}])
        #Added general taxes[which will apply on all cart items]
        self.assertTrue(self.cart.add_tax(19.6, type='percentage'))
        self.assertTrue(self.cart.add_tax(20.1, type='fixed'))
        #
        #TEST: By trying to add tax which is already added
        #
        self.assertFalse(self.cart.add_tax(19.6, type='percentage'))
        self.assertEqual(self.cart.get_taxes(), [{'amount': 10.0, 'type': 'percentage'}, {'amount': 5.0, 'type': 'fixed'}, {'amount': 19.600000000000001, 'type': 'percentage'}, {'amount': 20.100000000000001, 'type': 'fixed'}])
    
    def test_remove_tax(self):
        #Added general taxes
        self.assertTrue(self.cart.add_tax(19.6, type='percentage'))
        self.assertTrue(self.cart.add_tax(20.1, type='fixed'))
        self.assertFalse(self.cart.remove_tax(10))
        self.assertTrue(self.cart.remove_tax(20.1, type='fixed'))
        self.assertEqual(self.cart.get_taxes(), [{'amount': 19.600000000000001, 'type': 'percentage'}])

    def test_sub_total(self):
        self.cart.add_item(product=1, price=10.00, quantity=1)
        self.cart.add_item(product=2, price=12.25, quantity=2.5)
        #Sub Total
        self.assertEqual('%s %s'%(self.cart.sub_total(), self.cart.currency_symbol), '40.63 €')
        #Set `currency_rate`, `price_accuracy`, `currency_symbol` and `currency_code`
        self.cart.currency_rate = 1.2714
        self.cart.price_accuracy = 2
        self.cart.currency_symbol = '$'
        self.cart.currency_code = 'USD'
        #Sub Total
        self.assertEqual('%s%s'%(self.cart.currency_symbol, self.cart.sub_total()), '$51.63')
        
    def test_total_discount(self):
        self.cart.add_item(product=1, price=10.00, quantity=1)
        self.cart.add_item(product=2, price=12.25, quantity=2.5)
        #Sub Total
        self.assertEqual('%s %s'%(self.cart.sub_total(), self.cart.currency_symbol), '40.63 €')
        #Added discount
        self.cart.add_discount(self.discount_coupon1.discount, self.discount_coupon1.type)
        #Total Discount
        self.assertEqual('%s %s'%(self.cart.total_discount(), self.cart.currency_symbol), '12.19 €')
        
    def test_total_untaxed_amount(self):
        self.cart.add_item(product=1, price=10.00, quantity=1)
        self.cart.add_item(product=2, price=12.25, quantity=2.5)
        #Sub Total
        self.assertEqual('%s %s'%(self.cart.sub_total(), self.cart.currency_symbol), '40.63 €')
        #Added discount
        self.cart.add_discount(self.discount_coupon1.discount, self.discount_coupon1.type)
        #Total Discount
        self.assertEqual('%s %s'%(self.cart.total_discount(), self.cart.currency_symbol), '12.19 €')
        #Added Tax
        self.assertTrue(self.cart.add_tax(19.6, type='percentage'))
        #Set `tax_type` with 'excluded'
        self.cart.tax_type = 'excluded'
        #Total Tax
        self.assertEqual('%s %s'%(self.cart.total_tax(), self.cart.currency_symbol), '5.57 €')
        #Total Untaxed Amount
        self.assertEqual('%s %s'%(self.cart.total_untaxed_amount(), self.cart.currency_symbol), '28.44 €')
        #Set `tax_type` with 'included'
        self.cart.tax_type = 'included'
        #Total Tax
        self.assertEqual('%s %s'%(self.cart.total_tax(), self.cart.currency_symbol), '4.66 €')
        #Total Untaxed Amount
        self.assertEqual('%s %s'%(self.cart.total_untaxed_amount(), self.cart.currency_symbol), '23.78 €')

    def test_total_tax(self):
        self.cart.add_item(product=1, price=10.00, quantity=1)
        self.cart.add_item(product=2, price=12.25, quantity=2.5)
        #Added general tax
        self.assertTrue(self.cart.add_tax(19.6, type='percentage'))
        #Set `tax_type` with 'excluded'
        self.cart.tax_type = 'excluded'
        #Total Tax
        self.assertEqual('%s %s'%(self.cart.total_tax(), self.cart.currency_symbol), '7.96 €')
        #Set `tax_type` with 'included'
        self.cart.tax_type = 'included'
        #Total Tax
        self.assertEqual('%s %s'%(self.cart.total_tax(), self.cart.currency_symbol), '6.66 €')
        
    def test_total_with_multi_currency(self):
        self.cart.add_item(product=1, price=10.00, quantity=1)
        self.cart.add_item(product=2, price=12.25, quantity=2.5)
        #Sub Total
        self.assertEqual('%s %s'%(self.cart.sub_total(), self.cart.currency_symbol), '40.63 €')
        #Added discount
        self.cart.add_discount(self.discount_coupon1.discount, self.discount_coupon1.type)
        #Total discount
        self.assertEqual('%s %s'%(self.cart.total_discount(), self.cart.currency_symbol), '12.19 €')
        #Added tax
        self.assertTrue(self.cart.add_tax(19.6, type='percentage'))
        #Set `tax_type` with 'excluded'
        self.cart.tax_type = 'excluded'
        #Total Untaxed Amount
        self.assertEqual('%s %s'%(self.cart.total_untaxed_amount(), self.cart.currency_symbol), '28.44 €')
        #Total Tax
        self.assertEqual('%s %s'%(self.cart.total_tax(), self.cart.currency_symbol), '5.57 €')
        #Shipping Charge
        self.assertEqual('%s %s'%(self.cart.shipping_charge, self.cart.currency_symbol), '10.21 €')
        #Tax Excluded Total
        self.assertEqual('%s %s'%(self.cart.total(), self.cart.currency_symbol), '44.22 €')
        #Set `tax_type` with 'included'
        self.cart.tax_type = 'included'
        #Total Untaxed Amount
        self.assertEqual('%s %s'%(self.cart.total_untaxed_amount(), self.cart.currency_symbol), '23.78 €')
        #Total Tax
        self.assertEqual('%s %s'%(self.cart.total_tax(), self.cart.currency_symbol), '4.66 €')
        #Shipping Charge
        self.assertEqual('%s %s'%(self.cart.shipping_charge, self.cart.currency_symbol), '10.21 €')
        #Tax Included Total
        self.assertEqual('%s %s'%(self.cart.total(), self.cart.currency_symbol), '38.65 €')
        #Set `currency_rate`, `price_accuracy`, `currency_symbol` and `currency_code`
        self.cart.currency_rate = 1.2714
        self.cart.price_accuracy = 2 
        self.cart.currency_symbol = '$'
        self.cart.currency_code = 'USD'
        #Set `tax_type` with 'excluded'
        self.cart.tax_type = 'excluded'
        self.assertEqual('%s%s'%(self.cart.currency_symbol, self.cart.total_untaxed_amount()), '$36.14')
        self.assertEqual('%s%s'%(self.cart.currency_symbol, self.cart.total_tax()), '$7.08')
        self.assertEqual('%s%s'%(self.cart.currency_symbol, self.cart.shipping_charge), '$12.98')
        #Tax Excluded Total
        self.assertEqual('%s%s'%(self.cart.currency_symbol, self.cart.total()), '$56.2')
        #Set `tax_type` with 'included'
        self.cart.tax_type = 'included'
        self.assertEqual('%s%s'%(self.cart.currency_symbol, self.cart.total_untaxed_amount()), '$30.22')
        self.assertEqual('%s%s'%(self.cart.currency_symbol, self.cart.total_tax()), '$5.92')
        self.assertEqual('%s%s'%(self.cart.currency_symbol, self.cart.shipping_charge), '$12.98')
        #Tax Included Total
        self.assertEqual('%s%s'%(self.cart.currency_symbol, self.cart.total()), '$49.12')
        
def suite():
   suite = unittest.TestSuite()
   suite.addTest(unittest.makeSuite(CartTestCase))
   return suite

if __name__ == '__main__':
#    unittest.main()
#    suite = unittest.TestLoader().loadTestsFromTestCase(CartTestCase)
    unittest.TextTestRunner().run(suite())

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
