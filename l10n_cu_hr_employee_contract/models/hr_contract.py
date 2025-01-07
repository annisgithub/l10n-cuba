# -*- coding: utf-8 -*-
from odoo import fields, models, api,_
from datetime import timedelta
from odoo.exceptions import ValidationError, UserError
from dateutil.relativedelta import relativedelta
from datetime import date
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

    job_id = fields.Many2one('hr.job', 'Job Position',domain="[('department_id', '=', department_id)]",
                             check_company=True)

    wage = fields.Monetary('Wage', compute="_compute_job",
                           tracking=True, help="Employee's monthly gross wage.",
                           group_operator="avg", store=True)

    determined_contract_type_id = fields.Many2one('determined.contract.type', string='Determined Contract Type',
                                                  ondelete='restrict')

    number_of_days = fields.Integer(string='Number of days', default=0)

    date_end = fields.Date(string='End Date', tracking=True,
        help="End date of the contract (if it's a fixed-term contract).",compute='_compute_end_date', store=True)

    occupational_category_id = fields.Many2one('occupational.category',
                                               string='Occupational Category',
                                               compute='_compute_job', ondelete='restrict',
                                               store=True)

    skip_compute_date_end = fields.Boolean(string='Skip Compute', default=False)

    def unlink(self):
        for contract in self:
            if contract.contract_state == 'open':
                raise UserError('No se puede eliminar un contrato confirmado.')
        return super(HrContract, self).unlink()

    @api.constrains('contract_state')
    def _check_state(self):
        '''
        Valida el estado de los contratos
        '''
        # Check for open contracts
        open_contracts = self.search([
            ('contract_state', '=', 'open'),
            ('company_id', '=', self.company_id.id),
            ('employee_id', '=', self.employee_id.id),
            ('id', '!=', self.id)
        ])
        if open_contracts and self.contract_state == 'open':
            raise ValidationError(_('Solo puede haber un contrato aprobado para este empleado.'))

        # Check for overlapping dates
        overlapping_contracts = self.search([
            ('company_id', '=', self.company_id.id),
            ('employee_id', '=', self.employee_id.id),
            ('id', '!=', self.id),
            ('contract_state', '!=', 'close'),
            ('date_start', '=', self.date_start)
        ])
        if overlapping_contracts:
            raise ValidationError(_('Las fechas de inicio no pueden solaparse con otros contratos activos del empleado.'))


    @api.depends('employee_id')
    def _compute_employee_contract(self):
        for contract in self.filtered('employee_id'):
            contract.contract_type_id = contract.job_id.contract_type_id
        return super(HrContract, self)._compute_employee_contract()

    @api.onchange('department_id')
    def _onchange_department(self):
        for record in self:
            record.job_id = False
    @api.depends('job_id')
    def _compute_job(self):
        for record in self.filtered('job_id'):
            record.wage = record.job_id.wage if record.job_id and record.wage <= 0 else record.wage
            record.occupational_category_id = record.job_id and record.job_id.occupational_category_id


    @api.constrains('wage')
    def _check_wage(self):
        for record in self:
            if record.wage <= 0.00:
                raise ValidationError(_("The basic salary must be greater than 0.00."))

    @api.model
    def _expand_contract_states(self, states, domain, order):
        return [key for key, val in type(self).contract_state.selection]

    @api.depends('date_start', 'number_of_days', 'contract_type')
    def _compute_end_date(self):
        for record in self:
            if record.date_start and record.number_of_days:
                if record.contract_type == 'determinado' and record.contract_state == 'draft':
                    start_date = fields.Date.from_string(record.date_start)
                    record.date_end = start_date + timedelta(days=record.number_of_days - 1)
                elif record.contract_type == 'indeterminado'\
                        and record.contract_state == 'draft':
                    record.date_end = False if not record.skip_compute_date_end else record.date_end
                    record.determined_contract_type_id = False
                    record.number_of_days = 0
            else:
                record.date_end = False if not record.skip_compute_date_end else record.date_end

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

    def _assign_contract(self, vals):
        old_state = {c.id: c.contract_state for c in self}
        res = super(HrContract, self).write(vals)
        new_state = {c.id: c.contract_state for c in self}
        if vals.get('contract_state') == 'open':
            self._assign_open_contract()
        today = fields.Date.today()
        for contract in self:
            if contract == contract.sudo().employee_id.contract_id \
                and old_state[contract.id] == 'open' \
                and new_state[contract.id] != 'open':
                running_contract = self.env['hr.contract'].search([
                    ('employee_id', '=', contract.employee_id.id),
                    ('company_id', '=', contract.company_id.id),
                    ('contract_state', '=', 'open'),
                ]).filtered(lambda c: c.date_start <= today and (not c.date_end or c.date_end >= today))
                if running_contract:
                    contract.employee_id.sudo().contract_id = running_contract[0]
        if vals.get('contract_state') == 'close':
            for contract in self.filtered(lambda c: not c.date_end):
                contract.date_end = max(date.today(), contract.date_start)
        date_end = vals.get('date_end')
        if self.env.context.get('close_contract', True) and date_end and fields.Date.from_string(date_end) < fields.Date.context_today(self):
            for contract in self.filtered(lambda c: c.contract_state == 'open'):
                contract.contract_state = 'close'

        calendar = vals.get('resource_calendar_id')
        if calendar:
            self.filtered(
                lambda c: c.contract_state == 'open' or (c.contract_state == 'draft' and c.kanban_state == 'done' and c.employee_id.contracts_count == 1)
            ).mapped('employee_id').filtered(
                lambda e: e.resource_calendar_id
            ).write({'resource_calendar_id': calendar})

        if 'contract_state' in vals and 'kanban_state' not in vals:
            self.write({'kanban_state': 'normal'})

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self._prepare_contract_name(vals)
            if 'wage' not in vals:
                job = self.env['hr.job'].browse(vals.get('job_id',None))
                vals['wage'] = job and job.wage
        contracts = super().create(vals)
        contracts.filtered(lambda c: c.contract_state == 'open')._assign_open_contract()
        open_contracts = contracts.filtered(
            lambda c: c.contract_state == 'open' or (c.contract_state == 'draft' and c.kanban_state == 'done' and c.employee_id.contracts_count == 1)
        )
        # sync contract calendar -> calendar employee
        for contract in open_contracts.filtered(lambda c: c.employee_id and c.resource_calendar_id):
            contract.employee_id.resource_calendar_id = contract.resource_calendar_id
        return contracts

    def write(self, vals):
        for record in self:
            if vals.get('contract_type') or vals.get('job_id'):
                vals['name'] = self._prepare_contract_name(vals, record)
            self._assign_contract(vals)
        return super(HrContract, self).write(vals)

    def print_contract_proforma(self):
        return self.env.ref('l10n_cu_hr_employee_contract.action_report_contract').report_action(self)

    def print_supplier_contract(self):
        return self.env.ref('l10n_cu_hr_employee_contract.action_report_supplier_contract'). \
            report_action(self)

    def print_expiring_contracts_report(self):
        """
        This function finds all 'open' fixed-term contracts that are due to expire within
         a month and generates a report.
        """
        today = fields.Date.today()
        next_month = today + timedelta(days=30)

        expiring_contracts = self.search([
            ('contract_state', '=', 'open'),
            ('date_end', '<=', next_month),
            ('date_end', '>=', today),
            ('contract_type', '=', 'determinado')
        ])
        if not expiring_contracts:
            raise ValidationError(
                _('There is not any contract next to expiry'))
        else:
            return self.env.ref('l10n_cu_hr_employee_contract.report_fixed_term_contract_action') \
                .report_action(expiring_contracts)

    @api.model
    def update_state(self):
        from_cron = 'from_cron' in self.env.context
        companies = self.env['res.company'].search([])
        contracts = self.env['hr.contract']
        work_permit_contracts = self.env['hr.contract']
        for company in companies:
            contracts += self.search([
                ('contract_state', '=', 'open'), ('contract_type','=','determinado'), ('kanban_state', '!=', 'blocked'), ('company_id', '=', company.id),
                '&',
                ('date_end', '<=', fields.date.today() + relativedelta(days=company.contract_expiration_notice_period)),
                ('date_end', '>=', fields.date.today() + relativedelta(days=1)),
            ])

            work_permit_contracts += self.search([
                ('contract_state', '=', 'open'), ('kanban_state', '!=', 'blocked'), ('company_id', '=', company.id),
                '&',
                ('employee_id.work_permit_expiration_date', '<=', fields.date.today() + relativedelta(days=company.work_permit_expiration_notice_period)),
                ('employee_id.work_permit_expiration_date', '>=', fields.date.today() + relativedelta(days=1)),
            ])

        for contract in contracts:
            contract.with_context(mail_activity_quick_update=True).activity_schedule(
                'mail.mail_activity_data_todo', contract.date_end,
                _("The contract of %s is about to expire.", contract.employee_id.name),
                user_id=contract.hr_responsible_id.id or self.env.uid)
            contract.message_post(
                body=_(
                    "According to the contract's end date, this contract has been put in red on the %s. Please advise and correct.",
                    fields.Date.today()
                )
            )

        for contract in work_permit_contracts:
            contract.with_context(mail_activity_quick_update=True).activity_schedule(
                'mail.mail_activity_data_todo', contract.date_end,
                _("The work permit of %s is about to expire.", contract.employee_id.name),
                user_id=contract.hr_responsible_id.id or self.env.uid)
            contract.message_post(
                body=_(
                    "According to Employee's Working Permit Expiration Date, this contract has been put in red on the %s. Please advise and correct.",
                    fields.Date.today()
                )
            )

        if contracts:
            contracts._safe_write_for_cron({'kanban_state': 'blocked'}, from_cron)
        if work_permit_contracts:
            work_permit_contracts._safe_write_for_cron({'kanban_state': 'blocked'}, from_cron)

        contracts_to_close = self.search([
            ('contract_state', '=', 'open'),('contract_type','=','determinado'),
            '|',
            ('date_end', '<=', fields.Date.to_string(date.today())),
            ('employee_id.work_permit_expiration_date', '<=', fields.Date.to_string(date.today())),
        ])

        if contracts_to_close:
            contracts_to_close._safe_write_for_cron({'contract_state': 'close'}, from_cron)

        contracts_to_open = self.search([('contract_state', '=', 'draft'), ('kanban_state', '=', 'done'), ('date_start', '<=', fields.Date.to_string(date.today())),])

        if contracts_to_open:
            contracts_to_open._safe_write_for_cron({'state': 'open'}, from_cron)

        contract_ids = self.search([('date_end', '=', False), ('contract_state', '=', 'close'), ('employee_id', '!=', False)])
        # Ensure all closed contract followed by a new contract have a end date.
        # If closed contract has no closed date, the work entries will be generated for an unlimited period.
        for contract in contract_ids:
            next_contract = self.search([
                ('employee_id', '=', contract.employee_id.id),
                ('contract_state', 'not in', ['close', 'draft']),
                ('date_start', '>', contract.date_start)
            ], order="date_start asc", limit=1)
            if next_contract:
                contract._safe_write_for_cron({'date_end': next_contract.date_start - relativedelta(days=1)}, from_cron)
                continue
            next_contract = self.search([
                ('employee_id', '=', contract.employee_id.id),
                ('date_start', '>', contract.date_start)
            ], order="date_start asc", limit=1)
            if next_contract:
                contract._safe_write_for_cron({'date_end': next_contract.date_start - relativedelta(days=1)}, from_cron)

        return True






