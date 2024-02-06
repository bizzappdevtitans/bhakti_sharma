from odoo import models, fields, api


class SubjectDetails(models.Model):
    _name = "subject.details"
    _description = "Information about subject"
    _rec_name = "subject_name"

    subject_name = fields.Char(string="Subject name")
    class_name_id = fields.Many2one(comodel_name="class.details", string="Class Name")
    description = fields.Html(string="Subject Description", help="Information about subjects ")
    teacher_name_id = fields.Many2one(comodel_name="teacher.details", string="Teacher Details")
    textBooks = fields.Html(string="Textbooks", help="Information Related textbooks")
    url = fields.Text(string="Url to refer", help="url to understand subjects chapter")
    sequence_number = fields.Char(string="Number", required=True, readonly=True, default="New")
    exam_name_ids = fields.One2many(comodel_name="exam.details", inverse_name="subject_name_id", string="Exam data")

    @api.model
    def create(self, vals):
        if vals.get("sequence_number", "New") == "New":
            vals["sequence_number"] = self.env["ir.sequence"].next_by_code(
                "subject.details"
            )
            vals["subject_name"] = vals["subject_name"].upper()
            return super(SubjectDetails, self).create(vals)

    def write(self, vals):
        if "subject_name" in vals and vals["subject_name"]:
            vals["subject_name"] = vals["subject_name"].upper()
        return super(SubjectDetails, self).write(vals)

    def name_get(self):
        result = []
        for record in self:
            result.append(
                (record.id, "[%s]-[%s]" % (record.sequence_number, record.subject_name))
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

    # def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
    #     domain = [("class_name_id", "=", "10TH-A")]
    #     return super(SubjectDetails, self).search_read(
    #         domain, fields, offset, limit, order
    #     )
