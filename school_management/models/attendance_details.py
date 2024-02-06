from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError


class AttendanceDetails(models.Model):
    _name = "attendance.details"
    _description = "Information about daily attendance"
    _rec_name = "sheet_name"

    sheet_name = fields.Char(string="Sheet Name")
    attendance_date = fields.Date(string="Date", help="Enter today's attendance date")
    student_ids = fields.Many2many(comodel_name="student.details", string="Student")
    status = fields.Selection([("present", "Present"), ("absent", "Absent")])
    reason = fields.Text(string="Absent Reason")
    startTime = fields.Datetime(string="Start Time")
    endTime = fields.Datetime(string="End Time")
    notes = fields.Html(string="Notes")
    class_name_id = fields.Many2one(comodel_name="class.details", string="Class")
    state = fields.Selection(
        [("draft", "Draft"), ("in_progress", "In Progress"), ("done", "Done")],
        string="State",
        default="in_progress",
        required=True,
    )
    sequence_number = fields.Char(
        string="Number", required=True, readonly=True, default="New"
    )

    @api.constrains("startTime")
    def _validate_startTime(self):
        if self.startTime > self.endTime:
            raise ValidationError("Please check start time and end time")

    @api.onchange("class_name_id")
    def _validate_student(self):
        self.student_ids = self.class_name_id.student_ids.filtered(
            lambda name: name.student_class == self.class_name_id
        )

    @api.model
    def create(self, vals):
        if vals.get("sequence_number", "New") == "New":
            vals["sequence_number"] = self.env["ir.sequence"].next_by_code(
                "attendance.details"
            )
            vals["sheet_name"] = vals["sheet_name"].upper()
            return super(AttendanceDetails, self).create(vals)

    @api.onchange("status")
    def _validate_status(self):
        if not self.status == "present":
            self.write({"reason": ""})
        self.write({"reason": "None"})

    def write(self, vals):
        if "sheet_name" in vals and vals["sheet_name"]:
            vals["sheet_name"] = vals["sheet_name"].upper()
        return super(AttendanceDetails, self).write(vals)

    def name_get(self):
        result = []
        for record in self:
            result.append(
                (record.id, "%s - %s" % (record.sequence_number, record.sheet_name))
            )
        return result

    def _name_search(
        self, name="", args=None, operator="ilike", limit=100, name_get_uid=None
    ):
        args = list(args or [])
        if not (name == "" and operator == "ilike"):
            args += [
                "|",
                (self._rec_name, operator, name),
                ("class_name_id", operator, name),
            ]
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)

    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        domain = [
            "|",
            "|",
            ("state", "ilike", "in_progress"),
            ("state", "ilike", "done"),
            ("state", "ilike", "draft"),
        ]
        return super(AttendanceDetails, self).search_read(
            domain, fields, offset, limit, order
        )

    def unlink(self):
        if not self.class_name_id:
            return super(AttendanceDetails, self).unlink()
        raise UserError(
            "You can not delete the record which already have class details."
        )
