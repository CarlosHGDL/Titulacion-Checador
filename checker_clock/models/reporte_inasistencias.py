from odoo import models, fields, tools, api

class reporte_inasistencias(models.TransientModel):
    _name = 'reporte.inasistencias'

    fecha_de = fields.Date(string = 'Inicio', required=True) 
    fecha_asta = fields.Date(string = 'Fin', required=True)
    teacher_ids = fields.Many2many(comodel_name='res.partner', string='Docente', domain="[('is_teacher', '=', True)]")
    
    def print_reporte(self):
        return self.env.ref('checker_clock.account_reporte_inasistencias').report_action(self)

    def buscar_docentes(self):
        if self.teacher_ids:
            return self.teacher_ids
        else:
            teacher_ids = self.env['res.partner'].search([('is_teacher', '=', True)])
            return teacher_ids

    def buscar_faltas(self, teacher_id):
        justification_catalog_id = self.env['justification.catalog'].search([('name', '=', 'Falta')],limit = 1)
        faltas_registros_count = self.env['schedule.class'].search_count([('date', '<=', self.fecha_asta),('date', '>=', self.fecha_de),('teacher_id', '=', teacher_id.id),('justification_catalog_id', '=', justification_catalog_id.id)])
        print(faltas_registros_count)
        return faltas_registros_count

    def buscar_retardos(self, teacher_id):
        justification_catalog_id = self.env['justification.catalog'].search([('name', '=', 'Retardó')],limit = 1)
        retardos_registros_count = self.env['schedule.class'].search_count([('date', '<=', self.fecha_asta),('date', '>=', self.fecha_de),('teacher_id', '=', teacher_id.id),('justification_catalog_id', '=', justification_catalog_id.id)])
        print(retardos_registros_count)
        return retardos_registros_count
    
    def faltas_x_retardos(self, teacher_id):
        retardos_count = self.buscar_retardos(teacher_id)
        if retardos_count == 0:
            print('yo turne')
            return 0
        total = retardos_count/3
        print(total,'total')
        total = int(total)
        print(total)
        return total
    
    def buscar_Justificado(self, teacher_id):
        justification_catalog_id = self.env['justification.catalog'].search([('name', '=', 'Justificado')],limit = 1)
        Justificado_registros_count = self.env['schedule.class'].search_count([('date', '<=', self.fecha_asta),('date', '>=', self.fecha_de),('teacher_id', '=', teacher_id.id),('justification_catalog_id', '=', justification_catalog_id.id)])
        print(Justificado_registros_count)
        return Justificado_registros_count

    def buscar_suplencia(self, teacher_id):
        justification_catalog_id = self.env['justification.catalog'].search([('name', '=', 'Suplencia')],limit = 1)
        suplencia_registros_count = self.env['schedule.class'].search_count([('date', '<=', self.fecha_asta),('date', '>=', self.fecha_de),('teacher_id', '=', teacher_id.id),('justification_catalog_id', '=', justification_catalog_id.id)])
        print(suplencia_registros_count)
        return suplencia_registros_count
    
    def buscar_otro(self, teacher_id):
        justification_catalog_ids = self.env['justification.catalog'].search([('name', 'not in', ('Justificado','Retardó','Falta','Asistencia'))])
        otro_registros_count = self.env['schedule.class'].search_count([('date', '<=', self.fecha_asta),('date', '>=', self.fecha_de),('teacher_id', '=', teacher_id.id),('justification_catalog_id', 'in', justification_catalog_ids.ids)])
        print(otro_registros_count)
        return otro_registros_count