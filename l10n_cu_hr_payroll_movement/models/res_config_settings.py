from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    central_office = fields.Char('Central office')
    central_office_abbreviation = fields.Char('Central office abbreviation')
    business_group = fields.Char('Business group')
    abbreviation_group = fields.Char('Group abbreviation')
    ministry = fields.Char('Ministry')
    ministry_abbreviation = fields.Char('Ministry abbreviation')
    legal_address = fields.Char('Legal address')
    director = fields.Char('Director')
    job_id = fields.Char('Position')
    resolution = fields.Char('Resolution')
    phone = fields.Char('Phone')
    email = fields.Char('Email')
    employer = fields.Char('Footer page')
