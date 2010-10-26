import os
from setuptools import setup

execfile(os.path.join('shoppingCart', 'release.py'))

setup(
    name='shoppingCart',
    packages=["shoppingCart"],
    version=version,
    description=description,
    long_description=long_description,
    author=author,
    author_email=author_email,
    url=url,
    classifiers=classifiers,
    license=license,
    platforms='any',
    keywords='cart  shopcart shoppingcart e-shop e-shopcart e-shoppingCart',
    include_package_data=True,
    namespace_packages=['shoppingCart'],
    zip_safe=False
)
