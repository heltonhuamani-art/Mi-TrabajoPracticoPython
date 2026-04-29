import streamlit as st
import pandas as pd

st.set_page_config(page_title="PROYECTO 1 – APLICACIÓN EN STREAMLIT", page_icon="📊")


st.sidebar.title("Inicio")
aplicacion = st.sidebar.selectbox(
    "Selecciona una sección:",
    ("Home", "Ejercicio 1", "Ejercicio 2", "Ejercicio 3", "Ejercicio 4")
)

# ------ CONTENIDO DE LAS SECCIONES ------
if aplicacion == "Home":
    st.title("🏠 Mi Primer Proyecto en Python")
    st.image("logo.png", width=100)
    st.subheader("Helton Omar Huamani Ojeda")
    st.markdown("### :blue[**Curso : Especialización en Python for Analytics**]")
    st.write("2026")
    st.info("El presente proyecto es para demostrar lo aprendido en la primera etapa del curso.")
    
elif aplicacion == "Ejercicio 1":
    import streamlit as st
    import pandas as pd

    # 1. Generacion de la sesion para almacenar los movimientos.
    if 'movimientos' not in st.session_state:
        st.session_state.movimientos = []
        st.title("💰 Registro Financiero")

    # 2. Sidebar para la entrada de datos
    with st.sidebar:
        st.header("Nuevo Movimiento")
    
    # Formulario para mantener los inputs
    st.markdown("### :blue[Registro de Movimientos financieros : Ingreso o Gasto]")
    with st.form("formulario_registro", clear_on_submit=True):
        concepto = st.text_input("Concepto (Ej: Mensualidad, Salario, etc.)")
        monto = st.number_input("Monto ($)", min_value=0.0, step=0.01)
        tipo = st.selectbox("Tipo", ["Ingreso", "Gasto"])
        
        boton_guardar = st.form_submit_button("Registrar Movimiento")

    # 3. Lógica para añadir a la lista
    if boton_guardar:
        if concepto:
        # Guardamos como un diccionario para facilitar el manejo
            nuevo_registro = {
            "Concepto": concepto,
            "Monto": monto if tipo == "Ingreso" else -monto,
            "Tipo": tipo
            }
            st.session_state.movimientos.append(nuevo_registro)
            st.success(f"Registrado: {concepto}")
        else:
                st.error("Por favor, ingresa un concepto.")

    # 4. Mostrar el contenido de la lista
                st.subheader("Lista de Movimientos")
        if st.session_state.movimientos:
                # Convertimos la lista a un DataFrame para mostrar una tabla bonita
                df = pd.DataFrame(st.session_state.movimientos)
                st.table(df)
    
                # Cálculo de Flujo de Caja
                FlujoCaja = df["Monto"].sum()
                Ingresos =df[df["Tipo"] == "Ingreso"]["Monto"].sum()
                Gastos = df[df["Tipo"] == "Gasto"]["Monto"].sum()
                st.metric("TOTAL INGRESOS ", Ingresos, delta_color="normal")
                st.metric("TOTAL GASTOS ", Gastos, delta_color="normal")               
                st.markdown(f"### Flujo de Caja: :blue[${FlujoCaja:,.2f}]")
                
        else:
                st.info("Aún no hay movimientos registrados.")

