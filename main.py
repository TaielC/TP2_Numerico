from datos_fijos import *
from euler import *
from runge_kutta import *
from graficadora import *


def transformar_a_celcius_minutos(resultados):
	resultados_transformados = []
	for i in range(len(resultados)):
		resultados_transformados.append((resultados[i][0]/60, resultados[i][1] - 273.15))
	return resultados_transformados


def calcular_resultados_reales(funcion, h, punto_inicio, punto_final):
	i = punto_inicio
	resultados = []
	while i <= punto_final:
		resultados.append((i, funcion(i)))
		i+=h
	return resultados


def calcular_error_relativo(resultados_reales, resultados):
	lista = []
	for i in range(len(resultados_reales)):
		lista.append((resultados_reales[i][0], abs(resultados_reales[i][1]-resultados[i][1])/resultados_reales[i][1]))
	return lista


def soaking(resultados):
	tf = resultados[-1][0]
	T_arranque = resultados[-1][1] -10
	ti = 0
	n = 0
	temp = 0
	for resultado in resultados:
		if resultado[1] >= T_arranque:
			if ti == 0:
				ti = resultado[0]
			n+=1
			temp+=resultado[1]
	return (tf-ti,temp/n)


def Punto_1():
	punto_inicio = 0 # s
	punto_final = longitud / velocidad # s
	resolucion_euler = euler(funcion_sin_radiacion, cadencia, punto_inicio, punto_final, T_0)
	resolucion_runge_kutta = runge_kutta(funcion_sin_radiacion, cadencia, punto_inicio, punto_final, T_0)
	resultados_reales = calcular_resultados_reales(solucion_sin_radiacion, cadencia, punto_inicio, punto_final)

	guardar_grafico_tiempo_vs_temperatura("Método Euler", resolucion_euler)
	guardar_grafico_tiempo_vs_temperatura("Método Runge-Kutta", resolucion_runge_kutta)
	guardar_grafico_tiempo_vs_temperatura("Comparación de Métodods con Solución Analítica", \
		resultados_reales, resolucion_euler, resolucion_runge_kutta)

	error_relativo_euler = calcular_error_relativo(resultados_reales, resolucion_euler)
	error_relativo_runge_kutta = calcular_error_relativo(resultados_reales, resolucion_runge_kutta)

	guardar_grafico_error_relativo("Error Relativo Euler", error_relativo_euler)
	guardar_grafico_error_relativo("Error Relativo Runge-Kutta", error_relativo_runge_kutta)


def Punto_2():
	punto_inicio = 0 # s
	punto_final = longitud / velocidad # s
	resolucion_runge_kutta = runge_kutta(funcion_completa, cadencia, punto_inicio, punto_final, T_0)

	guardar_grafico_tiempo_vs_temperatura("Resultados obtenidos", resolucion_runge_kutta)

	resultados_reales_punto_1 = calcular_resultados_reales(solucion_sin_radiacion, cadencia, punto_inicio, punto_final)
	guardar_grafico_tiempo_vs_temperatura("Comparación de Resultados con Solución Analítica Sin Radiación", \
		resultados_reales_punto_1, resolucion_runge_kutta)

	tiempo_soaking, T_soaking = soaking(resolucion_runge_kutta)
	print(f"Tiempo de Soaking: {tiempo_soaking/60}\n Temperatura Soaking: {T_soaking-273}")

