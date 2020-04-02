from dateutil.relativedelta import relativedelta

from odoo import models, fields, api
import re
from datetime import datetime

from odoo.exceptions import ValidationError


class Hms(models.Model):
    _name = "hms"
    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    birth_date = fields.Date()
    history = fields.Html()
    cr_ratio = fields.Float()
    blooad_type = fields.Selection([('o', 'o'), ('A', 'a'), ('a+', 'a+')], default='o')
    status = fields.Selection([
        ('undetermined', 'undetermined'),
        ('fair', 'fair'),
        ('good', 'good'),
        ('serious', 'serious')
    ], default='undetermined')
    PCR = fields.Boolean()
    image = fields.Binary("Favicon", attachment=True,
                          help="patient page")
    address = fields.Char()
    age = fields.Char(compute="_compute_age")
    email = fields.Char()
    department_id = fields.Many2one(comodel_name="departments")
    doctor_ids = fields.Many2many(comodel_name="doctors")
    depaetment_capicity = fields.Integer(related="department_id.capicity")
    logs = fields.One2many(comodel_name="patient_log", inverse_name="patient_idd")
    # crm_patient_ids = fields.Many2one(comodel_name="res.partner")
    ccustomer_patient_ids = fields.One2many(comodel_name="res.partner", inverse_name="crm_patient_ids")


    # department_id=fields.One2many(comodel_name="departments",inverse_name="patient_id")
    #
    # @api.onchange('age')
    # def _onchange_age(self):
    #     if self.age < 30:
    #         print(self.PCR)
    #         self.PCR = True
    #         warning = {
    #             'title': 'Warning!',
    #             'message': 'PCR has been checked!'
    #         }
    #
    #         return {'warning': warning}
    #     else:
    #         self.PCR = False

    def change_patient_status(self):
        if (self.status == 'undetermined'):
            self.status = 'fair'
        elif (self.status == 'fair'):
            self.status = 'good'
        elif (self.status == 'good'):
            self.status = 'serious'
        elif (self.status == 'serious'):
            self.status = 'undetermined'
        self.logs.create({"description": f"State changed to {self.status}", "patient_idd": self.id})

    @api.constrains("email")
    def _check_mail(self):
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        for record in self:
            print(re.search(regex, self.email))
            if (re.search(regex, self.email) == None):
                raise ValidationError(f"your mail doesn't match")

    _sql_constraints = [('Duplicate', 'unique(email)', 'Email already exists.')]

    @api.depends("birth_date")
    def _compute_age(self):
        today=datetime.today().strftime('%Y-%m-%d')
        for rec in self:
            print(rec.birth_date )
            print(today)
            if rec.birth_date:
                rec.age = relativedelta(
                fields.Date.from_string(today),
                fields.Date.from_string(rec.birth_date)).years
