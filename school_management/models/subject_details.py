from odoo import models, fields, api


class SubjectDetails(models.Model):
    _name = "subject.details"
    _description = "Information about subject"
    _rec_name = "subject_name"

    subject_name = fields.Char(string="Subject name")
    class_name = fields.Many2one("class.details", "Class Name")
    description = fields.Html("Subject Description", help="Information about subjects ")
    teacher_name = fields.Many2one("teacher.details", "Teacher Details")
    textBooks = fields.Html("Textbooks", help="Information Related textbooks")
    url = fields.Text("Url to refer", help="url to understand subjects chapter")

    sequence_number = fields.Char("Number", required=True, readonly=True, default="New")

    # generate unique number for Subjects record
    @api.model
    def create(self, vals):
        if vals.get("sequence_number", "New") == "New":
            vals["sequence_number"] = self.env["ir.sequence"].next_by_code(
                "subject.details"
            )
            return super(SubjectDetails, self).create(vals)
