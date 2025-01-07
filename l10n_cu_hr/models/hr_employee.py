# -*- coding: utf-8 -*-
from odoo import fields, models, api
import re


class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    _rec_name = 'full_name'


    res_private_municipality_id = fields.Many2one('res.municipality', 'Private Municipality',
                                                  domain="[('state_id', '=', private_state_id)]", help="Mucipality of Cuba" )

    private_country_id = fields.Many2one("res.country",
                                         string="Private Country",
                                         groups="hr.group_hr_user",
                                         default=lambda self: self.env['res.country'].search([('code', '=', 'CU')], limit=1).id)

    personal_street = fields.Char(string="Personal Street", groups="hr.group_hr_user")
    personal_street2 = fields.Char(string="Personal Street2", groups="hr.group_hr_user")
    personal_city = fields.Char(string="Personal City", groups="hr.group_hr_user")
    personal_state_id = fields.Many2one("res.country.state", string="Personal State",
                                        domain="[('country_id', '=?', personal_country_id)]",
                                        groups="hr.group_hr_user")
    personal_zip = fields.Char(string="Personal Zip", groups="hr.group_hr_user")
    personal_country_id = fields.Many2one("res.country",
                                          string="Personal Country",
                                          groups="hr.group_hr_user",
                                          default=lambda self: self.env['res.country'].search([('code', '=', 'CU')], limit=1).id)
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
    last_name = fields.Char(string="First name", groups="hr.group_hr_user")
    second_last_name = fields.Char(string="Second name", groups="hr.group_hr_user")
    full_name = fields.Char(string='Full Name', compute='_compute_full_name', store=True)
    number = fields.Char(string="Number", groups="hr.group_hr_user")

    schooling_level_id = fields.Many2one('schooling.level', string='Schooling Level',
                                         ondelete='restrict')
    occupational_category_id = fields.Many2one('occupational.category',
                                               string='Occupational Category', ondelete='restrict')
    profession_id = fields.Many2one('profession', string='Profession', ondelete='restrict')

    job_id = fields.Many2one(tracking=True,
                             domain="[('department_id', '=', department_id)]")

    identification_id = fields.Char(string='Identification No', groups="hr.group_hr_user", tracking=True)



    skin_color = fields.Selection([
        ('white', 'White'),
        ('mixed', 'Mixed'),
        ('black', 'Black')
    ], string='Skin Color',help='Color of the skin employee', default='mixed')

    political_affiliation = fields.Selection([
        ('pcc', 'PCC'),
        ('ujc', 'UJC')
    ], string='Political Affiliation',help='Political affiliation of employee')


    @api.onchange('identification_id')
    def _onchange_name(self):
        patron = r'^\d{11}$'
        if self.identification_id:
            if not re.match(patron, self.identification_id):
                raise models.ValidationError(
                    "¡El formato del número de identidad debe ser de 11 digitos")
    @api.onchange('number')
    def _onchange_name(self):
        patron = r'^\d{5}$'
        if self.number:
            if not re.match(patron, self.number):
                raise models.ValidationError(
                    "¡El código del empleado debe ser de 5 digitos")

    @api.depends('name', 'last_name', 'second_last_name')
    def _compute_full_name(self):
        for record in self:
            record.full_name = f"{record.name} {record.last_name or ''} {record.second_last_name or ''}".strip()
    #
    # @api.onchange('job_id')
    # def _onchange_job(self):
    #     for record in self:
    #         record.department_id = record.job_id.department_id

    @api.onchange('department_id')
    def _onchange_department(self):
        for record in self:
            record.job_id = False
