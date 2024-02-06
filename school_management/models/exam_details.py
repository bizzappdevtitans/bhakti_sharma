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
        string="Exam",
        help="Select exam type",
    )
    subject_name_id = fields.Many2one(comodel_name="subject.details", string="Subjects")
    class_name_ids = fields.Many2many(comodel_name="class.details", string="Class Name")
    student_name_ids = fields.Many2many(
        comodel_name="student.details",
        string="Student Details",
        domain="[('student_class_id','in',class_name_ids)]",
    )
    dateTime = fields.Datetime(string="Date and Time")
    total_marks = fields.Integer(string="Total marks")
    passing_marks = fields.Integer(string="Passing marks")
    exam_number = fields.Char(string="Exam Number", readonly=True, default="New")

    @api.model
    def create(self, records):
        records["exam_number"] = self.env["ir.sequence"].next_by_code("exam.details")
        return super(ExamDetails, self).create(records)

    def name_get(self):
        result = []
        for record in self:
            result.append(
                (
                    record.id,
                    "[%s] - [%s]"
                    % (record.exam_name, record.subject_name_id.subject_name),
                )
            )
        return result

    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        domain = [("exam_name", "ilike", "final term examination")]
        return super(ExamDetails, self).search_read(
            domain, fields, offset, limit, order
        )
