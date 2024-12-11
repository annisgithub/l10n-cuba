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
     'depends': ["hr","hr_contract","l10n_cu_address","l10n_cu_hr"],
     'auto_install': True,     
     'data': [
          "views/payroll_movement_views.xml",
          "security/ir.model.access.csv"
     ],
     'license': 'LGPL-3',
}
