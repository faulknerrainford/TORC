from TORC import Plasmid


def RT_LL_circuit(params):
    # TODO: 1. Read through and lac loop formation
    pass


def RT_CR_circuit(params):
    # TODO: 2. Read through and canonical repression
    pass


def RT_LL_CR_circuit(params):
    # TODO: 3. Read through, lac loop and canonical repression
    pass


def RT_circuit(params):
    # TODO: 4. Just read through
    CF_response, gradient, CF_strong, CF_weak, relax, tetA_sc_rate, CF_sc_rate, Lac, anti_tet = params
    circuit = Plasmid([("tetA", {"sc_rate": tetA_sc_rate}), ("P", "anti-tet", "anticlockwise",
                                                             {"weak": 1, "strong": 1, "terminator": False}),
                       ("bridge", "lacX"),
                       ("CF", "Yellow", "anticlockwise", {"strong": CF_strong, "weak": CF_weak, "sc_rate": CF_sc_rate,
                                                          "response": CF_response, "gradient": gradient,
                                                          "rate_dist": "sigmoid"}),
                       ("bridge", "lacX")], environments=[("lacX", 0), ("lac", 0)],
                      relax=relax, read_through=[("anti-tet", "Yellow", "lacX")])
    circuit.setup()
    return circuit


def SC_LL_circuit(params):
    # 5. Anti-tet supercoiling and lac loop formation
    CF_response, gradient, CF_strong, CF_weak, relax, tetA_sc_rate, CF_sc_rate, Lac, anti_tet = params
    circuit = Plasmid([("tetA", {"sc_rate": tetA_sc_rate}), ("P", "anti-tet", "anticlockwise", {"sc_rate": anti_tet}),
                       ("bridge", "lac"),
                       ("CF", "Yellow", "anticlockwise", {"strong": CF_strong, "weak": CF_weak, "sc_rate": CF_sc_rate,
                                                          "response": CF_response, "gradient": gradient,
                                                          "rate_dist": "sigmoid"}),
                       ("bridge", "lac")], environments=[("lacX", 0), ("lac", Lac)], relax=relax)
    circuit.setup()
    return circuit


def SC_CR_circuit(params):
    # 6. Anti-tet supercoiling and canonical repression
    CF_response, gradient, CF_strong, CF_weak, relax, tetA_sc_rate, CF_sc_rate, Lac, anti_tet = params
    circuit = Plasmid([("tetA", {"sc_rate": tetA_sc_rate}), ("P", "anti-tet", "anticlockwise", {"sc_rate": anti_tet}),
                       ("bridge", "lacX"),
                       ("CF", "Yellow", "anticlockwise", {"strong": CF_strong, "weak": CF_weak, "sc_rate": CF_sc_rate,
                                                          "response": CF_response, "gradient": gradient,
                                                          "rate_dist": "sigmoid", "repress": "lac"}),
                       ("bridge", "lacX")], environments=[("lacX", 0), ("lac", Lac)], relax=relax)
    circuit.setup()
    return circuit


def SC_LL_CR_circuit(params):
    # 7. Anti-tet supercoiling, lac loop and canonical repression
    CF_response, gradient, CF_strong, CF_weak, relax, tetA_sc_rate, CF_sc_rate, Lac, anti_tet = params
    circuit = Plasmid([("tetA", {"sc_rate": tetA_sc_rate}), ("P", "anti-tet", "anticlockwise", {"sc_rate": anti_tet}),
                       ("bridge", "lac"),
                       ("CF", "Yellow", "anticlockwise", {"strong": CF_strong, "weak": CF_weak, "sc_rate": CF_sc_rate,
                                                          "response": CF_response, "gradient": gradient,
                                                          "rate_dist": "sigmoid", "repress": "lac"}),
                       ("bridge", "lac")], environments=[("lacX", 0), ("lac", Lac)], relax=relax)
    circuit.setup()
    return circuit


