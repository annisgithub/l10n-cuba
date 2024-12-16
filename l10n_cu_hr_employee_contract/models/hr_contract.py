# -*- coding: utf-8 -*-
from odoo import fields, models, api,_
from datetime import timedelta

class HrContract(models.Model):
    _inherit = 'hr.contract'

    name = fields.Char(string='Contract Reference', required=True,
                       default=_('New'), readonly=True)
    contract_state = fields.Selection([
        ('draft', 'New'),
        ('open', 'Running'),
        ('close', 'Expired')
    ], string='Status', group_expand='_expand_contract_states', copy=False,
        tracking=True, help='Status of the contract', default='draft')

    contract_type = fields.Selection([('indeterminado', 'Indeterminado'), ('determinado', 'Determinado')],
                                        default="indeterminado",string="Contract Type")
    contract_type_id = fields.Many2one('hr.contract.type', "Other Contract Type", tracking=True)
    determined_contract_type_id = fields.Many2one('determined.contract.type', string='Determined Contract Type',
                                                  ondelete='restrict',check_company=True)


    number_of_days = fields.Integer(string='Number of days', default=0)

    date_end = fields.Date(string='End Date', tracking=True,
        help="End date of the contract (if it's a fixed-term contract).",compute='_compute_end_date', store=True)


    @api.depends('employee_id')
    def _compute_employee_contract(self):
        for contract in self.filtered('employee_id'):
            contract.contract_type_id = contract.job_id.contract_type_id
        return super(HrContract, self)._compute_employee_contract()

    @api.model
    def _expand_contract_states(self, states, domain, order):
        return [key for key, val in type(self).contract_state.selection]

    @api.depends('date_start', 'number_of_days', 'contract_type')
    def _compute_end_date(self):
        for record in self:
            if record.date_start and record.number_of_days:
                if record.contract_type == 'determinado':
                    start_date = fields.Date.from_string(record.date_start)
                    record.date_end = start_date + timedelta(days=record.number_of_days - 1)
                elif record.contract_type == 'indeterminado':
                    record.date_end = False
                    record.number_of_days = 0
            else:
                record.date_end = False

    @api.model
    def get_sequence_prefix(self,designation):
        return 'DESIG' if designation else 'CONT'

    @api.model
    def get_sequence_suffix(self,contract_type,designation):
        return ('IND' if contract_type == 'indeterminado' else 'DET') if not designation else ''


    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            sequence = self.env['ir.sequence'].next_by_code('hr.contract') or _('New')
            contract_type = vals.get('contract_type')
            job_id = vals.get('job_id')
            job = self.env['hr.job'].browse(job_id) if job_id else False
            designation = job.designation if job else False
            prefix = self.get_sequence_prefix(designation)
            suffix = self.get_sequence_suffix(contract_type,designation)
            vals['name'] = str(sequence).replace('CONTRACT_PREFIX',prefix).replace('SUFFIX_VALUE',suffix)
        return super(HrContract, self).create(vals)

    def write(self, vals):
        for record in self:
            contract_type = vals.get('contract_type') if vals.get('contract_type',False) else record.contract_type
            job = self.env['hr.job'].browse(vals.get('job_id')) if vals.get('job_id',False) else record.job_id
            designation = job.designation if job else False
            prefix = self.get_sequence_prefix(designation)
            suffix = self.get_sequence_suffix(contract_type,designation)
            if vals.get('contract_type',False):
                sequence = self.env['ir.sequence'].next_by_code('hr.contract') or _('New') if record.name == '' else record.name
                new_sequence = str(sequence).split('/')
                if record.name != '' and len(new_sequence) > 2:
                    sequence = prefix+'/'.join(new_sequence[1:len(new_sequence)-1])+'/'+suffix
                else:
                    sequence = self.env['ir.sequence'].next_by_code('hr.contract')
                vals['name'] = str(sequence).replace('CONTRACT_PREFIX',prefix).replace('SUFFIX_VALUE',suffix)
        res = super(HrContract, self).write(vals)
        return res





