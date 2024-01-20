from odoo import models, fields, api

# from odoo.exceptions import ValidationError


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
