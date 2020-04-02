from odoo import models, fields


class Doctor(models.Model):
    _name = "doctors"
    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    image = fields.Binary("Favicon", attachment=True,
                          help="patient page")
