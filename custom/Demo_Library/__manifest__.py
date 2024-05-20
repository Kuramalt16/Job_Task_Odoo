# __manifest__.py
{
    'name': 'Book Registry',
    'version': '1.0',
    'summary': 'Module for managing a library of books',
    'description': 'A simple module to manage a registry of books',
    'author': 'Your Name',
    'depends': ['base'],
    'data': [
        'views/book_views.xml',
    ],
    'installable': True,
    'application': True,
}
