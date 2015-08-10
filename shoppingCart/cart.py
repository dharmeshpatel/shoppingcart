#!/usr/bin/python
# -*- encoding: utf-8 -*-
################################################################################
#
#    Copyright (C) 2010 - 2015 Dharmesh Patel <mr.dlpatel@gmail.com>.
#    Licence : BSD, see LICENSE for more details.
#
################################################################################

from shoppingCart.tax import calculate
from shoppingCart.utils import id_from_object, get_dict_of_ids, get_list_of_ids

__all__ = ['Cart']

class Cart(object):
    """
    Collection of :class:`CartItem` objects.
    """
    def __init__(self, site=None, customer=None):
        """
        :param site: Unique id or name of :class:`Site` object or instance of :class:`Site`.
        :param customer: Unique id or name of :class:`Customer` object or instance of :class:`Customer`.
        """
        self.site = site
        self.customer = customer
        self.__intiallize()
    
    def __intiallize(self):
        """
        To intiallize or reset class member variable's value.
        """
        self.__items = list()
        self.__taxes = list()
        self.currency_rate = 1
        self.price_accuracy = 2
        self.currency_symbol = '€'
        self.currency_code = 'EUR'
        self.__shipping_charge = 0.0
        self.shipping_method = 'Flat Rate Per Order'
        self.tax_type = 'excluded'
        self.__discounts = list()

    def add_item(self, product, price=0.0, quantity=1, taxes=[], options={}):
        """
        To add or update product, price, quantity, taxes and options in :class:`CartItem` object.
        
        :param product: Unique id or name of :class:`Product` object or instance of :class:`Product`.
        :param price: Product price.
        :param quantity: Product quantity(default 1).
        :param taxes: Taxes of the product(default []).
        :param options: Options of the product(default {}).
        """        
        if not isinstance(quantity, (int, float)):
            raise TypeError('quantity field value must be integer or float type', 'quantity')
        elif not (quantity or quantity >= 1):
            raise ValueError('quantity field value must be greater then 1', 'quantity')
        
        option_values = []
        for option_value in options.values():            
            if isinstance(option_value, dict):
                option_value = option_value.keys()[0]
            option_values.append(option_value)
            
        cart_item = self.find_item(product, option_values)
        
        if cart_item:
            cart_item.update_quantity(cart_item.quantity + quantity)
        else:
            if not price:
                raise ValueError('price value is 0.0')
            elif not isinstance(price, (int, float)):
                raise TypeError('price value must be integer or float type', 'price')
                
            cart_item = CartItem(self, product, price, quantity, taxes, options)
            self.__items.append(cart_item)

    def update_item(self, product, quantity, option_values=[]):
        """
        To update :class:`CartItem` object quantity.
        
        :param product: Unique id or name of :class:`Product` object or instance of :class:`Product`.
        :param quantity: Updated quantity.
        :param option_values: Option values of the product(default []).
        """
        if not isinstance(quantity, (int, float)):
            raise TypeError('quantity field value must be integer or float type', 'price')
        elif not (quantity or quantity >= 1):
            raise ValueError('quantity field value must be greater then 1')
            
        cart_item = self.find_item(product, option_values)
        
        if cart_item:
            cart_item.update_quantity(quantity)

    def remove_item(self, product, option_values=[]):
        """
        To remove existing :class:`CartItem` object related to product.

        :param product: Unique id or name of :class:`Product` object or instance of :class:`Product`.
        :param option_values: Option values of the product(default []).
        """
        cart_item = self.find_item(product, option_values)
        if cart_item:
            self.__items.remove(cart_item)
            
    def remove_items(self):
        """
        To remove all existing :class:`CartItem` objects.
        """
        self.__items = list()

    def find_item(self, product, option_values=[]):
        """
        To find :class:`CartItem` object related to product.
        
        :param product: Unique id or name of :class:`Product` object or instance of :class:`Product`.
        :param option_values: Option values of the product(default []).
        :return: :class:`CartItem` object if cart item is exist else None.
        """
        product = id_from_object(product)
        option_values = get_list_of_ids(option_values)
        for cart_item in self.__items:
            cart_product = id_from_object(cart_item.product)
            if not cmp(cart_product, product):
                if option_values:
                    if not cart_item.has_options:
                        continue
                    cart_item_option_values = []
                    cart_item_options = get_dict_of_ids(cart_item.get_options())
                    for option, option_value in cart_item_options.items():
                        if isinstance(option_value, dict):
                            option_value = option_value.keys()[0]
                        cart_item_option_values.append(option_value)
                    if not cmp(option_values, cart_item_option_values):
                        return cart_item
                else:
                    if not cart_item.has_options:
                        return cart_item
        return None

    def get_items(self):
        """
        :return: List of :class:`CartItem` objects.
        """
        return self.__items

    def add_discount(self, amount, type='percentage'):
        """
        To apply discount.
        
        :param amount: Discount amount.
        :param type: Discount type like 'percentage' or 'amount'(default amount).
        """
        self.__discounts.append({'amount': amount, 'type': type})
            
    def remove_discounts(self):
        """
        To remove all applied discounts.
        """
        self.__discounts = list()
        
    def get_discounts(self):
        """
        :return: List of applied discounts.
        """
        return self.__discounts
        
    def add_tax(self, amount, type='percentage'):
        """
        To apply taxes.
        
        :param tax: Tax amount according to country region.
        :param type: Tax type like 'percentage' or 'fixed'(default percentage).

        :return: True if tax is applied and tax is already exist then False.
        """
        if not isinstance(amount, (int, float)):
            raise TypeError('tax field value must be integer or float type', 'price')
            
        if type not in ('percentage', 'fixed'):
            raise ValueError('type field value must be `percentage` or `fixed`', 'type')
        
        tax_exist = self.find_tax(amount, type)
        if not tax_exist:
            self.__taxes.append({'amount': amount, 'type': type})
            return True
            
        return False
        
    def remove_tax(self, amount, type='percentage'):
        """
        To remove existing tax.
        
        :param amount: Tax amount according to country region.
        :param type: Tax type like 'percentage' or 'fixed'(defualt percentage).
        """
        if not isinstance(amount, (int, float)):
            raise TypeError('tax field value must be integer or float type', 'price')
        tax_exist = self.find_tax(amount, type)
        if tax_exist:
            self.__taxes.remove({'amount': amount, 'type': type})
            return True
            
        return False
        
    def remove_taxes(self):
        """
        To remove all applied taxes.
        """
        self.__taxes = list()

    def find_tax(self, amount, type='percentage'):
        """
        To find applied tax.
        
        :param amount: Tax amount according to country region.
        :param type: Tax type like 'percentage' or 'fixed'(defualt percentage).
        :return: True if tax is exist else False.
        """
        if {'amount': amount, 'type': type} in self.__taxes:
            return True
            
        return False

    def get_taxes(self):
        """
        :return: list of applied taxes.
        """
        taxes = []
        for cart_item in self.get_items():
            taxes.extend(cart_item.get_taxes())
        taxes.extend(self.__taxes)
        return taxes

    def sub_total(self):
        """
        :return: Total cart amount(without discount deduction).
        """
        total = 0.0
        
        for cart_item in self.__items:
            total += cart_item.sub_total()
        return round(total, self.price_accuracy)
        
    def total_discount(self):
        """
        :return: Total discount amount.
        """
        total_discount = 0.0
        
        for cart_item in self.get_items():
            total_discount += cart_item.discount_amount()
        return round(total_discount, self.price_accuracy)

    def total_untaxed_amount(self):
        """
        :return: Untaxed amount after deducating discount amount.
        """
        total_untaxed_amount = self.sub_total() - self.total_discount()
        if self.tax_type == 'included':
            total_untaxed_amount -= self.total_tax()
        return round(total_untaxed_amount, self.price_accuracy)

    def total_tax(self):
        """
        :return: Total tax amount.
        """
        total_tax = 0.0
        
        if self.tax_type == 'included':
            total = self.sub_total() - self.total_discount()
        else:
            total = self.total_untaxed_amount()
        total_tax = calculate(total, self.__taxes, self.tax_type, self.currency_rate, self.price_accuracy)
        for cart_item in self.get_items():
            total_tax += cart_item.tax_amount()
        return round(total_tax, self.price_accuracy)

    def total(self):
        """
        :return: Total amount(`tax excluded` or `tax included`) by adding total untaxed amount, total tax and shipping charge.
        """

        return round(self.total_untaxed_amount() + self.total_tax() + self.shipping_charge, self.price_accuracy)

    def count(self):
        """
        :return: Total quantity.
        """
        self.total_items=0
        
        for cart_item in self.get_items():
            self.total_items += cart_item.quantity
            
        return self.total_items
            
    def clear(self):
        """
        To clean :class:`Cart` Object.
        """
        self.__intiallize()        
        
    @property
    def is_empty(self):
        """
        :return: True if cart has an item else False.
        """
        if self.__items:
            return False
            
        return True        
        
    @property
    def is_discount_applied(self):
        """
        :return: True if discount is applied else False.
        """
        if self.__discounts:
            return True
            
        return False
        
    @property
    def has_taxes(self):
        """
        :return: True if tax is applied else False.
        """
        if self.get_taxes():
            return True
        return False

    def _get__shipping_charge(self):
        """
        :return: Shipping charge.
        """
        return round(self.__shipping_charge * self.currency_rate, self.price_accuracy)

    def _set__shipping_charge(self, value):
        """
        To set shipping charge amount.
        
        :param value: Shipping charge amount.
        """
        self.__shipping_charge = value
    
    shipping_charge = property(_get__shipping_charge, _set__shipping_charge)    

