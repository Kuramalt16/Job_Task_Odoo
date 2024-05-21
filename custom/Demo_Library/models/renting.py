# models/book.py
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date
import logging

def print_log(message):
    _logger = logging.getLogger(__name__)
    _logger.info(message)


class ResPartner_Inherit(models.Model):
    _inherit = 'res.partner'
    name = fields.Char(string='Name')

class BookRent(models.Model):
    _name = 'rent.books'
    _description = 'Rent'
    _rec_name = 'rented_book_id'

    rented_book_id = fields.Many2one('book.registry', string="Book", required=True)
    contact = fields.Many2one('res.partner', string="Contact", required=True)
    start_of_rent = fields.Date(string='Rent Start Date', required=True)
    end_of_rent = fields.Date(string='Rent End Date', required=True)
    state_of_rent = fields.Selection([
        ('reserved', 'Reserved'),
        ('rented', 'Rented'),
        ('returned', 'Returned'),
        ('canceled', 'Canceled'),
        ], default='rented', string="State")


    def Check_late_books(self):
        today = date.today()
        for record in self:
            print_log(record)
            print_log(record.state_of_rent)

    def action_cancel_rent(self):
        for record in self:
            if record.state_of_rent == "reserved":
                record.state_of_rent = 'canceled'
                print_log("pressed CANCEL")
                print_log(record.state_of_rent)
            else:
                raise ValidationError('Cant cancel non existing orders')

    def action_return_book(self):
        for record in self:
            if record.state_of_rent == "rented":
                record.state_of_rent = 'returned'
                print_log("pressed RETURN")
                print_log(record.state_of_rent)
            else:
                raise ValidationError('Cant return things that are not taken')

    @api.constrains('start_of_rent')
    def update_rent_list(self):
        today = date.today()
        for record in self:
            print_log("BOOK NAME and state: ")
            print_log(record.rented_book_id)
            print_log(record.state_of_rent)
            print_log(record.start_of_rent)
            print_log(today)
            if record.start_of_rent and record.start_of_rent <= today:
                record.state_of_rent = "rented"
            elif record.start_of_rent and record.start_of_rent >= today:
                record.state_of_rent = "reserved"
            print_log("BOOK After NAME and state: ")
            print_log(record.rented_book_id)
            print_log(record.state_of_rent)

    @api.constrains('start_of_rent', 'end_of_rent')
    def _check_rent_dates(self):
        today = date.today()
        for record in self:
            # if record.start_of_rent < today:
            #     raise ValidationError('We don''t rent books to time travelers')

            if record.start_of_rent > record.end_of_rent:
                raise ValidationError('Start date must be before the end date.')

            overlapping_rentals = self.env['rent.books'].search([
                ('rented_book_id', '=', record.rented_book_id.id),
                ('id', '!=', record.id),
                ('state_of_rent', 'in', ['rented', 'reserved']),
                ('start_of_rent', '<=', record.end_of_rent),
                ('end_of_rent', '>=', record.start_of_rent),
            ])

            if overlapping_rentals:
                raise ValidationError('The book is already rented for the selected period.')
