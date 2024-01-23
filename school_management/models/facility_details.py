from odoo import models, fields


class FacilityDetails(models.Model):
    _name = "facility.details"
    _description = "Facility Details"
    _rec_name = "facility_name"

    facility_name = fields.Char("Facility name")
    color = fields.Integer("Color")

    classes = fields.Many2many("class.details")
    class_count = fields.Integer(compute="_compute_class_count")

    def _compute_class_count(self):
        for record in self:
            record.class_count = len(record.classes)

    def class_button(self):
        return {
            "name": "Class with same facility",
            "view_mode": "tree,form",
            "res_model": "class.details",
            "type": "ir.actions.act_window",
            "domain": [("facilities", "=", self.facility_name)],
        }
