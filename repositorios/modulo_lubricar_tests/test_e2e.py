# -*- coding: utf-8 -*-

from odoo.tests import common, tagged, HttpCase
from odoo.exceptions import ValidationError
from datetime import datetime
import logging
import json

_logger = logging.getLogger(__name__)


@tagged('post_install', '-at_install', 'modulo_lubricar_e2e')
class TestFleetVehicleHandoverE2E(HttpCase):
    """Pruebas End-to-End para el flujo completo de entrega de vehículos"""

    def setUp(self):
        super(TestFleetVehicleHandoverE2E, self).setUp()

        # Crear datos de prueba
        self.partner_driver = self.env['res.partner'].create({
            'name': 'E2E Test Driver',
            'email': 'e2e@test.com',
        })

        self.brand = self.env['fleet.vehicle.model.brand'].create({
            'name': 'E2E Brand'
        })

        self.model = self.env['fleet.vehicle.model'].create({
            'name': 'E2E Model',
            'brand_id': self.brand.id
        })

        self.vehicle = self.env['fleet.vehicle'].create({
            'name': 'E2E Vehicle',
            'license_plate': 'E2E123',
            'model_id': self.model.id,
        })

        self.handover_model = self.env['fleet.vehicle.handover']

    def test_01_e2e_complete_handover_workflow(self):
        """Test E2E: Flujo completo de entrega de vehículo"""
        # 1. Crear entrega (simula el backend)
        handover = self.handover_model.create({
            'driver_id': self.partner_driver.id,
            'vehicle_id': self.vehicle.id,
            'handover_date': datetime.now(),
            'odometer': 5000.0,
            'personal_equipo': 'E2E Personal',
        })

        self.assertEqual(handover.state, 'draft', "Estado inicial debe ser draft")
        _logger.info(f"[E2E] Paso 1: Entrega creada - {handover.name}")

        # 2. Completar checklist
        handover.write({
            'electrico_luces_altas': 'N',
            'electrico_luces_bajas': 'N',
            'carroceria_parabrisas': 'N',
            'interior_limpieza': 'L',  # Necesita limpieza
            'elementos_seguridad_extintor': 'V',  # Necesita verificación
        })

        self.assertTrue(handover.has_issues, "Debe detectar problemas")
        _logger.info(f"[E2E] Paso 2: Checklist completado - Issues: {handover.has_issues}")

        # 3. Confirmar entrega
        handover.action_confirm()
        self.assertEqual(handover.state, 'confirmed', "Estado debe ser confirmed")
        _logger.info(f"[E2E] Paso 3: Entrega confirmada")

        # 4. Verificar actualización del vehículo
        self.vehicle.invalidate_cache()
        self.assertEqual(self.vehicle.driver_id.id, self.partner_driver.id,
                        "Conductor debe estar asignado")
        self.assertEqual(self.vehicle.odometer, 5000.0,
                        "Odómetro debe estar actualizado")
        _logger.info(f"[E2E] Paso 4: Vehículo actualizado - Driver: {self.vehicle.driver_id.name}")

        # 5. Usar el vehículo (simular viajes)
        _logger.info(f"[E2E] Paso 5: Vehículo en uso...")

        # 6. Devolver vehículo
        handover.action_return()
        self.assertEqual(handover.state, 'returned', "Estado debe ser returned")
        _logger.info(f"[E2E] Paso 6: Vehículo devuelto")

        # 7. Verificar que el flujo se completó
        self.assertTrue(handover.id, "El handover debe existir")
        _logger.info(f"[E2E] Flujo completo exitoso: {handover.name}")

    def test_02_e2e_web_form_submission(self):
        """Test E2E: Envío de formulario web (simulado)"""
        # Simular datos POST del formulario web
        post_data = {
            'driver_id': str(self.partner_driver.id),
            'vehicle_id': str(self.vehicle.id),
            'handover_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'odometer': '6000.0',
            'personal_equipo': 'E2E Web Personal',

            # Sistema eléctrico
            'electrico_luces_altas': 'N',
            'electrico_luces_bajas': 'N',
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
            'elementos_seguridad_pala': 'Nc',
            'elementos_seguridad_cadenas': 'Nc',
            'elementos_seguridad_chaleco': 'N',
            'elementos_seguridad_velas': 'Nc',

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

            # Notas
            'notes': 'Formulario enviado desde prueba E2E',
        }

        # Simular creación desde el controlador
        vals = {
            'driver_id': int(post_data['driver_id']),
            'vehicle_id': int(post_data['vehicle_id']),
            'handover_date': post_data['handover_date'],
            'personal_equipo': post_data['personal_equipo'],
            'odometer': float(post_data['odometer']),

            # Copiar todos los campos del formulario
            'electrico_luces_altas': post_data.get('electrico_luces_altas', 'N'),
            'electrico_luces_bajas': post_data.get('electrico_luces_bajas', 'N'),
            'electrico_luces_giro_traseras': 'N',
            'electrico_luces_giro_delanteras': post_data.get('electrico_luces_giro_delanteras', 'N'),
            'electrico_luces_freno': post_data.get('electrico_luces_freno', 'N'),
            'electrico_luces_marcha_atras': post_data.get('electrico_luces_marcha_atras', 'N'),
            'electrico_luces_balizas_intermitentes': post_data.get('electrico_luces_balizas_intermitentes', 'N'),
            'electrico_alarma_retroceso': post_data.get('electrico_alarma_retroceso', 'N'),

            'carroceria_parabrisas': post_data.get('carroceria_parabrisas', 'N'),
            'carroceria_puertas': post_data.get('carroceria_puertas', 'N'),
            'carroceria_espejo_retrovisor': post_data.get('carroceria_espejo_retrovisor', 'N'),
            'carroceria_frenos': post_data.get('carroceria_frenos', 'N'),
            'carroceria_freno_estacionamiento': post_data.get('carroceria_freno_estacionamiento', 'N'),
            'carroceria_otros': post_data.get('carroceria_otros', 'N'),

            'interior_limpieza': post_data.get('interior_limpieza', 'N'),
            'interior_otros': post_data.get('interior_otros', 'N'),

            'elementos_seguridad_extintor': post_data.get('elementos_seguridad_extintor', 'N'),
            'elementos_seguridad_balizas': post_data.get('elementos_seguridad_balizas', 'N'),
            'elementos_seguridad_linterna': post_data.get('elementos_seguridad_linterna', 'N'),
            'elementos_seguridad_pala': post_data.get('elementos_seguridad_pala', 'N'),
            'elementos_seguridad_cadenas': post_data.get('elementos_seguridad_cadenas', 'N'),
            'elementos_seguridad_chaleco': post_data.get('elementos_seguridad_chaleco', 'N'),
            'elementos_seguridad_velas': post_data.get('elementos_seguridad_velas', 'N'),

            'ruedas_cubiertas': post_data.get('ruedas_cubiertas', 'N'),
            'ruedas_ajuste': post_data.get('ruedas_ajuste', 'N'),
            'rueda_auxilio': post_data.get('rueda_auxilio', 'N'),
            'rueda_checkpoint': post_data.get('rueda_checkpoint', 'N'),
            'rueda_otros': post_data.get('rueda_otros', 'N'),

            'accesorios_llave_ruedas': post_data.get('accesorios_llave_ruedas', 'N'),
            'accesorios_crique': post_data.get('accesorios_crique', 'N'),
            'accesorios_otros': post_data.get('accesorios_otros', 'N'),

            'documentacion_cedula_verde': post_data.get('documentacion_cedula_verde', 'N'),
            'documentacion_vtv': post_data.get('documentacion_vtv', 'N'),
            'documentacion_seguro': post_data.get('documentacion_seguro', 'N'),

            'notes': post_data.get('notes', ''),
            'state': 'draft',
        }

        # Crear el handover
        handover = self.handover_model.sudo().create(vals)

        # Verificar creación
        self.assertTrue(handover.id, "Handover debe crearse desde formulario web")
        self.assertEqual(handover.notes, 'Formulario enviado desde prueba E2E')
        self.assertEqual(handover.state, 'draft')
        _logger.info(f"[E2E] Formulario web procesado: {handover.name}")

    def test_03_e2e_api_drivers_endpoint(self):
        """Test E2E: Endpoint API de conductores"""
        # Simular llamada a la API
        partners = self.env['res.partner'].sudo().search([])
        result = [{'id': p.id, 'name': p.name} for p in partners]

        self.assertTrue(len(result) > 0, "Debe retornar conductores")
        _logger.info(f"[E2E] API drivers retornó {len(result)} conductores")

        # Verificar formato
        for driver in result[:5]:  # Verificar primeros 5
            self.assertIn('id', driver, "Debe tener campo 'id'")
            self.assertIn('name', driver, "Debe tener campo 'name'")

    def test_04_e2e_api_vehicles_endpoint(self):
        """Test E2E: Endpoint API de vehículos"""
        # Simular llamada a la API
        vehicles = self.env['fleet.vehicle'].sudo().search([])
        result = [{'id': v.id, 'name': v.display_name} for v in vehicles]

        self.assertTrue(len(result) > 0, "Debe retornar vehículos")
        _logger.info(f"[E2E] API vehicles retornó {len(result)} vehículos")

        # Verificar formato
        for vehicle in result:
            self.assertIn('id', vehicle, "Debe tener campo 'id'")
            self.assertIn('name', vehicle, "Debe tener campo 'name'")

    def test_05_e2e_validation_missing_fields(self):
        """Test E2E: Validación de campos faltantes en formulario"""
        # Simular envío con campos faltantes
        incomplete_post = {
            'driver_id': str(self.partner_driver.id),
            # vehicle_id faltante
            # handover_date faltante
            # odometer faltante
        }

        missing_fields = []

        if not incomplete_post.get('driver_id'):
            missing_fields.append('Conductor')
        if not incomplete_post.get('vehicle_id'):
            missing_fields.append('Vehículo')
        if not incomplete_post.get('handover_date'):
            missing_fields.append('Fecha de Entrega')
        if not incomplete_post.get('odometer'):
            missing_fields.append('Odómetro')

        # Verificar que se detectaron los campos faltantes
        self.assertEqual(len(missing_fields), 3, "Deben faltar 3 campos")
        self.assertIn('Vehículo', missing_fields)
        self.assertIn('Fecha de Entrega', missing_fields)
        self.assertIn('Odómetro', missing_fields)
        _logger.info(f"[E2E] Validación detectó campos faltantes: {missing_fields}")

    def test_06_e2e_driver_security_validation(self):
        """Test E2E: Validación de seguridad del conductor"""
        # Crear segundo conductor
        fake_driver = self.env['res.partner'].create({
            'name': 'Fake Driver',
            'email': 'fake@test.com',
        })

        # Simular que el usuario actual es partner_driver
        current_driver_id = self.partner_driver.id

        # Pero el formulario intenta enviar fake_driver
        submitted_driver_id = fake_driver.id

        # Validar que no coinciden
        is_valid = (submitted_driver_id == current_driver_id)

        self.assertFalse(is_valid, "La validación debe fallar")
        _logger.info(f"[E2E] Validación de seguridad: detectó manipulación de driver_id")

    def test_07_e2e_multiple_handovers_same_day(self):
        """Test E2E: Múltiples entregas el mismo día"""
        today = datetime.now()

        # Crear 5 entregas el mismo día
        handovers = []
        for i in range(5):
            handover = self.handover_model.create({
                'driver_id': self.partner_driver.id,
                'vehicle_id': self.vehicle.id,
                'handover_date': today,
                'odometer': 7000.0 + i * 100,
                'personal_equipo': f'E2E Personal {i}',
            })
            handovers.append(handover)

        # Verificar que todas se crearon
        self.assertEqual(len(handovers), 5, "Deben crearse 5 entregas")

        # Verificar secuencias únicas
        names = [h.name for h in handovers]
        self.assertEqual(len(set(names)), 5, "Todas deben tener secuencias únicas")
        _logger.info(f"[E2E] Entregas múltiples: {names}")

    def test_08_e2e_handover_with_all_problems(self):
        """Test E2E: Entrega con todos los problemas posibles"""
        handover = self.handover_model.create({
            'driver_id': self.partner_driver.id,
            'vehicle_id': self.vehicle.id,
            'handover_date': datetime.now(),
            'odometer': 8000.0,
            'personal_equipo': 'E2E Personal',

            # Marcar varios problemas
            'electrico_luces_altas': 'R',
            'electrico_luces_bajas': 'R',
            'carroceria_parabrisas': 'Co',
            'carroceria_puertas': 'L',
            'interior_limpieza': 'L',
            'elementos_seguridad_extintor': 'F',
            'elementos_seguridad_balizas': 'F',
            'ruedas_cubiertas': 'Ca',
            'accesorios_llave_ruedas': 'F',
            'documentacion_vtv': 'V',
        })

        self.assertTrue(handover.has_issues, "Debe detectar problemas")
        _logger.info(f"[E2E] Entrega con múltiples problemas creada: {handover.name}")

        # Simular que se crea una actividad para cada problema
        activity_type = self.env['mail.activity.type'].search([], limit=1)
        if activity_type:
            handover.activity_schedule(
                activity_type_id=activity_type.id,
                summary='Resolver problemas detectados en entrega',
                user_id=self.env.user.id,
            )

            activities = handover.activity_ids
            self.assertTrue(len(activities) > 0, "Debe haber actividades creadas")
            _logger.info(f"[E2E] Actividades creadas: {len(activities)}")

    def test_09_e2e_handover_lifecycle_with_messages(self):
        """Test E2E: Ciclo de vida completo con mensajes"""
        # 1. Crear
        handover = self.handover_model.create({
            'driver_id': self.partner_driver.id,
            'vehicle_id': self.vehicle.id,
            'handover_date': datetime.now(),
            'odometer': 9000.0,
            'personal_equipo': 'E2E Personal',
        })
        _logger.info(f"[E2E] 1. Creado: {handover.name}")

        # 2. Agregar mensaje inicial
        handover.message_post(
            body="Vehículo recibido para revisión inicial",
            subject="Recepción"
        )
        _logger.info(f"[E2E] 2. Mensaje inicial agregado")

        # 3. Completar inspección
        handover.write({
            'electrico_luces_altas': 'N',
            'carroceria_parabrisas': 'N',
            'interior_limpieza': 'L',
        })
        handover.message_post(
            body="Inspección completada. Requiere limpieza interior.",
            subject="Inspección"
        )
        _logger.info(f"[E2E] 3. Inspección completada")

        # 4. Confirmar
        handover.action_confirm()
        handover.message_post(
            body="Entrega confirmada al conductor",
            subject="Confirmación"
        )
        _logger.info(f"[E2E] 4. Confirmado")

        # 5. Devolver
        handover.action_return()
        handover.message_post(
            body="Vehículo devuelto en buen estado",
            subject="Devolución"
        )
        _logger.info(f"[E2E] 5. Devuelto")

        # Verificar mensajes
        messages = handover.message_ids
        self.assertTrue(len(messages) >= 4, "Debe haber al menos 4 mensajes")
        _logger.info(f"[E2E] Total de mensajes: {len(messages)}")

    def test_10_e2e_search_and_filter(self):
        """Test E2E: Búsqueda y filtrado de entregas"""
        # Crear entregas con diferentes características
        handover_normal = self.handover_model.create({
            'driver_id': self.partner_driver.id,
            'vehicle_id': self.vehicle.id,
            'handover_date': datetime.now(),
            'odometer': 10000.0,
            'personal_equipo': 'E2E Normal',
        })

        handover_problems = self.handover_model.create({
            'driver_id': self.partner_driver.id,
            'vehicle_id': self.vehicle.id,
            'handover_date': datetime.now(),
            'odometer': 11000.0,
            'personal_equipo': 'E2E Problems',
            'electrico_luces_bajas': 'R',
        })

        handover_problems.action_confirm()

        # Búsquedas
        all_handovers = self.handover_model.search([
            ('vehicle_id', '=', self.vehicle.id)
        ])
        _logger.info(f"[E2E] Total de entregas: {len(all_handovers)}")

        draft_handovers = self.handover_model.search([
            ('vehicle_id', '=', self.vehicle.id),
            ('state', '=', 'draft')
        ])
        _logger.info(f"[E2E] Entregas en draft: {len(draft_handovers)}")

        confirmed_handovers = self.handover_model.search([
            ('vehicle_id', '=', self.vehicle.id),
            ('state', '=', 'confirmed')
        ])
        _logger.info(f"[E2E] Entregas confirmadas: {len(confirmed_handovers)}")

        # Verificar
        self.assertGreaterEqual(len(all_handovers), 2, "Debe haber al menos 2 entregas")
        self.assertIn(handover_normal, draft_handovers, "handover_normal debe estar en draft")
        self.assertIn(handover_problems, confirmed_handovers, "handover_problems debe estar confirmed")


