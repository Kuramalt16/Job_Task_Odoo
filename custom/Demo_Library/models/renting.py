# models/book.py
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date
import logging

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
    days_late = fields.Integer(string="Days Late", compute='_compute_days_late')

    @api.depends('end_of_rent')
    def _compute_days_late(self):
        today = date.today()
        for record in self:
            if record.end_of_rent and record.end_of_rent < today:
                record.days_late = (today - record.end_of_rent).days
            else:
                record.days_late = 0

    def scheduled_Late_messaging(self):
        today = date.today()
        for record in self.env['rent.books'].search([]):
            if record.end_of_rent and record.end_of_rent < today:
                template_id = self.env.ref('Demo_Library.reminder_mail_template').id
                self.env['mail.template'].browse(template_id).send_mail(record.id, force_send=True)

    def action_cancel_rent(self):
        for record in self:
            if record.state_of_rent == "reserved":
                record.state_of_rent = 'canceled'
            else:
                raise ValidationError('Cant cancel non existing orders')

    def action_return_book(self):
        for record in self:
            if record.state_of_rent == "rented":
                record.state_of_rent = 'returned'
            else:
                raise ValidationError('Cant return things that are not taken')

    @api.constrains('start_of_rent')
    def update_rent_list(self):
        today = date.today()
        for record in self:
            if record.start_of_rent and record.start_of_rent <= today:
                record.state_of_rent = "rented"
            elif record.start_of_rent and record.start_of_rent >= today:
                record.state_of_rent = "reserved"

    @api.constrains('start_of_rent', 'end_of_rent')
    def _check_rent_dates(self):
        for record in self:
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
                raise ValidationError(record.rented_book_id.book_name + ' is already rented for the selected period. (From: ' + str(record.start_of_rent) + ' Until: ' + str(record.end_of_rent) + ')')

