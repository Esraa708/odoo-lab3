from odoo import models, fields
# from datetime import datetime


class PatientLog(models.Model):
    _name = "patient_log"
    created_by = fields.Many2one('res.users', 'Created By', default=lambda self: self.env.user)
    patient_idd = fields.Many2one(comodel_name="hms")
    date = fields.Datetime(string="Date", default=fields.datetime.now())
    description = fields.Text(string="Description")
