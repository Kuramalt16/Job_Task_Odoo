# models/book.py
from odoo import models, fields

class BookRegistry(models.Model):
    _name = 'book.registry'
    _description = 'Book Registry'

    name = fields.Char(string='Title', required=True)
    summary = fields.Char(string='Summary', required=True)
    num_of_pages = fields.Char(string='Number of Pages')
    genre = fields.Char(string='Genre')