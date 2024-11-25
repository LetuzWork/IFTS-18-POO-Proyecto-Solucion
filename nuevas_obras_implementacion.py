from gestionar_obras import GestionarObra
from modelo_orm import *
from datetime import date, timedelta

def crear_casos_de_prueba():
    def llevar_obra_de_inicio_a_fin(
        area_responsable, barrio,empresa,fuente_financiamiento,
        tipo_contratacion,tipo_obra,nro_contratacion, nro_expediente,
        destacada, fecha_inicio, fecha_fin_inicial, mano_obra,
        porcentaje,salio_bien, nombre, monto_contrato
    ):
        obra = Obra.create(nombre = nombre, monto_contrato=monto_contrato)

        obra.nuevo_proyecto(tipo_obra, area_responsable, barrio)

        obra.iniciar_contratacion(tipo_contratacion, nro_contratacion)

        obra.adjudicar_obra(empresa, nro_expediente) 

        obra.iniciar_obra(destacada, fecha_inicio, fecha_fin_inicial, fuente_financiamiento, mano_obra)

        obra.actualizar_porcentaje_avance(porcentaje)

        accion_final = obra.finalizar_obra if salio_bien else obra.rescindir_obra
        
        accion_final()

    # GestionarObra.mapear_orm()

    obras = [
        {
            "area_responsable": AreaResponsable.get_or_create(nombre="Ministerio X")[0],
            "barrio": Barrio.get_or_create(nombre="parque patricios", comuna=4)[0],
            "empresa": Empresa.get_or_create(nombre="test SA", cuit="20123456780")[0],
            "fuente_financiamiento": FuenteFinanciamiento.get_or_create(nombre='x')[0],
            "tipo_contratacion": TipoContratacion.get_or_create(nombre='x')[0],
            "tipo_obra": TipoObra.get_or_create(nombre='x')[0],
            "nro_contratacion": "123-CTC-001",
            "nro_expediente": "123-XPD-001",
            "destacada": True,
            "fecha_inicio": date.today(),
            "fecha_fin_inicial": date.today() + timedelta(days=90),
            "mano_obra": 900000.50,
            "porcentaje": 20.00,
            "salio_bien": True,
            "nombre": "Plaza Guiraldes",
            "monto_contrato": 900000
        },
        {
            "area_responsable": AreaResponsable.get_or_create(nombre="Ministerio Y")[0],
            "barrio": Barrio.get_or_create(nombre="parque patricios", comuna=4)[0],
            "empresa": Empresa.get_or_create(nombre="test Seguros", cuit="20673456780")[0],
            "fuente_financiamiento": FuenteFinanciamiento.get_or_create(nombre='y')[0],
            "tipo_contratacion": TipoContratacion.get_or_create(nombre='y')[0],
            "tipo_obra": TipoObra.get_or_create(nombre='y')[0],
            "nro_contratacion": "123-CTC-002",
            "nro_expediente": "123-XPD-002",
            "destacada": False,
            "fecha_inicio": date.today(),
            "fecha_fin_inicial": date.today() + timedelta(days=90),
            "mano_obra": 10000.50,
            "porcentaje": 5.00,
            "salio_bien": False,
            "nombre": "Coima",
            "monto_contrato": 100000
        },
        {
            "area_responsable": AreaResponsable.get_or_create(nombre="Ministerio Z")[0],
            "barrio": Barrio.get_or_create(nombre="villa luro", comuna=10)[0],
            "empresa": Empresa.get_or_create(nombre="test IRL", cuit="20893456780")[0],
            "fuente_financiamiento": FuenteFinanciamiento.get_or_create(nombre='z')[0],
            "tipo_contratacion": TipoContratacion.get_or_create(nombre='z')[0],
            "tipo_obra": TipoObra.get_or_create(nombre='z')[0],
            "nro_contratacion": "123-CTC-003",
            "nro_expediente": "123-XPD-003",
            "destacada": False,
            "fecha_inicio": date.today(),
            "fecha_fin_inicial": date.today() + timedelta(days=90),
            "mano_obra": 1000.50,
            "porcentaje": 85.00,
            "salio_bien": True,
            "nombre": "Monumento a Mech",
            "monto_contrato": 5000.8
        }
    ]
    for o in obras:
        llevar_obra_de_inicio_a_fin(**o)


# crear_casos_de_prueba()

GestionarObra.obtener_indicadores()




