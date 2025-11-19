# -*- coding: utf-8 -*-

from odoo.tests import common, tagged
from odoo.exceptions import ValidationError
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)


@tagged('post_install', '-at_install', 'modulo_lubricar')
class TestFleetVehicleHandover(common.TransactionCase):
    """Pruebas unitarias para el modelo fleet.vehicle.handover"""

    def setUp(self):
        super(TestFleetVehicleHandover, self).setUp()

        # Crear datos de prueba
        self.partner_driver = self.env['res.partner'].create({
            'name': 'Test Driver',
            'email': 'driver@test.com',
        })

        self.vehicle = self.env['fleet.vehicle'].create({
            'name': 'Test Vehicle',
            'license_plate': 'ABC123',
            'model_id': self.env['fleet.vehicle.model'].create({
                'name': 'Test Model',
                'brand_id': self.env['fleet.vehicle.model.brand'].create({
                    'name': 'Test Brand'
                }).id
            }).id,
        })

        self.handover_model = self.env['fleet.vehicle.handover']

    def test_01_create_handover_basic(self):
        """Test: Crear un handover básico con datos mínimos"""
        handover = self.handover_model.create({
            'driver_id': self.partner_driver.id,
            'vehicle_id': self.vehicle.id,
            'handover_date': datetime.now(),
            'odometer': 1000.0,
            'personal_equipo': 'Test Personal',
        })

        self.assertTrue(handover.id, "El handover debe crearse correctamente")
        self.assertEqual(handover.driver_id.id, self.partner_driver.id, "Driver debe coincidir")
        self.assertEqual(handover.vehicle_id.id, self.vehicle.id, "Vehículo debe coincidir")
        self.assertEqual(handover.odometer, 1000.0, "Odómetro debe coincidir")
        self.assertEqual(handover.state, 'draft', "Estado inicial debe ser 'draft'")

    def test_02_sequence_generation(self):
        """Test: Verificar generación automática de secuencia"""
        handover = self.handover_model.create({
            'driver_id': self.partner_driver.id,
            'vehicle_id': self.vehicle.id,
            'handover_date': datetime.now(),
            'odometer': 1500.0,
            'personal_equipo': 'Test Personal',
        })

        self.assertNotEqual(handover.name, 'New', "La secuencia debe generarse automáticamente")
        self.assertTrue(len(handover.name) > 0, "El nombre debe tener contenido")
        _logger.info(f"Secuencia generada: {handover.name}")

    def test_03_default_values(self):
        """Test: Verificar valores por defecto de campos de checklist"""
        handover = self.handover_model.create({
            'driver_id': self.partner_driver.id,
            'vehicle_id': self.vehicle.id,
            'handover_date': datetime.now(),
            'odometer': 2000.0,
            'personal_equipo': 'Test Personal',
        })

        # Verificar que todos los campos de checklist tienen valor por defecto 'N'
        self.assertEqual(handover.electrico_luces_altas, 'N', "Luces altas debe ser 'N' por defecto")
        self.assertEqual(handover.electrico_luces_bajas, 'N', "Luces bajas debe ser 'N' por defecto")
        self.assertEqual(handover.carroceria_parabrisas, 'N', "Parabrisas debe ser 'N' por defecto")
        self.assertEqual(handover.interior_limpieza, 'N', "Limpieza debe ser 'N' por defecto")
        self.assertEqual(handover.elementos_seguridad_extintor, 'N', "Extintor debe ser 'N' por defecto")
        self.assertEqual(handover.ruedas_cubiertas, 'N', "Cubiertas debe ser 'N' por defecto")
        self.assertEqual(handover.accesorios_llave_ruedas, 'N', "Llave de ruedas debe ser 'N' por defecto")
        self.assertEqual(handover.documentacion_cedula_verde, 'N', "Cédula verde debe ser 'N' por defecto")

    def test_04_compute_has_issues_false(self):
        """Test: has_issues debe ser False cuando todos los campos están en 'N'"""
        handover = self.handover_model.create({
            'driver_id': self.partner_driver.id,
            'vehicle_id': self.vehicle.id,
            'handover_date': datetime.now(),
            'odometer': 2500.0,
            'personal_equipo': 'Test Personal',
        })

        self.assertFalse(handover.has_issues, "has_issues debe ser False cuando todo está en 'N'")

    def test_05_compute_has_issues_true(self):
        """Test: has_issues debe ser True cuando algún campo tiene problema"""
        handover = self.handover_model.create({
            'driver_id': self.partner_driver.id,
            'vehicle_id': self.vehicle.id,
            'handover_date': datetime.now(),
            'odometer': 3000.0,
            'personal_equipo': 'Test Personal',
            'electrico_luces_bajas': 'R',  # Reparar
        })

        self.assertTrue(handover.has_issues, "has_issues debe ser True cuando hay un problema")

    def test_06_compute_has_issues_multiple_problems(self):
        """Test: has_issues con múltiples problemas"""
        handover = self.handover_model.create({
            'driver_id': self.partner_driver.id,
            'vehicle_id': self.vehicle.id,
            'handover_date': datetime.now(),
            'odometer': 3500.0,
            'personal_equipo': 'Test Personal',
            'electrico_luces_bajas': 'R',  # Reparar
            'carroceria_puertas': 'Co',     # Corregir
            'elementos_seguridad_extintor': 'F',  # Faltante
        })

        self.assertTrue(handover.has_issues, "has_issues debe ser True con múltiples problemas")

    def test_07_all_estado_selection_values(self):
        """Test: Verificar que todos los valores de ESTADO_SELECTION funcionan"""
        estados = ['N', 'Co', 'F', 'V', 'R', 'L', 'Ca', 'Nc']

        for estado in estados:
            handover = self.handover_model.create({
                'driver_id': self.partner_driver.id,
                'vehicle_id': self.vehicle.id,
                'handover_date': datetime.now(),
                'odometer': 4000.0 + estados.index(estado) * 100,
                'personal_equipo': 'Test Personal',
                'electrico_luces_altas': estado,
            })

            self.assertEqual(handover.electrico_luces_altas, estado,
                           f"Estado '{estado}' debe guardarse correctamente")

            if estado != 'N':
                self.assertTrue(handover.has_issues,
                              f"has_issues debe ser True para estado '{estado}'")

    def test_08_action_confirm(self):
        """Test: Acción de confirmar entrega"""
        handover = self.handover_model.create({
            'driver_id': self.partner_driver.id,
            'vehicle_id': self.vehicle.id,
            'handover_date': datetime.now(),
            'odometer': 5000.0,
            'personal_equipo': 'Test Personal',
        })

        self.assertEqual(handover.state, 'draft', "Estado inicial debe ser 'draft'")

        handover.action_confirm()

        self.assertEqual(handover.state, 'confirmed', "Estado debe cambiar a 'confirmed'")

    def test_09_action_return(self):
        """Test: Acción de devolver vehículo"""
        handover = self.handover_model.create({
            'driver_id': self.partner_driver.id,
            'vehicle_id': self.vehicle.id,
            'handover_date': datetime.now(),
            'odometer': 5500.0,
            'personal_equipo': 'Test Personal',
        })

        handover.action_confirm()
        handover.action_return()

        self.assertEqual(handover.state, 'returned', "Estado debe cambiar a 'returned'")

    def test_10_state_workflow(self):
        """Test: Flujo completo de estados"""
        handover = self.handover_model.create({
            'driver_id': self.partner_driver.id,
            'vehicle_id': self.vehicle.id,
            'handover_date': datetime.now(),
            'odometer': 6000.0,
            'personal_equipo': 'Test Personal',
        })

        # Draft -> Confirmed
        self.assertEqual(handover.state, 'draft')
        handover.action_confirm()
        self.assertEqual(handover.state, 'confirmed')

        # Confirmed -> Returned
        handover.action_return()
        self.assertEqual(handover.state, 'returned')

    def test_11_vehicle_odometer_update(self):
        """Test: Actualización del odómetro del vehículo"""
        initial_odometer = self.vehicle.odometer
        new_odometer = 7000.0

        handover = self.handover_model.create({
            'driver_id': self.partner_driver.id,
            'vehicle_id': self.vehicle.id,
            'handover_date': datetime.now(),
            'odometer': new_odometer,
            'personal_equipo': 'Test Personal',
        })

        # Refrescar el vehículo para obtener valores actualizados
        self.vehicle.invalidate_cache()

        self.assertEqual(self.vehicle.odometer, new_odometer,
                        "El odómetro del vehículo debe actualizarse")

    def test_12_vehicle_driver_update(self):
        """Test: Actualización del conductor del vehículo"""
        initial_driver = self.vehicle.driver_id

        handover = self.handover_model.create({
            'driver_id': self.partner_driver.id,
            'vehicle_id': self.vehicle.id,
            'handover_date': datetime.now(),
            'odometer': 7500.0,
            'personal_equipo': 'Test Personal',
        })

        # Refrescar el vehículo
        self.vehicle.invalidate_cache()

        self.assertEqual(self.vehicle.driver_id.id, self.partner_driver.id,
                        "El conductor del vehículo debe actualizarse")

    def test_13_notes_field(self):
        """Test: Campo de notas adicionales"""
        notes_text = "Vehículo con rayón en puerta trasera izquierda"

        handover = self.handover_model.create({
            'driver_id': self.partner_driver.id,
            'vehicle_id': self.vehicle.id,
            'handover_date': datetime.now(),
            'odometer': 8000.0,
            'personal_equipo': 'Test Personal',
            'notes': notes_text,
        })

        self.assertEqual(handover.notes, notes_text, "Las notas deben guardarse correctamente")

    def test_14_tracking_enabled(self):
        """Test: Verificar que el tracking está habilitado"""
        handover = self.handover_model.create({
            'driver_id': self.partner_driver.id,
            'vehicle_id': self.vehicle.id,
            'handover_date': datetime.now(),
            'odometer': 8500.0,
            'personal_equipo': 'Test Personal',
        })

        # Verificar que el modelo hereda de mail.thread
        self.assertTrue(hasattr(handover, 'message_post'),
                       "El modelo debe heredar de mail.thread")
        self.assertTrue(hasattr(handover, 'activity_schedule'),
                       "El modelo debe heredar de mail.activity.mixin")

    def test_15_electrico_luces_giro_traseras_normalization(self):
        """Test: Normalización del campo electrico_luces_giro_traseras"""
        handover = self.handover_model.create({
            'driver_id': self.partner_driver.id,
            'vehicle_id': self.vehicle.id,
            'handover_date': datetime.now(),
            'odometer': 9000.0,
            'personal_equipo': 'Test Personal',
            # No se envía electrico_luces_giro_traseras
        })

        self.assertEqual(handover.electrico_luces_giro_traseras, 'N',
                        "electrico_luces_giro_traseras debe normalizarse a 'N'")

    def test_16_multiple_handovers_same_vehicle(self):
        """Test: Múltiples entregas del mismo vehículo"""
        driver2 = self.env['res.partner'].create({
            'name': 'Second Driver',
            'email': 'driver2@test.com',
        })

        handover1 = self.handover_model.create({
            'driver_id': self.partner_driver.id,
            'vehicle_id': self.vehicle.id,
            'handover_date': datetime.now(),
            'odometer': 10000.0,
            'personal_equipo': 'Test Personal 1',
        })

        handover1.action_confirm()
        handover1.action_return()

        handover2 = self.handover_model.create({
            'driver_id': driver2.id,
            'vehicle_id': self.vehicle.id,
            'handover_date': datetime.now(),
            'odometer': 11000.0,
            'personal_equipo': 'Test Personal 2',
        })

        self.assertEqual(handover1.state, 'returned', "Primera entrega debe estar 'returned'")
        self.assertEqual(handover2.state, 'draft', "Segunda entrega debe estar 'draft'")
        self.assertEqual(self.vehicle.driver_id.id, driver2.id,
                        "Vehículo debe tener el segundo conductor")

    def test_17_complete_checklist_all_sections(self):
        """Test: Checklist completo con todos los campos llenos"""
        handover = self.handover_model.create({
            'driver_id': self.partner_driver.id,
            'vehicle_id': self.vehicle.id,
            'handover_date': datetime.now(),
            'odometer': 12000.0,
            'personal_equipo': 'Test Personal',

            # Sistema eléctrico
            'electrico_luces_altas': 'N',
            'electrico_luces_bajas': 'N',
            'electrico_luces_giro_traseras': 'N',
            'electrico_luces_giro_delanteras': 'N',
            'electrico_luces_freno': 'N',
            'electrico_luces_marcha_atras': 'N',
            'electrico_luces_balizas_intermitentes': 'N',
            'electrico_alarma_retroceso': 'N',

            # Carrocería
            'carroceria_parabrisas': 'N',
            'carroceria_puertas': 'N',
            'carroceria_espejo_retrovisor': 'N',
            'carroceria_frenos': 'N',
            'carroceria_freno_estacionamiento': 'N',
            'carroceria_otros': 'N',

            # Interior
            'interior_limpieza': 'N',
            'interior_otros': 'N',

            # Elementos de seguridad
            'elementos_seguridad_extintor': 'N',
            'elementos_seguridad_balizas': 'N',
            'elementos_seguridad_linterna': 'N',
            'elementos_seguridad_pala': 'N',
            'elementos_seguridad_cadenas': 'N',
            'elementos_seguridad_chaleco': 'N',
            'elementos_seguridad_velas': 'N',

            # Ruedas
            'ruedas_cubiertas': 'N',
            'ruedas_ajuste': 'N',
            'rueda_auxilio': 'N',
            'rueda_checkpoint': 'N',
            'rueda_otros': 'N',

            # Accesorios
            'accesorios_llave_ruedas': 'N',
            'accesorios_crique': 'N',
            'accesorios_otros': 'N',

            # Documentación
            'documentacion_cedula_verde': 'N',
            'documentacion_vtv': 'N',
            'documentacion_seguro': 'N',
        })

        self.assertFalse(handover.has_issues, "No debe haber issues con todo en 'N'")
        _logger.info("Checklist completo creado exitosamente")

    def test_18_search_by_driver(self):
        """Test: Búsqueda por conductor"""
        handover = self.handover_model.create({
            'driver_id': self.partner_driver.id,
            'vehicle_id': self.vehicle.id,
            'handover_date': datetime.now(),
            'odometer': 13000.0,
            'personal_equipo': 'Test Personal',
        })

        found_handovers = self.handover_model.search([
            ('driver_id', '=', self.partner_driver.id)
        ])

        self.assertIn(handover, found_handovers, "Debe encontrar el handover por conductor")

    def test_19_search_by_vehicle(self):
        """Test: Búsqueda por vehículo"""
        handover = self.handover_model.create({
            'driver_id': self.partner_driver.id,
            'vehicle_id': self.vehicle.id,
            'handover_date': datetime.now(),
            'odometer': 14000.0,
            'personal_equipo': 'Test Personal',
        })

        found_handovers = self.handover_model.search([
            ('vehicle_id', '=', self.vehicle.id)
        ])

        self.assertIn(handover, found_handovers, "Debe encontrar el handover por vehículo")

    def test_20_search_by_state(self):
        """Test: Búsqueda por estado"""
        handover = self.handover_model.create({
            'driver_id': self.partner_driver.id,
            'vehicle_id': self.vehicle.id,
            'handover_date': datetime.now(),
            'odometer': 15000.0,
            'personal_equipo': 'Test Personal',
        })

        # Buscar drafts
        draft_handovers = self.handover_model.search([('state', '=', 'draft')])
        self.assertIn(handover, draft_handovers, "Debe encontrar el handover en estado draft")

        # Confirmar y buscar confirmed
        handover.action_confirm()
        confirmed_handovers = self.handover_model.search([('state', '=', 'confirmed')])
        self.assertIn(handover, confirmed_handovers, "Debe encontrar el handover en estado confirmed")