elif aplicacion == "Ejercicio 2":
        import streamlit as st
        import numpy as np
        import pandas as pd

        # 1. Configuración del formulario
        st.set_page_config(page_title="Registro de Productos", layout="wide")
        st.title("📦 Registro de Productos Apicolas 🐝")


        # 2. Inicializar el Session State para persistir la informacion entre interacciones
        # Usaremos una lista para acumular registros y luego convertir a NumPy
        if 'data_list' not in st.session_state:
            st.session_state.data_list = []

        # 3. Formulario de entrada
        with st.form("form_productos", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                nombre = st.text_input("Nombre del producto")
                categoria = st.selectbox("Categoría", ["Colmenas", "Cera", "Epp Apicola", "Miel", "Pisos", "Tapas"  ])
            with col2:
                precio = st.number_input("Precio unitario", min_value=0.0, step=0.1)
                cantidad = st.number_input("Cantidad", min_value=0, step=1)
         
            
            submitted = st.form_submit_button("Registrar Producto")

        # 4. Lógica al enviar el formulario
        if submitted and nombre:
            total = precio * cantidad
            # Crear un registro (tipo estructurado para manejar texto y números)
            nuevo_registro_apicola = [nombre, categoria, precio, cantidad, total]
            st.session_state.data_list.append(nuevo_registro_apicola)
            st.success(f"Producto '{nombre}' registrado.")

        # 5. Visualización de datos usando NumPy
        if st.session_state.data_list:
            st.subheader("Inventario Actual")
            
            # Convertir la lista de registros a una matriz NumPy
            # Usamos object para permitir texto y números
            np_data = np.array(st.session_state.data_list, dtype=object)
            
            # Mostrar con pandas para mejor formato (opcional pero recomendado)
            df = pd.DataFrame(np_data, columns=["Nombre", "Categoría", "Precio", "Cantidad", "Total"])
            st.dataframe(df, use_container_width=True)

            # 6. Ejemplo de cálculo con NumPy (Total inventario)
            total_inventario = np.sum(np_data[:, 4].astype(float))
            st.metric("Valor Total del Inventario", f"${total_inventario:,.2f}")

            # Botón para borrar datos
            if st.button("Limpiar Registro"):
                st.session_state.data_list = []
                st.rerun()
        else:
            st.info("No hay productos registrados aún.")
elif aplicacion == "Ejercicio 3":
        import streamlit as st
        import pandas as pd
        import libreria_funciones_proyecto1 as lfp

        # Título de la App
        st.title("📊 Calculadora de Productividad Laboral")

        # Entradas de datos
        st.sidebar.header("Datos de Entrada")
        unidades_producidas = st.sidebar.number_input("Total Unidades ($)", min_value=0.0, value=100000.0)
        horas_trabajadas    = st.sidebar.number_input("Total Horas Trabajadas", min_value=0.0, value=2000.0)
        numero_trabajadores = st.sidebar.number_input("Número de Trabajadores", min_value=0, value=10)

        # Inicializar histórico en sesión si no existe
        if 'historico' not in st.session_state:
            st.session_state['historico'] = pd.DataFrame(columns=['Unidades', 'Horas', 'Trabajadores', 'Prod/Hora', 'Prod/Tra'])

        # Botón para ejecutar la función
        if st.sidebar.button("Calcular"):
            # Ejecución de la función desde archivo .py
            resultado = lfp.calcular_productividad_laboral(unidades_producidas, horas_trabajadas, numero_trabajadores)
            
            # Mostrar resultados
            st.subheader("Resultados")
            col1, col2 = st.columns(2)
            col1.metric("Prod. por Hora ($/h)", f"{resultado['productividad_por_hora']:,.2f}")
            col2.metric("Prod. por Trabajador", f"{resultado['productividad_por_trabajador']:,.2f}")

            # Guardar en el histórico (DataFrame)
            nuevo_registro = {
                'Unidades': unidades_producidas,
                'Horas': horas_trabajadas,
                'Trabajadores': numero_trabajadores,
                'Prod/Hora': resultado['productividad_por_hora'],
                'Prod/Tra': resultado['productividad_por_trabajador']
            }
            st.session_state['historico'] = pd.concat([st.session_state['historico'], pd.DataFrame([nuevo_registro])], ignore_index=True)

        # Mostrar histórico
        st.subheader("Histórico de Cálculos")
        st.dataframe(st.session_state['historico'], use_container_width=True)

elif aplicacion == "Ejercicio 4":
        import streamlit as st
        import pandas as pd
        import libreria_clases_proyecto1 as lcp

        # --- CONFIGURACIÓN DE STREAMLIT ---
        st.set_page_config(page_title="Calculador Agrícola Pro", layout="wide")
        st.title("🚜 Gestión de Parcelas y Fertilización")

        # Inicializar sesión
        if 'db_parcelas' not in st.session_state:
            st.session_state.db_parcelas = []
        if 'id_counter' not in st.session_state:
            st.session_state.id_counter = 1

        # --- INTERFAZ: CREAR (C) ---
        with st.expander("➕ Registrar Nueva Parcela", expanded=True):
            with st.form("form_parcela"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    nombre = st.text_input("Nombre de la Parcela", value=f"Parcela {st.session_state.id_counter}")
                    #nombre = st.text_input("Nombre de la Parcela", value="Parcela 1")
                    area = st.number_input("Área (Hectáreas)", min_value=0.1, value=1.0)
                with col2:
                    d_surcos = st.number_input("Distancia entre surcos (m)", min_value=0.1, value=0.7)
                    d_plantas = st.number_input("Distancia entre plantas (m)", min_value=0.1, value=0.3)
                with col3:
                    germ = st.slider("% Germinación", 1, 100, 90)
                    dosis = st.number_input("Dosis Nutriente (kg/ha)", min_value=1, value=150)
                
                col4, col5 = st.columns(2)
                pureza = col4.slider("% Pureza Fertilizante", 1, 100, 46)
                eficiencia = col5.slider("% Eficiencia Aplicación", 1, 100, 80)
                
                if st.form_submit_button("Calcular y Guardar"):
                    try:
                        nueva_p = lcp.ParcelaAgricola(st.session_state.id_counter, nombre, area, d_surcos, 
                                                d_plantas, germ, dosis, pureza, eficiencia)
                        st.session_state.db_parcelas.append(nueva_p)
                        st.session_state.id_counter += 1
                        st.success("¡Parcela registrada con éxito!")
                    except Exception as e:
                        st.error(f"Error: {e}")

        # --- INTERFAZ: LEER 
        st.subheader("📋 Resumen de Operaciones Agricolas")

        if st.session_state.db_parcelas:
            # Generar tabla de resultados desde los métodos de la clase
            tabla_resumen = [p.resumen() for p in st.session_state.db_parcelas]
            df = pd.DataFrame(tabla_resumen)
            st.dataframe(df, use_container_width=True,hide_index=True)
        else:
            st.info("No hay parcelas registradas. Usa el formulario superior.")

        # Eliminar (D)
        if st.session_state.db_parcelas:
            st.subheader("🗑️ Eliminar Registro")
            
            # 1. Generamos la lista de IDs disponibles
            ids_disponibles = [p.id for p in st.session_state.db_parcelas]
            
            # 2. Creamos el selector (AQUÍ SE DEFINE LA VARIABLE)
            id_para_borrar = st.selectbox("Seleccione el ID a eliminar", ids_disponibles)
            
            # 3. El botón debe estar justo debajo
            if st.button("Confirmar Eliminación", type="primary"):
                # Ahora sí, id_para_borrar existe y tiene un valor
                st.session_state.db_parcelas = [p for p in st.session_state.db_parcelas if p.id != id_para_borrar]
                st.success(f"Parcela con ID {id_para_borrar} eliminada correctamente.")
                st.rerun() 

        # Actualizar (U)
            if st.session_state.db_parcelas:
                with st.expander("🔄 Editar Datos de Parcela"):
                # 1. Selector de parcela a editar
                    ids_disponibles = [p.id for p in st.session_state.db_parcelas]
                    id_mod = st.selectbox("Seleccione el ID para modificar", ids_disponibles)

                # 2. Obtener el objeto actual para mostrar sus valores actuales en los campos
                parcela_actual = next(p for p in st.session_state.db_parcelas if p.id == id_mod)

                # 3. Formulario de edición
                with st.form("form_edicion"):
                    st.write(f"Editando: **{parcela_actual.nombre}**")
                    
                    col1, col2 = st.columns(2)
                    nuevo_nombre = col1.text_input("Nuevo Nombre", value=parcela_actual.nombre)
                    nueva_area = col2.number_input("Nueva Área (ha)", min_value=0.1, value=float(parcela_actual.area_hectareas))
                    
                    col3, col4 = st.columns(2)
                    nueva_dist_surcos = col3.number_input("Nueva Dist. Surcos (m)", min_value=0.1, value=float(parcela_actual.distancia_surcos_m))
                    nueva_dist_plantas = col4.number_input("Nueva Dist. Plantas (m)", min_value=0.1, value=float(parcela_actual.distancia_plantas_m))
                    
                    nueva_dosis = st.number_input("Nueva Dosis (kg/ha)", min_value=1, value=int(parcela_actual.dosis_nutriente_kg_ha))

                    # 4. Botón de confirmación dentro del formulario
                    if st.form_submit_button("Guardar Cambios"):
                        # Actualizamos los atributos del objeto directamente
                        parcela_actual.nombre = nuevo_nombre
                        parcela_actual.area_hectareas = nueva_area
                        parcela_actual.distancia_surcos_m = nueva_dist_surcos
                        parcela_actual.distancia_plantas_m = nueva_dist_plantas
                        parcela_actual.dosis_nutriente_kg_ha = nueva_dosis
                        
                        st.success(f"¡Datos de ID {id_mod} actualizados!")
                        st.rerun() # Refresca la tabla y el resumen

  