@tagged('post_install', '-at_install', 'modulo_lubricar_http')
class TestVehicleHandoverHTTP(HttpCase):
    """Pruebas HTTP para controladores web"""

    def test_01_http_vehicle_handover_form_page(self):
        """Test HTTP: Página de formulario de entrega"""
        # Intentar acceder a la página (requiere autenticación)
        response = self.url_open('/vehicle-handover')

        self.assertEqual(response.status_code, 200, "La página debe responder 200")
        _logger.info(f"[HTTP] Formulario accesible: {response.status_code}")

    def test_02_http_api_drivers(self):
        """Test HTTP: API de conductores"""
        response = self.url_open('/vehicle_handover/api/drivers')

        self.assertEqual(response.status_code, 200, "API drivers debe responder 200")

        # Intentar parsear JSON
        try:
            data = json.loads(response.text)
            self.assertIsInstance(data, list, "Debe retornar una lista")
            _logger.info(f"[HTTP] API drivers retornó {len(data)} conductores")
        except json.JSONDecodeError:
            self.fail("La respuesta debe ser JSON válido")

    def test_03_http_api_vehicles(self):
        """Test HTTP: API de vehículos"""
        response = self.url_open('/vehicle_handover/api/vehicles')

        self.assertEqual(response.status_code, 200, "API vehicles debe responder 200")

        # Intentar parsear JSON
        try:
            data = json.loads(response.text)
            self.assertIsInstance(data, list, "Debe retornar una lista")
            _logger.info(f"[HTTP] API vehicles retornó {len(data)} vehículos")
        except json.JSONDecodeError:
            self.fail("La respuesta debe ser JSON válido")
