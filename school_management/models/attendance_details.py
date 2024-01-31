from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError


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
    sequence_number = fields.Char("Number", required=True, readonly=True, default="New")

    # generate unique number for attendance record
    @api.model
    def create(self, vals):
        if vals.get("sequence_number", "New") == "New":
            vals["sequence_number"] = self.env["ir.sequence"].next_by_code(
                "attendance.details"
            )
            return super(AttendanceDetails, self).create(vals)

    @api.constrains("startTime")
    def _validate_startTime(self):
        for record in self:
            if record.startTime > record.endTime:
                raise ValidationError("Please check start time and end time")

    # By selecing class name all the records of students of that particular class we get
    @api.onchange("class_name")
    def _compute_student(self):
        for record in self:
            record.student = record.class_name.students.filtered(
                lambda name: name.student_class == record.class_name
            )
            print(
                record.class_name.students.filtered(
                    lambda name: name.student_class == record.class_name
                )
            )

    @api.onchange("status")
    def _compute_status(self):
        for record in self:
            if record.status == "present":
                print(record.write({"reason": "None"}))
            else:
                record.write({"reason": ""})

    def unlink(self):
        if self.class_name:
            raise UserError(
                "You can not delete the record which already have class details."
            )
        else:
            self.clear_caches()
            return super(AttendanceDetails, self).unlink()
