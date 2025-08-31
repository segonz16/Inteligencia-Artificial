import clips

env = clips.Environment()


moods = ["cansado", "estresado", "feliz", "relajado"]
preparations = ["espresso", "capuccino", "latte", "americano", "cold brew"]

def load_templates():
    try:
        existing_templates = [t.name for t in env.templates()]
        if "person" not in existing_templates:
            env.build("""
            (deftemplate person (slot name) (slot prefered_preparation) (slot mood))          
            """)
        if "coffee" not in existing_templates:
            env.build("""
            (deftemplate coffee (slot coffee_name) (slot preparation) (slot origin) (slot caffeine_level) (slot mood))
            """)
    except clips.CLIPSError as e:
        print(f"Error al cargar templates: {e}")
        return False
    return True


def load_rules():
    try:
        existing_rules = [r.name for r in env.rules()]

        if "espresso_cansado" not in existing_rules:
            env.build("""
                (defrule espresso_cansado
                    (person (name ?name) (prefered_preparation "espresso") (mood "cansado"))
                    =>
                    (printout t "Regla espresso_cansado activada para " ?name crlf)
                    (assert (coffee (coffee_name "Espresso doble") (preparation "espresso") (origin "Colombia") (caffeine_level "alto") (mood "cansado"))))
            """)

        if "latte_relajado" not in existing_rules:
            env.build("""
                (defrule latte_relajado
                    (person (name ?name) (prefered_preparation "latte") (mood "relajado"))
                    =>
                    (printout t "Regla latte_relajado activada para " ?name crlf)
                    (assert (coffee (coffee_name "Latte Vainilla") (preparation "latte") (origin "Brasil") (caffeine_level "medio") (mood "relajado"))))
            """)

        if "capuccino_feliz" not in existing_rules:
            env.build("""
                (defrule capuccino_feliz
                    (person (name ?name) (prefered_preparation "capuccino") (mood "feliz"))
                    =>
                    (printout t "Regla capuccino_feliz activada para " ?name crlf)
                    (assert (coffee (coffee_name "Capuccino Italiano") (preparation "capuccino") (origin "Italia") (caffeine_level "medio") (mood "feliz"))))
            """)

        if "americano_estresado" not in existing_rules:
            env.build("""
                (defrule americano_estresado
                    (person (name ?name) (prefered_preparation "americano") (mood "estresado"))
                    =>
                    (printout t "Regla americano_estresado activada para " ?name crlf)
                    (assert (coffee (coffee_name "Americano Suave") (preparation "americano") (origin "Etiopía") (caffeine_level "medio-bajo") (mood "estresado"))))
            """)

        if "cold_brew_cansado" not in existing_rules:
            env.build("""
                (defrule cold_brew_cansado
                    (person (name ?name) (prefered_preparation "cold brew") (mood "cansado"))
                    =>
                    (printout t "Regla cold_brew_cansado activada para " ?name crlf)
                    (assert (coffee (coffee_name "Cold Brew Energético") (preparation "cold brew") (origin "Costa Rica") (caffeine_level "alto") (mood "cansado"))))
            """)
    except clips.CLIPSError as e:
        print(f"Error al cargar reglas: {e}")
        return False
    return True


def evaluacion(name: str, prefered_preparation: str, mood: str):
    env.reset()   
    print("----- EVALUACIÓN -----")

    factArray = []

    usuario = f"""
        (person (name "{name}") (prefered_preparation "{prefered_preparation}") (mood "{mood}"))
    """
    try:
        env.assert_string(usuario)
    except clips.CLIPSError as e:
        print(f"Error al asertar el hecho: {e}")
        return "Error"

    env.run()

    for fact in env.facts():
        if fact.template.name != "initial-fact": 
            fact_conditions = {slot.name: fact[slot.name] for slot in fact.template.slots()}
            factArray.append({
                "fact_rule": fact.template.name,
                "fact_conditions": fact_conditions
            })

    return factArray

def preconditions():
    print("----- PLANTILLAS -----")
    if load_templates():
        print("Plantillas cargadas correctamente.")
    else:
        print("Error al cargar plantillas.")

    print("----- REGLAS -----")
    if load_rules():
        print("Reglas cargadas correctamente.")
    else:
        print("Error al cargar reglas.")

preconditions()