def SC_circuit(params):
    # 8. Anti-tet supercoiling
    CF_response, gradient, CF_strong, CF_weak, relax, tetA_sc_rate, CF_sc_rate, Lac, anti_tet = params
    circuit = Plasmid([("tetA", {"sc_rate": tetA_sc_rate}), ("P", "anti-tet", "anticlockwise", {"sc_rate": anti_tet}),
                       ("bridge", "lacX"),
                       ("CF", "Yellow", "anticlockwise", {"strong": CF_strong, "weak": CF_weak, "sc_rate": CF_sc_rate,
                                                          "response": CF_response, "gradient": gradient,
                                                          "rate_dist": "sigmoid"}),
                       ("bridge", "lacX")], environments=[("lacX", 0), ("lac", 0)], relax=relax)
    circuit.setup()
    return circuit


def RT_SC_LL_circuit(params):
    # TODO: 9. Anti-tet supercoiling, read through and lac loop formation
    pass


def RT_SC_CR_circuit(params):
    # TODO: 10. Anti-tet supercoiling, read through and canonical repression
    pass


def RT_SC_LL_CR_circuit(params):
    # TODO: 11. Anti-tet supercoiling, read through, lac loop formation and canonical repression
    pass


def RT_SC_circuit(params):
    # TODO: 12. Anti-tet supercoiling and read through
    pass


def LL_circuit(params):
    # 13. Lac loop formation
    CF_response, gradient, CF_strong, CF_weak, relax, tetA_sc_rate, CF_sc_rate, Lac, anti_tet = params
    circuit = Plasmid([("tetA", {"sc_rate": tetA_sc_rate}),
                       ("bridge", "lac"),
                       ("CF", "Yellow", "anticlockwise", {"strong": CF_strong, "weak": CF_weak, "sc_rate": CF_sc_rate,
                                                          "response": CF_response, "gradient": gradient,
                                                          "rate_dist": "sigmoid"}),
                       ("bridge", "lac")], environments=[("lac", Lac)], relax=relax)
    circuit.setup()
    return circuit


def CR_circuit(params):
    # 14. Canonical repression
    CF_response, gradient, CF_strong, CF_weak, relax, tetA_sc_rate, CF_sc_rate, Lac, anti_tet = params
    circuit = Plasmid([("tetA", {"sc_rate": tetA_sc_rate}),
                       ("bridge", "lacX"),
                       ("CF", "Yellow", "anticlockwise", {"strong": CF_strong, "weak": CF_weak, "sc_rate": CF_sc_rate,
                                                          "response": CF_response, "gradient": gradient,
                                                          "rate_dist": "sigmoid", "repress": "lac"}),
                       ("bridge", "lacX")], environments=[("lac", Lac)], relax=relax)
    circuit.setup()
    return circuit


def LL_CR_circuit(params):
    # 15. Lac loop formation and canonical repression
    CF_response, gradient, CF_strong, CF_weak, relax, tetA_sc_rate, CF_sc_rate, Lac, anti_tet = params
    circuit = Plasmid([("tetA", {"sc_rate": tetA_sc_rate}),
                       ("bridge", "lac"),
                       ("CF", "Yellow", "anticlockwise", {"strong": CF_strong, "weak": CF_weak, "sc_rate": CF_sc_rate,
                                                          "response": CF_response, "gradient": gradient,
                                                          "rate_dist": "sigmoid", "repress": "lac"}),
                       ("bridge", "lac")], environments=[("lac", Lac)], relax=relax)
    circuit.setup()
    return circuit


def None_circuit(params):
    # 16. No effects
    CF_response, gradient, CF_strong, CF_weak, relax, tetA_sc_rate, CF_sc_rate, Lac, anti_tet = params
    circuit = Plasmid([("tetA", {"sc_rate": tetA_sc_rate}),
                       ("bridge", "lacX"),
                       ("CF", "Yellow", "anticlockwise", {"strong": CF_strong, "weak": CF_weak, "sc_rate": CF_sc_rate,
                                                          "response": CF_response, "gradient": gradient,
                                                          "rate_dist": "sigmoid"}),
                       ("bridge", "lacX")], environments=[("lacX", 0), ("lac", 0)], relax=relax)
    circuit.setup()
    return circuit
