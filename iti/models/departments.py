from odoo import models, fields

class Department(models.Model):
    _name = "departments"
    name = fields.Char(required=True)
    capicity = fields.Integer()
    is_opened = fields.Boolean()
    # patient_id= fields.Many2one(comodel_name="hms")
    patient_id=fields.One2many(comodel_name="hms",inverse_name="department_id")

