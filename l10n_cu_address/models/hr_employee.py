# -*- coding: utf-8 -*-
from odoo import fields, models, api

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    res_private_municipality_id = fields.Many2one('res.municipality', 'Private Municipality',
                                                  domain="[('state_id', '=', private_state_id)]", help="Mucipality of Cuba" )



    personal_street = fields.Char(string="Personal Street", groups="hr.group_hr_user")
    personal_street2 = fields.Char(string="Personal Street2", groups="hr.group_hr_user")
    personal_city = fields.Char(string="Personal City", groups="hr.group_hr_user")
    personal_state_id = fields.Many2one(
        "res.country.state", string="Personal State",
        domain="[('country_id', '=?', personal_country_id)]",
        groups="hr.group_hr_user")
    personal_zip = fields.Char(string="Personal Zip", groups="hr.group_hr_user")
    personal_country_id = fields.Many2one("res.country", string="Personal Country", groups="hr.group_hr_user")
    personal_phone = fields.Char(string="Personal Phone", groups="hr.group_hr_user")
    personal_email = fields.Char(string="Personal Email", groups="hr.group_hr_user")
    res_personal_municipality_id = fields.Many2one('res.municipality', 'Personal Municipality',
                                              domain="[('state_id', '=', personal_state_id)]", help="Mucipality of Cuba")

    state_of_birth_id = fields.Many2one(
        "res.country.state", string="State of Birth",
        domain="[('country_id', '=?', country_of_birth)]",
        groups="hr.group_hr_user")

    municipality_of_birth_id = fields.Many2one(
        'res.municipality', string='Municipality of birth',
        domain="[('state_id', '=', state_of_birth_id)]",
        groups="hr.group_hr_user")
