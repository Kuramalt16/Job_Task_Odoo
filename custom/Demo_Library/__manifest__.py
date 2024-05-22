# __manifest__.py
{
    'name': 'Book Registry',
    'version': '1.0',
    'summary': 'Module for managing a library of books',
    'description': 'A simple module to manage a registry of books',
    'author': 'Gytis',
    'license': 'AGPL-3',
    'depends': ['base', 'mail'],
    'data': [
        'data/cron.xml',
        'data/data.xml',
        'data/mail_template.xml',
        'security/ir.model.access.csv',
        'views/book_views.xml',
        'views/rent_views.xml',
        'reports/report.xml',
        'reports/Client_report.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
}
