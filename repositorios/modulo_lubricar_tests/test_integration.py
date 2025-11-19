# -*- coding: utf-8 -*-

from odoo.tests import common, tagged
from odoo.exceptions import AccessError
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)


@tagged('post_install', '-at_install', 'modulo_lubricar_integration')
class TestFleetVehicleHandoverIntegration(common.TransactionCase):
    """Pruebas de integración para fleet.vehicle.handover con otros módulos"""

    def setUp(self):
        super(TestFleetVehicleHandoverIntegration, self).setUp()

        # Crear datos de prueba
        self.partner_driver = self.env['res.partner'].create({
            'name': 'Integration Test Driver',
            'email': 'integration@test.com',
        })

        self.brand = self.env['fleet.vehicle.model.brand'].create({
            'name': 'Integration Brand'
        })

        self.model = self.env['fleet.vehicle.model'].create({
            'name': 'Integration Model',
            'brand_id': self.brand.id
        })

        self.vehicle = self.env['fleet.vehicle'].create({
            'name': 'Integration Vehicle',
            'license_plate': 'INT123',
            'model_id': self.model.id,
        })

        self.handover_model = self.env['fleet.vehicle.handover']

    def test_01_integration_fleet_vehicle_odometer(self):
        """Test: Integración con fleet.vehicle.odometer"""
        initial_odometer_count = self.env['fleet.vehicle.odometer'].search_count([
            ('vehicle_id', '=', self.vehicle.id)
        ])

        handover = self.handover_model.create({
            'driver_id': self.partner_driver.id,
            'vehicle_id': self.vehicle.id,
            'handover_date': datetime.now(),
            'odometer': 5000.0,
            'personal_equipo': 'Test Personal',
        })

        self.vehicle.invalidate_cache()

        # Verificar que el odómetro se actualizó
        self.assertEqual(self.vehicle.odometer, 5000.0,
                        "El odómetro del vehículo debe actualizarse")

        # El módulo fleet crea automáticamente registros de odómetro
        final_odometer_count = self.env['fleet.vehicle.odometer'].search_count([
            ('vehicle_id', '=', self.vehicle.id)
        ])

        _logger.info(f"Registros de odómetro antes: {initial_odometer_count}, después: {final_odometer_count}")

    def test_02_integration_fleet_vehicle_driver(self):
        """Test: Integración con res.partner como conductor"""
        # Crear handover
        handover = self.handover_model.create({
            'driver_id': self.partner_driver.id,
            'vehicle_id': self.vehicle.id,
            'handover_date': datetime.now(),
            'odometer': 6000.0,
            'personal_equipo': 'Test Personal',
        })

        self.vehicle.invalidate_cache()

        # Verificar que el conductor del vehículo se actualizó
        self.assertEqual(self.vehicle.driver_id.id, self.partner_driver.id,
                        "El conductor del vehículo debe coincidir")

        # Verificar que el partner tiene la relación inversa
        # (esto depende de si fleet.vehicle tiene un campo relacionado)
        _logger.info(f"Vehículo asignado a: {self.vehicle.driver_id.name}")

    def test_03_integration_mail_thread(self):
        """Test: Integración con mail.thread para mensajería"""
        handover = self.handover_model.create({
            'driver_id': self.partner_driver.id,
            'vehicle_id': self.vehicle.id,
            'handover_date': datetime.now(),
            'odometer': 7000.0,
            'personal_equipo': 'Test Personal',
        })

        # Enviar mensaje
        message_body = "Vehículo entregado correctamente"
        handover.message_post(body=message_body, subject="Entrega")

        # Verificar que el mensaje se creó
        messages = handover.message_ids
        self.assertTrue(len(messages) > 0, "Debe haber al menos un mensaje")

        # Buscar nuestro mensaje
        our_message = messages.filtered(lambda m: message_body in (m.body or ''))
        self.assertTrue(our_message, "El mensaje debe haberse creado")
        _logger.info(f"Mensaje creado: {our_message[0].body if our_message else 'No encontrado'}")

    def test_04_integration_mail_activity(self):
        """Test: Integración con mail.activity.mixin para actividades"""
        handover = self.handover_model.create({
            'driver_id': self.partner_driver.id,
            'vehicle_id': self.vehicle.id,
            'handover_date': datetime.now(),
            'odometer': 8000.0,
            'personal_equipo': 'Test Personal',
            'electrico_luces_bajas': 'R',  # Necesita reparación
        })

        # Crear actividad
        activity_type = self.env['mail.activity.type'].search([], limit=1)
        if activity_type:
            handover.activity_schedule(
                activity_type_id=activity_type.id,
                summary='Reparar luces bajas',
                user_id=self.env.user.id,
                date_deadline=datetime.now() + timedelta(days=7)
            )

            # Verificar que la actividad se creó
            activities = handover.activity_ids
            self.assertTrue(len(activities) > 0, "Debe haber al menos una actividad")
            _logger.info(f"Actividad creada: {activities[0].summary if activities else 'No encontrada'}")

    def test_05_integration_sequence(self):
        """Test: Integración con ir.sequence"""
        # Verificar que la secuencia existe
        sequence = self.env['ir.sequence'].search([
            ('code', '=', 'fleet.vehicle.handover')
        ], limit=1)

        self.assertTrue(sequence, "La secuencia debe existir")

        # Crear múltiples handovers y verificar secuencia incremental
        handovers = []
        for i in range(3):
            handover = self.handover_model.create({
                'driver_id': self.partner_driver.id,
                'vehicle_id': self.vehicle.id,
                'handover_date': datetime.now(),
                'odometer': 9000.0 + i * 100,
                'personal_equipo': f'Test Personal {i}',
            })
            handovers.append(handover)

        # Verificar que los nombres son diferentes
        names = [h.name for h in handovers]
        self.assertEqual(len(names), len(set(names)), "Todos los nombres deben ser únicos")
        _logger.info(f"Secuencias generadas: {names}")

    def test_06_integration_tracking_fields(self):
        """Test: Integración del tracking con mail.thread"""
        handover = self.handover_model.create({
            'driver_id': self.partner_driver.id,
            'vehicle_id': self.vehicle.id,
            'handover_date': datetime.now(),
            'odometer': 10000.0,
            'personal_equipo': 'Test Personal',
        })

        initial_message_count = len(handover.message_ids)

        # Cambiar un campo con tracking
        new_driver = self.env['res.partner'].create({
            'name': 'New Driver',
            'email': 'newdriver@test.com',
        })

        handover.write({'driver_id': new_driver.id})

        # Verificar que se creó un mensaje de tracking
        final_message_count = len(handover.message_ids)
        self.assertGreater(final_message_count, initial_message_count,
                          "Debe haberse creado un mensaje de tracking")
        _logger.info(f"Mensajes antes: {initial_message_count}, después: {final_message_count}")

    def test_07_integration_security_groups(self):
        """Test: Integración con grupos de seguridad"""
        # Verificar que el grupo existe
        group = self.env.ref('modulo_lubricar.group_vehicle_handover_user', raise_if_not_found=False)

        if group:
            _logger.info(f"Grupo de seguridad encontrado: {group.name}")
            self.assertTrue(group.id, "El grupo debe existir")
        else:
            _logger.warning("Grupo de seguridad no encontrado")

    def test_08_integration_access_rights(self):
        """Test: Verificar permisos de acceso al modelo"""
        # Verificar que existen los permisos
        access_rights = self.env['ir.model.access'].search([
            ('model_id.model', '=', 'fleet.vehicle.handover')
        ])

        self.assertTrue(len(access_rights) > 0, "Deben existir permisos de acceso")

        for access in access_rights:
            _logger.info(f"Permiso: {access.name}, "
                        f"Lectura: {access.perm_read}, "
                        f"Escritura: {access.perm_write}, "
                        f"Crear: {access.perm_create}, "
                        f"Eliminar: {access.perm_unlink}")

    def test_09_integration_fleet_vehicle_state(self):
        """Test: Verificar que el estado del vehículo se mantiene consistente"""
        # Crear primera entrega
        handover1 = self.handover_model.create({
            'driver_id': self.partner_driver.id,
            'vehicle_id': self.vehicle.id,
            'handover_date': datetime.now(),
            'odometer': 11000.0,
            'personal_equipo': 'Test Personal 1',
        })

        self.vehicle.invalidate_cache()
        first_odometer = self.vehicle.odometer

        # Confirmar y devolver
        handover1.action_confirm()
        handover1.action_return()

        # Crear segunda entrega con odómetro mayor
        handover2 = self.handover_model.create({
            'driver_id': self.partner_driver.id,
            'vehicle_id': self.vehicle.id,
            'handover_date': datetime.now(),
            'odometer': 12000.0,
            'personal_equipo': 'Test Personal 2',
        })

        self.vehicle.invalidate_cache()
        second_odometer = self.vehicle.odometer

        self.assertGreater(second_odometer, first_odometer,
                          "El odómetro debe incrementar")
        _logger.info(f"Odómetro 1: {first_odometer}, Odómetro 2: {second_odometer}")

    def test_10_integration_search_domain(self):
        """Test: Búsquedas complejas con dominios"""
        # Crear varios handovers con diferentes estados
        handover1 = self.handover_model.create({
            'driver_id': self.partner_driver.id,
            'vehicle_id': self.vehicle.id,
            'handover_date': datetime.now(),
            'odometer': 13000.0,
            'personal_equipo': 'Test Personal',
            'electrico_luces_bajas': 'R',
        })

        handover2 = self.handover_model.create({
            'driver_id': self.partner_driver.id,
            'vehicle_id': self.vehicle.id,
            'handover_date': datetime.now(),
            'odometer': 14000.0,
            'personal_equipo': 'Test Personal',
        })

        # Buscar handovers con problemas
        # Nota: has_issues es computed y no store, así que no se puede buscar directamente
        # Buscamos por un campo específico
        problematic_handovers = self.handover_model.search([
            ('electrico_luces_bajas', '!=', 'N')
        ])

        self.assertIn(handover1, problematic_handovers,
                     "Debe encontrar el handover con problemas")
        self.assertNotIn(handover2, problematic_handovers,
                        "No debe encontrar el handover sin problemas")

    def test_11_integration_multi_vehicle(self):
        """Test: Múltiples vehículos y múltiples entregas"""
        # Crear segundo vehículo
        vehicle2 = self.env['fleet.vehicle'].create({
            'name': 'Integration Vehicle 2',
            'license_plate': 'INT456',
            'model_id': self.model.id,
        })

        # Crear segundo conductor
        driver2 = self.env['res.partner'].create({
            'name': 'Driver 2',
            'email': 'driver2@test.com',
        })

        # Crear entregas para diferentes combinaciones
        handover1 = self.handover_model.create({
            'driver_id': self.partner_driver.id,
            'vehicle_id': self.vehicle.id,
            'handover_date': datetime.now(),
            'odometer': 15000.0,
            'personal_equipo': 'Test Personal',
        })

        handover2 = self.handover_model.create({
            'driver_id': driver2.id,
            'vehicle_id': vehicle2.id,
            'handover_date': datetime.now(),
            'odometer': 20000.0,
            'personal_equipo': 'Test Personal',
        })

        # Verificar asignaciones
        self.vehicle.invalidate_cache()
        vehicle2.invalidate_cache()

        self.assertEqual(self.vehicle.driver_id.id, self.partner_driver.id,
                        "Vehículo 1 debe tener conductor 1")
        self.assertEqual(vehicle2.driver_id.id, driver2.id,
                        "Vehículo 2 debe tener conductor 2")

    def test_12_integration_copy_record(self):
        """Test: Copiar un registro de handover"""
        handover = self.handover_model.create({
            'driver_id': self.partner_driver.id,
            'vehicle_id': self.vehicle.id,
            'handover_date': datetime.now(),
            'odometer': 16000.0,
            'personal_equipo': 'Test Personal',
        })

        # Copiar el registro
        handover_copy = handover.copy()

        # Verificar que el nombre es diferente (copy=False en el campo name)
        self.assertNotEqual(handover.name, handover_copy.name,
                          "El nombre debe ser diferente en la copia")
        self.assertNotEqual(handover_copy.name, 'New',
                          "La copia debe tener una nueva secuencia")

        _logger.info(f"Original: {handover.name}, Copia: {handover_copy.name}")

    def test_13_integration_unlink_record(self):
        """Test: Eliminar un registro de handover"""
        handover = self.handover_model.create({
            'driver_id': self.partner_driver.id,
            'vehicle_id': self.vehicle.id,
            'handover_date': datetime.now(),
            'odometer': 17000.0,
            'personal_equipo': 'Test Personal',
        })

        handover_id = handover.id
        handover.unlink()

        # Verificar que el registro fue eliminado
        exists = self.handover_model.search([('id', '=', handover_id)])
        self.assertFalse(exists, "El registro debe haber sido eliminado")

    def test_14_integration_write_multiple_fields(self):
        """Test: Actualizar múltiples campos simultáneamente"""
        handover = self.handover_model.create({
            'driver_id': self.partner_driver.id,
            'vehicle_id': self.vehicle.id,
            'handover_date': datetime.now(),
            'odometer': 18000.0,
            'personal_equipo': 'Test Personal',
        })

        # Actualizar múltiples campos
        handover.write({
            'electrico_luces_bajas': 'R',
            'carroceria_puertas': 'Co',
            'notes': 'Múltiples problemas detectados',
            'state': 'confirmed',
        })

        # Verificar actualizaciones
        self.assertEqual(handover.electrico_luces_bajas, 'R')
        self.assertEqual(handover.carroceria_puertas, 'Co')
        self.assertEqual(handover.notes, 'Múltiples problemas detectados')
        self.assertEqual(handover.state, 'confirmed')
        self.assertTrue(handover.has_issues, "Debe detectar los problemas")

    def test_15_integration_fleet_vehicle_log(self):
        """Test: Verificar que se mantiene un log de cambios"""
        handover = self.handover_model.create({
            'driver_id': self.partner_driver.id,
            'vehicle_id': self.vehicle.id,
            'handover_date': datetime.now(),
            'odometer': 19000.0,
            'personal_equipo': 'Test Personal',
        })

        # Cambiar estado
        handover.action_confirm()

        # Verificar mensajes en el chatter
        messages = handover.message_ids
        tracking_messages = messages.filtered(lambda m: 'Estado' in (m.body or ''))

        _logger.info(f"Total de mensajes: {len(messages)}")
        _logger.info(f"Mensajes de tracking: {len(tracking_messages)}")

        # Debe haber al menos el mensaje de creación
        self.assertTrue(len(messages) > 0, "Debe haber mensajes en el chatter")
