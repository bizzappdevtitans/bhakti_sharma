from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    title_page_text = fields.Integer(
        string="Title",
        config_parameter="school.title_page_text",
    )
    allowed_students = fields.Integer(
        string="Allowed", config_parameter="allowed_students"
    )

    deleted_students = fields.Integer(
        string="Deleted ", config_parameter="school.deleted_students", default=0
    )

    available_rooms = fields.Integer(
        string="Room", config_parameter="class.available_rooms", default=0
    )
