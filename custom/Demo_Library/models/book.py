# models/book.py
from odoo import models, fields

class BookRegistry(models.Model):
    _name = 'book.registry'
    _description = 'Book Registry'

    name = fields.Char(string='Title', required=True)
    author = fields.Char(string='Author', required=True)
    publication_date = fields.Date(string='Publication Date')
    isbn = fields.Char(string='ISBN')
    genre = fields.Char(string='Genre')