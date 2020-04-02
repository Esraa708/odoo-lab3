from odoo import models, fields, api
from odoo.exceptions import UserError


class crsPartener(models.Model):
    _inherit = 'res.partner'
    # ccustomer_patient_ids = fields.One2many(comodel_name="hms", inverse_name="crm_patient_ids")
    crm_patient_ids = fields.Many2one(comodel_name="hms")
    vat=fields.Char(required=True)
    @api.model
    def create(self, vals_list):
        patient_email = self.env['hms'].search([('email', '=', vals_list['email'])])
        # patient_email=self.env.hms.search([('email','=',vals_list['email'])])
        print(patient_email)
        if len(patient_email) == 0:
            new_customer = super().create(vals_list)
            print(vals_list)
            return new_customer
        else:
            raise UserError(f"please enter another mail rather than your patient mail")
    @api.multi
    def unlink(self):
        if self.crm_patient_ids:
            raise UserError(f"customer is linked to a patient")
        else:
            super().unlink()



