################################################################################
#
# This program is free software: you can redistribute it and/or modify it under 
# the terms of the GNU General Public License as published by the Free Software 
# Foundation, either version 3 of the License, or (at your option) any later 
# version.
# 
# This program is distributed in the hope that it will be useful, but WITHOUT 
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS 
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along with 
# this program. If not, see <https://www.gnu.org/licenses/>. 
#
# Copyright 2025 Nelson R. Salinas
#
################################################################################

import streamlit as st
import pandas as pd
import gspread
import datetime

gc = gspread.service_account_from_dict(st.secrets.credentials)

if 'errors' not in st.session_state:
	st.session_state.errors = ''

if 'data' not in st.session_state:
	st.session_state.data = None

if 'submitted' not in st.session_state:
	st.session_state.submitted = False


observers = [
	'Juliana Zuluaga',
	'Carlos Vargas',
	'Nelson Salinas'
	]

digitizers = ['Angela', 'Nelson']

interacts = [
	'Alelopatía negativa con',
	'Alelopatía positiva con',
	'Anida en',
	'Consume',
	'Crece sobre',
	'Dispersa a',
	'Es simbionte con',
	'Nidifica con',
	'Parasita a',
	'Poliniza a',
	'Interactúa con',
	'Se agrede con',
]

parts = [
	'esporangio',
	'esporófilo',
	'flor',
	'néctar',
	'polen',
	'fruto',
	'general',
	'hoja',
	'piel',
	'raíz',
	'savia',
	'sangre',
	'semilla',
	'parte no especificada',
	'sistema digestivo',
	'tallo',
	'hígado',
	'huevo',
	'pulmón',
]

id_observaciones = []

st.markdown("""

# Jardín Botánico de Bogotá

## Programa Conservación _in situ_

### Formato de digitalización de interacciones fotográficas.

#### Instrucciones

Insertar las observaciones en la forma abajo. Una vez termine de digitar los datos de una observación, presione el botón :red[**Validar**] para validar los datos. Si existen errores, un mensaje aparecerá indicando la naturaleza del error. Los datos no serán guardados si son erróneos, así que deben ser corregidos para que puedan ser guardados.

""")

# This doesn't work in Linux -> :blue-background[:red[**Enviar**]] 

def validate():

	if st.session_state.date is None:
		#st.info('Error: Falta fecha de observación.', icon="🔥")
		st.session_state.errors += 'Falta fecha de observación (obligatorio).\n\n'

	if st.session_state.photo:
		if len(st.session_state.photo.name) < 5:
			#st.info("El nombre de la fotografía es sospechosamente pequeño.")
			st.session_state.errors += "El nombre de la fotografía es sospechosamente pequeño.\n\n"
		
	else:
		st.session_state.errors += "No hay fotografía adjudicada a la observación.\n"


	st.session_state.submitted = False




def submit():
	
	sh = gc.open_by_key(st.secrets.table_link).worksheet(st.session_state.digitizer)
	now = datetime.datetime.now()
	row = [
		str(st.session_state.date),
		st.session_state.photo.name,
		st.session_state.observer,
		st.session_state.sp1,
		st.session_state.sp2,
		st.session_state.inter,
		st.session_state.part,
		st.session_state.lat,
		st.session_state.lon,
		now.strftime('%Y-%m-%d %H:%M:%S'),
		st.session_state.digitizer,
	]
	sh.append_row(row)
	st.session_state.submitted = True




with st.form(
	"Fotografías - Interacciones",
	clear_on_submit=True,
	):

	st.date_input(
		"Fecha",
		help="Fecha en la cual fue realizada la observación.",
		value=None,
		key="date",
	)

	st.file_uploader(
		"Seleccione una fotografía", 
		key="photo",
		help='Fotografía base de observación.'
	)
	
	st.selectbox(
		"Observador", 
		observers, 
		index=None, 
		key='observer',
		placeholder="Seleccione un investigador",
		help='Persona que tomó la fotografía'
	)

	st.selectbox(
		"Digitalizador", 
		digitizers, 
		index=None, 
		key='digitizer',
		placeholder="Seleccione un investigador",
		help='Persona que sistematiza la fotografía'
	)

	st.text_input(
		"Especie de planta", 
		key="sp1",
		placeholder='Digite el nombre de la planta',
		help="Nombre científico (sin autores) de la planta registrada en la fotografía"

	)

	st.text_input(
		"Especie de animal", 
		key="sp2",
		placeholder='Digite el nombre del animal',
		help="Nombre científico (sin autores) del animal registrado en la fotografía"
	)

	st.selectbox(
		"Tipo de interacción", 
		interacts, 
		index=None, 
		key='inter',
		placeholder="Seleccione una clase de interacción",
		help='Tipo de interacción entre las especies'
	)

	st.selectbox(
		"Órgano de interacción", 
		parts, 
		index=None, 
		key='part',
		placeholder="Seleccione una órgano",
		help='Órgano morfológico donde se realiza la interacción'
	)

	st.number_input(
		"Latitud", 
		key="lat",
		value=None,
		placeholder="Latitud",
		help='Latitud de la observación en formato decimal (e.g., 3.09284)',
		max_value=4.838990,
		min_value=3.725902
	)

	st.number_input(
		"Longitud", 
		key="lon",
		value=None,
		placeholder="Longitud",
		help='Longitud de la observación en formato decimal (e.g., -77.2360184)',
		min_value=-74.2248,
		max_value=-73.99194,
	)

	st.form_submit_button('Validar', on_click=validate)

pretty_data = st.empty()

if len(st.session_state.errors) > 0:
	st.info(st.session_state.errors)


else:

	# Present data before upload

	with pretty_data.container():

		if st.session_state.date:
			st.write(f"Fecha observación: '{str(st.session_state.date)}'")

		if st.session_state.photo:
			st.write(f"Nombre de la fotografía: '{str(st.session_state.photo.name)}'")

		if st.session_state.observer:
			st.write(f"Observador: '{st.session_state.observer}'")

		if st.session_state.digitizer:
			st.write(f"Digitador: '{st.session_state.digitizer}'")

		if st.session_state.sp1:
			st.write(f"Especie 1: '{st.session_state.sp1}'")

		if st.session_state.sp2:
			st.write(f"Especie 2: '{st.session_state.sp2}'")

		if st.session_state.inter:
			st.write(f"Interacción: '{st.session_state.inter}'")

		if st.session_state.part:
			st.write(f"Órgano: '{st.session_state.part}'")

		if st.session_state.lat:
			st.write(f"Latitud: '{st.session_state.lat}'")

		if st.session_state.lon:
			st.write(f"Longitud: '{st.session_state.lon}'")


	st.markdown("""Si los datos arriba son correctos, presione el botón :red[**Guardar**] para enviar los datos.""")

	st.button("Guardar", on_click=submit)

	if st.session_state.submitted:
		pretty_data.empty()




exit(0)