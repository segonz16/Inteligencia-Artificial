import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl
import matplotlib.pyplot as plt
import io

hora = ctrl.Antecedent(np.arange(0, 25, 1), 'hora')
estado = ctrl.Antecedent(np.arange(0, 11, 1), 'estado')  # 0: triste, 10: feliz
clima = ctrl.Antecedent(np.arange(0, 41, 1), 'clima')    # 0°C a 40°C
cafe_recomendado = ctrl.Consequent(np.arange(0, 11, 1), 'cafe')


hora['madrugada'] = fuzz.trapmf(hora.universe, [0, 2, 4, 6])
hora['manana'] = fuzz.trapmf(hora.universe, [5, 7, 11, 13])
hora['tarde'] = fuzz.trapmf(hora.universe, [12, 14, 16, 18])
hora['noche'] = fuzz.trapmf(hora.universe, [18, 19, 22, 24])

estado['triste'] = fuzz.trapmf(estado.universe, [0, 0, 3.5, 4])
estado['normal'] = fuzz.trapmf(estado.universe, [3, 3.5, 6.5, 7])
estado['feliz'] = fuzz.trapmf(estado.universe, [6, 6.5, 10, 10])

clima['frio'] = fuzz.trapmf(clima.universe, [0, 0, 10, 15])
clima['templado'] = fuzz.trimf(clima.universe, [10, 20, 25])
clima['caliente'] = fuzz.trapmf(clima.universe, [22, 30, 40, 40])

cafe_recomendado['suave'] = fuzz.trimf(cafe_recomendado.universe, [0, 2, 4])
cafe_recomendado['medio'] = fuzz.trimf(cafe_recomendado.universe, [3, 5, 7])
cafe_recomendado['fuerte'] = fuzz.trimf(cafe_recomendado.universe, [6, 8, 10])


rule1 = ctrl.Rule(hora['madrugada'] & estado['triste'] & clima['frio'], cafe_recomendado['medio'])
rule2 = ctrl.Rule(hora['madrugada'] & estado['triste'] & clima['templado'], cafe_recomendado['medio'])
rule3 = ctrl.Rule(hora['madrugada'] & estado['triste'] & clima['caliente'], cafe_recomendado['suave'])
rule4 = ctrl.Rule(hora['madrugada'] & estado['normal'] & clima['frio'], cafe_recomendado['medio'])
rule5 = ctrl.Rule(hora['madrugada'] & estado['normal'] & clima['templado'], cafe_recomendado['suave'])
rule6 = ctrl.Rule(hora['madrugada'] & estado['normal'] & clima['caliente'], cafe_recomendado['suave'])
rule7 = ctrl.Rule(hora['madrugada'] & estado['feliz'] & clima['frio'], cafe_recomendado['fuerte'])
rule8 = ctrl.Rule(hora['madrugada'] & estado['feliz'] & clima['templado'], cafe_recomendado['fuerte'])
rule9 = ctrl.Rule(hora['madrugada'] & estado['feliz'] & clima['caliente'], cafe_recomendado['medio'])
rule10 = ctrl.Rule(hora['manana'] & estado['triste'] & clima['frio'], cafe_recomendado['medio'])
rule11 = ctrl.Rule(hora['manana'] & estado['triste'] & clima['templado'], cafe_recomendado['medio'])
rule12 = ctrl.Rule(hora['manana'] & estado['triste'] & clima['caliente'], cafe_recomendado['suave'])
rule13 = ctrl.Rule(hora['manana'] & estado['normal'] & clima['frio'], cafe_recomendado['medio'])
rule14 = ctrl.Rule(hora['manana'] & estado['normal'] & clima['templado'], cafe_recomendado['medio'])
rule15 = ctrl.Rule(hora['manana'] & estado['normal'] & clima['caliente'], cafe_recomendado['suave'])
rule16 = ctrl.Rule(hora['manana'] & estado['feliz'] & clima['frio'], cafe_recomendado['fuerte'])
rule17 = ctrl.Rule(hora['manana'] & estado['feliz'] & clima['templado'], cafe_recomendado['fuerte'])
rule18 = ctrl.Rule(hora['manana'] & estado['feliz'] & clima['caliente'], cafe_recomendado['medio'])
rule19 = ctrl.Rule(hora['tarde'] & estado['triste'] & clima['frio'], cafe_recomendado['suave'])
rule20 = ctrl.Rule(hora['tarde'] & estado['triste'] & clima['templado'], cafe_recomendado['suave'])
rule21 = ctrl.Rule(hora['tarde'] & estado['triste'] & clima['caliente'], cafe_recomendado['suave'])
rule22 = ctrl.Rule(hora['tarde'] & estado['normal'] & clima['frio'], cafe_recomendado['medio'])
rule23 = ctrl.Rule(hora['tarde'] & estado['normal'] & clima['templado'], cafe_recomendado['medio'])
rule24 = ctrl.Rule(hora['tarde'] & estado['normal'] & clima['caliente'], cafe_recomendado['suave'])
rule25 = ctrl.Rule(hora['tarde'] & estado['feliz'] & clima['frio'], cafe_recomendado['medio'])
rule26 = ctrl.Rule(hora['tarde'] & estado['feliz'] & clima['templado'], cafe_recomendado['medio'])
rule27 = ctrl.Rule(hora['tarde'] & estado['feliz'] & clima['caliente'], cafe_recomendado['suave'])
rule28 = ctrl.Rule(hora['noche'] & estado['triste'], cafe_recomendado['suave'])
rule29 = ctrl.Rule(hora['noche'] & estado['normal'], cafe_recomendado['medio'])
rule30 = ctrl.Rule(hora['noche'] & estado['feliz'], cafe_recomendado['medio'])



cafe_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10,
    rule11, rule12, rule13, rule14, rule15, rule16, rule17, rule18, rule19, rule20,
    rule21, rule22, rule23, rule24, rule25, rule26, rule27, rule28, rule29, rule30,])
cafe_sim = ctrl.ControlSystemSimulation(cafe_ctrl)


def evaluar_cafe(hora_val, estado_val, clima_val):
    cafe_sim.reset()
    cafe_sim.input['hora'] = hora_val
    cafe_sim.input['estado'] = estado_val
    cafe_sim.input['clima'] = clima_val
    cafe_sim.compute()

    resultado = cafe_sim.output['cafe']
    print(f"Recomendación de café: {resultado:.2f}")

    cafe_recomendado.view(sim=cafe_sim)
    plt.title("Recomendación de café")
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return buf

def visualizacion_cafe():
    cafe_recomendado.view()
    plt.title("Tipos de café recomendados")
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()
    return buf
