from odoo import models, fields, api
from odoo.exceptions import UserError


class FacilityDetails(models.Model):
    _name = "facility.details"
    _description = "Facility Details"
    _rec_name = "facility_name"

    facility_name = fields.Char("Facility name")
    color = fields.Integer("Color")

    classes = fields.Many2many("class.details")
    class_count = fields.Integer(compute="_compute_class_count")

    sequence_number = fields.Char("Number", required=True, readonly=True, default="New")

    # generate unique number for facility record
    @api.model
    def create(self, vals):
        if vals.get("sequence_number", "New") == "New":
            vals["sequence_number"] = self.env["ir.sequence"].next_by_code(
                "facility.details"
            )
            vals["facility_name"] = vals["facility_name"].capitalize()
            return super(FacilityDetails, self).create(vals)

    def write(self, vals):
        if "facility_name" in vals and vals["facility_name"]:
            vals["facility_name"] = vals["facility_name"].upper()
            res = super(FacilityDetails, self).write(vals)
            return res

    def name_get(self):
        result = []
        for record in self:
            result.append(
                (record.id, "%s - %s" % (record.sequence_number, record.facility_name))
            )
        return result

    def _name_search(
        self, name="", args=None, operator="ilike", limit=100, name_get_uid=None
    ):
        args = list(args or [])
        if not (name == "" and operator == "ilike"):
            args += ["|", (self._rec_name, operator, name), ("classes", operator, name)]
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)

    def unlink(self):
        if self.classes:
            raise UserError(
                "You can not delete the record which already have class details."
            )
        else:
            return super(FacilityDetails, self).unlink()

    # Count the number of classes
    def _compute_class_count(self):
        for record in self:
            record.class_count = self.env["class.details"].search_count(
                [("facilities", "=", self.id)]
            )

    def class_button(self):
        for record in self:
            if record.class_count > 1:
                return {
                    "name": "Classes with same facility",
                    "view_mode": "tree,form",
                    "res_model": "class.details",
                    "type": "ir.actions.act_window",
                    "domain": [("facilities", "=", self.facility_name)],
                }
            else:
                return {
                    "name": "Classe with same facility",
                    "view_mode": "form",
                    "res_model": "class.details",
                    "type": "ir.actions.act_window",
                    "res_id": record.classes.id,
                }
