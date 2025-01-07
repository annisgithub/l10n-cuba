# List of contributors:
# Segu

{
     'name': 'Cuba - HR Movimientos',
     'version': '17.0',
     'category': 'Human Resources',
     'summary': """
        Empleados, Movimientos de Nómina.
     """,
     'author': 'Comunidad Cubana de Odoo',
     'depends': ["l10n_cu_address","l10n_cu_hr","l10n_cu_hr_employee_contract"],
     'auto_install': True,     
     'data': [
          "views/details_movement_type_views.xml",
          "views/reasons_movement_type_views.xml",
          "views/hr_contract_views.xml",
          "views/payroll_movement_views.xml",
          "views/hr_employee_views.xml",
          "data/paperformat_global.xml",
          "data/details_movement_type_data.xml",
          "data/reasons_movement_type_data.xml",
          "reports/report_payroll_movement.xml",
          "security/ir.model.access.csv"
     ],
     'license': 'LGPL-3',

}
