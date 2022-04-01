# -*- coding: utf-8 -*-
{
    'name': "RadiantDessert",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "BMS Tech",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Administration',
    'version': '0.1',
    'application':True,

    # any module necessary for this one to work correctly
    'depends': ['base','sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/navbar.xml',
        'views/drinks_views.xml',
        'views/package_views.xml',
        'views/icecream_views.xml',
        'views/waffles_views.xml',
        'views/order_views.xml',
        'views/employee_views.xml',
        'views/customer_views.xml',
        'views/payment_views.xml',
        'views/accounting_views.xml',
        'report/report.xml',
        'report/invoice_report.xml',
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
