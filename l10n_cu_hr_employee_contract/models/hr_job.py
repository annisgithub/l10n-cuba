# -*- coding: utf-8 -*-
from odoo import fields, models, api
from datetime import timedelta

class Hrjob(models.Model):
    _inherit = 'hr.job'

    designation = fields.Boolean(string='Designation')





