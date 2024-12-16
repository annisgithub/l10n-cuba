# -*- coding: utf-8 -*-
from odoo import fields, models, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    _rec_name = 'full_name'

    last_name = fields.Char(string="First name", groups="hr.group_hr_user")
    second_last_name = fields.Char(string="Second name", groups="hr.group_hr_user")
    full_name = fields.Char(string='Full Name', compute='_compute_full_name', store=True)

    schooling_level_id = fields.Many2one('schooling.level', string='Schooling Level',
                                         ondelete='restrict',check_company=True)
    occupational_category_id = fields.Many2one('occupational.category',
                                               string='Occupational Category', ondelete='restrict',check_company=True)
    profession_id = fields.Many2one('profession', string='Profession', ondelete='restrict',check_company=True)


    skin_color = fields.Selection([
        ('white', 'White'),
        ('mixed', 'Mixed'),
        ('black', 'Black')
    ], string='Skin Color',help='Color of the skin employee', default='mixed')

    political_affiliation = fields.Selection([
        ('pcc', 'PCC'),
        ('ujc', 'UJC')
    ], string='Political Affiliation',help='Political affiliation of employee', default='ujc')

    @api.depends('name', 'last_name', 'second_last_name')
    def _compute_full_name(self):
        for record in self:
            record.full_name = f"{record.name} {record.last_name or ''} {record.second_last_name or ''}".strip()



