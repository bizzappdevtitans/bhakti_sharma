from odoo import models, fields, api


class ExamDetails(models.Model):
    _name = "exam.details"
    _description = "Information about exams"
    _rec_name = "exam_name"

    exam_name = fields.Selection(
        [
            ("first term examination", "First Term Examination"),
            ("second term examination", "Second Term Examination"),
            ("final term examination", "Final Term Examination"),
        ],
        "Exam",
        help="Select exam type",
    )
    subject_name = fields.Many2one("subject.details", string="Subjects")
    class_name = fields.Many2many("class.details", string="Class Name")
    student_names = fields.Many2many(
        "student.details",
        string="Student Details",
        domain="[('student_class','in',class_name)]",
    )
    dateTime = fields.Datetime("Date and Time")
    total_marks = fields.Integer("Total marks")
    passing_marks = fields.Integer("Passing marks")
