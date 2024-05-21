# models/book.py
from odoo import models, fields

class BookRegistry(models.Model):
    _name = 'book.registry'
    _description = 'Book Registry'
    _rec_name = 'book_name'

    book_name = fields.Char(string='Title', required=True)
    summary = fields.Char(string='Summary', required=True)
    num_of_pages = fields.Integer(string='Number of Pages')
    genre = fields.Char(string='Genre', required=True)