# -*- coding: utf-8 -*-
from odoo import fields, models, api,_
from datetime import timedelta
from odoo.exceptions import ValidationError
class HrContract(models.Model):
    _inherit = 'hr.contract'

    name = fields.Char(string='Contract Reference', required=True,
                       default=lambda self: _('New'), readonly=True)
    contract_state = fields.Selection([
        ('draft', 'New'),
        ('open', 'Running'),
        ('close', 'Expired')
    ], string='Status', group_expand='_expand_contract_states', copy=False,
        tracking=True, help='Status of the contract', default='draft')

    contract_type = fields.Selection([('indeterminado', 'Indeterminado'), ('determinado', 'Determinado')],
                                        default="indeterminado",string="Contract Type")
    contract_type_id = fields.Many2one('hr.contract.type', "Other Contract Type",
                                       compute="_compute_employee_contract",
                                       tracking=True, store=True)

    wage = fields.Monetary('Wage', required=True, compute="_compute_employee_contract",
                           tracking=True, help="Employee's monthly gross wage.",
                           group_operator="avg", store=True)

    determined_contract_type_id = fields.Many2one('determined.contract.type', string='Determined Contract Type',
                                                  ondelete='restrict',check_company=True)


    number_of_days = fields.Integer(string='Number of days', default=0)

    date_end = fields.Date(string='End Date', tracking=True,
        help="End date of the contract (if it's a fixed-term contract).",compute='_compute_end_date', store=True)


    @api.depends('employee_id')
    def _compute_employee_contract(self):
        for contract in self.filtered('employee_id'):
            contract.contract_type_id = contract.job_id.contract_type_id
            contract.wage = contract.job_id.wage
        return super(HrContract, self)._compute_employee_contract()

    @api.constrains('wage')
    def _check_wage(self):
        for record in self:
            if record.wage <= 0.00:
                raise ValidationError("The basic salary must be greater than 0.00.")

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
                    record.determined_contract_type_id = False
                    record.number_of_days = 0
            else:
                record.date_end = False

    @api.model
    def get_sequence_prefix(self,designation):
        return 'DESIG' if designation else 'CONT'

    @api.model
    def get_sequence_suffix(self,contract_type,designation):
        return ('IND' if contract_type == 'indeterminado' else 'DET') if not designation else ''

    def _prepare_contract_name(self, vals, record=None):
        sequence_obj = self.env['ir.sequence']
        sequence = sequence_obj.next_by_code('hr.contract') or _('New')
        contract_type = vals.get('contract_type') or (record and record.contract_type)
        job_id = vals.get('job_id') or (record and record.job_id and record.job_id.id)
        job = self.env['hr.job'].browse(job_id) if job_id else False
        designation = job.designation if job else False
        prefix = self.get_sequence_prefix(designation)
        suffix = self.get_sequence_suffix(contract_type, designation)
        if record and record.name:
            new_sequence = record.name.split('/')
            if len(new_sequence) > 2:
                sequence = prefix+'/' + '/'.join(new_sequence[1:-1]) + '/' + suffix
                current_next = sequence_obj.search([('code', '=', 'hr.contract')], limit=1)
                next_number = current_next and int(current_next.number_next_actual) - 1
                sequence_obj.write({'number_next_actual': next_number})
        return str(sequence).replace('CONTRACT_PREFIX', prefix).replace('SUFFIX_VALUE', suffix)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self._prepare_contract_name(vals)
        return super(HrContract, self).create(vals)

    def write(self, vals):
        for record in self:
            if vals.get('contract_type') or vals.get('job_id'):
                vals['name'] = self._prepare_contract_name(vals, record)
        return super(HrContract, self).write(vals)







