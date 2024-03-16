from plasmidcanvas.plasmid import *
from plasmidcanvas.feature import *


if __name__ == "__main__":
    # Creates a plasmid that is 2500 base pairs long and is called "my_plasmid"
    # plasmid = Plasmid("pBR322", 4370)
    # new_plasmid_line_width = plasmid.get_plasmid_line_width() * 0.1
    # plasmid.set_plasmid_line_width(1)
    #
    # tetA = ArrowFeature("tetA", 86, 1276)
    # tetA.set_color("orange")
    # plasmid.add_feature(tetA)
    #
    # mKalama = ArrowFeature("mKalama", 3200, 4000, direction=-1)
    # mKalama.set_color("blue")
    # plasmid.add_feature(mKalama)
    #
    # pleu = ArrowFeature("P_leu500", 4000, 4030, direction=-1)
    # pleu.set_color("darkblue")
    # plasmid.add_feature(pleu)
    #
    # lac = RectangleFeature("lac", 4060, 4070)
    # lac.set_color("green")
    # plasmid.add_feature(lac)
    #
    # lac2 = RectangleFeature("lac", 3150, 3160)
    # lac2.set_color("green")
    # plasmid.add_feature(lac2)
    #
    # rop = ArrowFeature("rop", 1915, 2106)
    # rop.set_color("grey")
    # plasmid.add_feature(rop)
    #
    # ori = ArrowFeature("pMB1 ori", 2534, 3122, direction=-1)
    # ori.set_color("grey")
    # plasmid.add_feature(ori)

    # plasmid.save_to_file("partial_circuit.svg")

    full_circuit = Plasmid("TORC", 5273)

    tetA = ArrowFeature("tetA", 86, 1276)
    tetA.set_color("orange")
    full_circuit.add_feature(tetA)

    mRaspberry = ArrowFeature("mRaspberry", 4130, 4930)
    mRaspberry.set_color("red")
    full_circuit.add_feature(mRaspberry)

    pleu2 = ArrowFeature("P_leu500", 4100, 4129)
    pleu2.set_color("darkred")
    full_circuit.add_feature(pleu2)

    mKalama = ArrowFeature("mKalama", 3200, 4000, direction=-1)
    mKalama.set_color("blue")
    full_circuit.add_feature(mKalama)

    pleu = ArrowFeature("P_leu500", 4001, 4030, direction=-1)
    pleu.set_color("darkblue")
    full_circuit.add_feature(pleu)

    lac = RectangleFeature("lac", 4060, 4070)
    lac.set_color("green")
    full_circuit.add_feature(lac)

    lac2 = RectangleFeature("lac", 3150, 3160)
    lac2.set_color("green")
    full_circuit.add_feature(lac2)

    rop = ArrowFeature("rop", 1915, 2106)
    rop.set_color("grey")
    full_circuit.add_feature(rop)

    ori = ArrowFeature("pMB1 ori", 2534, 3122, direction=-1)
    ori.set_color("grey")
    full_circuit.add_feature(ori)

    full_circuit.save_to_file("full_circuit.svg")