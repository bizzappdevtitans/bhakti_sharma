from odoo import models, fields


class FacilityDetails(models.Model):
    _name = "facility.details"
    _description = "Facility Details"
    _rec_name = "facility_name"

    facility_name = fields.Char("Facility name")
    color = fields.Integer("Color")
