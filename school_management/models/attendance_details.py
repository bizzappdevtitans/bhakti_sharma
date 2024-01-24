from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AttendanceDetails(models.Model):
    _name = "attendance.details"
    _description = "Information about daily attendance"
    _rec_name = "sheet_name"

    sheet_name = fields.Char("Sheet Name")
    attendance_date = fields.Date("Date", help="Enter today's attendance date")
    student = fields.Many2many("student.details", string="Student")
    status = fields.Selection([("present", "Present"), ("absent", "Absent")])
    reason = fields.Text("Absent Reason")
    startTime = fields.Datetime("Start Time")
    endTime = fields.Datetime("End Time")
    notes = fields.Html("Notes")
    class_name = fields.Many2one("class.details", "Class")
    state = fields.Selection(
        [("draft", "Draft"), ("in_progress", "In Progress"), ("done", "Done")],
        string="State",
        default="in_progress",
        required=True,
    )

    @api.constrains("startTime")
    def _validate_startTime(self):
        for record in self:
            if record.startTime > record.endTime:
                raise ValidationError("Please check start time and end time")

    @api.onchange("class_name")
    def _compute_student(self):
        for record in self:
            record.student = record.class_name.students.filtered(
                lambda name: name.student_class == record.class_name
            )
            print(record.class_name.students.filtered(
                lambda name: name.student_class == record.class_name
            ))
