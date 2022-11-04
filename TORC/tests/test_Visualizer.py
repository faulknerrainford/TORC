from unittest import TestCase
from TORC import Visualizer, GenetetA, Promoter, Supercoil, LocalArea, Bridge, Environment, Visible
from queue import Queue


class TestVisualizer(TestCase):
    def test_draw_plasmid(self):
        queue = Queue()
        local = LocalArea()
        viz = Visualizer([Promoter("Red", 0, None, output_channel=queue), Bridge("lac", local),
                          GenetetA(queue, 0, None), Bridge("lac", local), Supercoil(queue, local),
                          Supercoil(queue, local), Supercoil(queue, local), Supercoil(queue, local),
                          Environment("Red", local, input_queue=queue), Environment("lac", local, input_queue=queue),
                          Visible(local)])
        viz.draw_plasmid(comp_size=0.2)
        self.fail()

    def test_shade_sc_regions(self):
        self.fail()

    def test_node_shading(self):
        self.fail()

    def test_get_plasmid_coordinates(self):
        queue = Queue()
        viz = Visualizer([GenetetA(queue, 0, None)])
        viz.get_plasmid_coordinates((-1, 0), 0.6)
        self.assertAlmostEqual(-0.4, viz.plasmid_positions[0][0], places=2, msg="incorrect position")
        self.assertAlmostEqual(0, viz.plasmid_positions[0][1], places=2, msg="incorrect position")

    def test_get_label(self):
        queue = Queue()
        viz = Visualizer([GenetetA(queue, 0, None), Promoter("Red", 0, None, output_channel=queue)])
        self.assertEqual("tetA", viz.get_label(GenetetA(queue, 0, None)), "tetA incorrectly labeled")
        self.assertEqual("P_Red", viz.get_label(Promoter("Red", 0, None, output_channel=queue)),
                         "Promoter incorrectly labeled")

