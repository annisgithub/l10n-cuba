# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import ValidationError

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    occupational_category_id = fields.Many2one('occupational.category',
                                               string='Occupational Category',
                                               compute='_compute_job', ondelete='restrict',check_company=True)
    currency_id = fields.Many2one(string="Currency", related='company_id.currency_id', readonly=True)

    wage = fields.Monetary('Wage', required=True, tracking=True,
                           compute='_compute_job',
                           help="Employee's monthly gross wage.",
                           group_operator="avg")

    @api.depends('job_id')
    def _compute_job(self):
        for record in self.filtered('job_id'):
            record.wage = record.job_id.wage
            record.occupational_category_id = record.job_id.occupational_category_id
        return True

    @api.constrains('wage')
    def _check_wage(self):
        for record in self:
            if record.wage <= 0.00:
                raise ValidationError("The basic salary must be greater than 0.00.")



