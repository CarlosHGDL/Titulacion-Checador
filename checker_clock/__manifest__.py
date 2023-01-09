# -*- coding: utf-8 -*-
{
    'name': "checker_clock",

    'summary': """
       Employee entry and exit control system """,

    'description': """
        Entry and exit control system for unedel teachers as well as some reports
    """,

    'author': "Carlos Hermosillo gutierrez",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','portal','website'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'report/classroom_qr.xml',
        'report/reporte_inasistencias.xml',
        'views/colony_catalog.xml',
        'views/teacher.xml',
        'views/subject.xml',
        'views/views.xml',
        'views/schedule.xml',
        'views/reporte_inasistencias.xml',
        'views/campuses.xml',
        'views/classroom.xml',
        'views/templates.xml',
        'views/justification.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}