class CartItem(object):
    """
    Collection of :class:`Product` and it's quantity, taxes and options.
    """
    
    def __init__(self, cart, product, price, quantity, taxes=[], options={}):
        """
        :param cart: Instance of :class:`Cart`.
        :param product: Unique id or name of :class:`Product` object or instance of :class:`Product`.
        :param price: Product price.
        :param quantity: Product quantity.
        :param taxes: Taxes(default []).
        :param options: Options(default {}).
        """
        for tax in taxes:
            if not isinstance(tax, dict):
                raise TypeError('taxes should be list of `dict` type value', 'taxes')
        self.product = product
        self.__price = price
        self.quantity = quantity
        self.__taxes = taxes
        self.__options = options
        self.__cart = cart
                
    def update_quantity(self, quantity):
        """
        To update existing quantity related to :class:`Product` object.
        
        :param quantity: Product quantity.
        """
        self.quantity = quantity
        
    def get_options(self):
        """
        :return:  Dict of product's option.
        """
        for option, option_value in self.__options.items():
            if isinstance(option_value, dict):
               for key, value in option_value.items():
                   if value.has_key('price'):
                        value['price'] =  round(value['price'] * self.__cart.currency_rate, self.__cart.price_accuracy)
        return self.__options
        
    def get_taxes(self):
        """
        :return: List of applied taxes.
        """
        return self.__taxes

    def sub_total(self):
        """
        :return: Total amount by multiplying product price and quantity(without discount deduction).
        """
        price = self.price
        for option, option_value in self.get_options().items():
            if isinstance(option_value, dict):
               for key, value in option_value.items():
                   if value.has_key('price'):
                        price += value['price']
        return round(price * self.quantity, self.__cart.price_accuracy)
        
    def discount_amount(self):
        """
        :return: Discount amount.
        """
        discount_amount = 0.0
        sub_total = self.sub_total()
        
        for discount in self.__cart.get_discounts():
            if discount['type'] == 'percentage':
                discount_amount += round(sub_total * (float(discount['amount'])/100), self.__cart.price_accuracy)
            elif discount['type'] == 'amount':
                discount_amount += round(float(discount['amount']) * self.__cart.currency_rate, self.__cart.price_accuracy)
                
        return round(discount_amount, self.__cart.price_accuracy)

    def untaxed_amount(self):
        """
        :return: Untaxed amount(after deducating discount amount).
        """
        total = self.sub_total() - self.discount_amount()

        if self.__cart.tax_type == 'included':
            total -= self.tax_amount()
        
        return round(total, self.__cart.price_accuracy)

    def tax_amount(self):
        """
        :return: Tax amount.
        """
        tax_amount = 0.0
        
        if self.__cart.tax_type == 'included':
            total = self.sub_total() - self.discount_amount()
        else:
            total = self.untaxed_amount()
        tax_amount = calculate(total, self.__taxes, self.__cart.tax_type, self.__cart.currency_rate, self.__cart.price_accuracy)    
        return tax_amount

    def total(self):
        """
        :return: Total amount(`tax excluded` or `tax included`) by adding untaxed and taxed amount.
        """
        return round(self.untaxed_amount() + self.tax_amount(), self.__cart.price_accuracy)
            
    @property
    def has_options(self):
        """
        :return: True if product has an option else False.
        """
        if self.__options:
            return True
        return False
    
    @property
    def has_taxes(self):
        """
        :return: True if product has tax else False.
        """    
        if self.__taxes:
            return True
        return False

    def _get_price(self):
        """
        :return: Price by multiplying currency rate.
        """
        return round(self.__price * self.__cart.currency_rate, self.__cart.price_accuracy)

    def _set_price(self, value):
        """
        To set product price.
        
        :param value: Product price.
        """
        self.__price = value

    price = property(_get_price, _set_price)
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
