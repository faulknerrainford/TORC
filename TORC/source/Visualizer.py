import matplotlib
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.lines as lines
from TORC import Supercoil, Environment, Visible, SupercoilSensitive, Promoter, GenetetA, Bridge
matplotlib.use('TkAgg')


Barriers = (str, GenetetA, Bridge)


class Visualizer:
    """
    Produces circular plasmid image of a circuit based on input components.

    Parameters
    ----------
    components  :   List<>
        List of components in the plasmid system.
    """

    def __init__(self, components):
        # TODO: settings for output and videos
        # TODO: initialise the drawing
        self.figure, self.axis = plt.subplots(1, 1)
        self.plasmid_components = ["ori"] + [x for x in components if not (isinstance(x, Supercoil) or
                                                                           isinstance(x, Environment) or
                                                                           isinstance(x, Visible))]
        self.supercoils = [x for x in components if isinstance(x, Supercoil)]
        self.environments = [x for x in components if isinstance(x, Environment) or isinstance(x, Visible)]
        self.component_count = len(self.plasmid_components)
        self.plasmid_positions = []
        pass

    def draw_plasmid(self, comp_size=0.2):
        """
        Draws and displays plasmid with the components representations with a given size.

        Parameters
        ----------
        comp_size   :   float
            Size on the axis of a side of the square components. All other components are sized relative to this.
        """
        centre = (-1, 0)
        radius = 0.6
        last_barrier = None
        current_supercoil = 0
        # adds the circle
        self.axis.set_xlim(-2, 1)
        self.axis.set_ylim(-1, 1)
        drawing_colored_circle = plt.Circle(centre, radius, edgecolor="orange", linestyle="--", fill=False)
        self.axis.set_aspect(1)
        self.axis.add_artist(drawing_colored_circle)
        # add components and labels
        # get plasmid coordinates
        self.get_plasmid_coordinates(centre, radius)
        # add bridge arc
        for shape in self.draw_bridge_arcs(centre, radius, comp_size, arc_level=0.5):
            if shape:
                self.axis.add_artist(shape)
        for ind in range(len(self.plasmid_components)):
            if isinstance(self.plasmid_components[ind], Barriers):
                if last_barrier is not None:
                    # add sc label
                    if not(current_supercoil == 0 and ind == 1):
                        sc_label, sc_box = self.get_supercoil_label(last_barrier, ind, centre,
                                                                    radius,
                                                                    current_supercoil, comp_size)
                        self.axis.add_artist(sc_box)
                        self.axis.add_artist(sc_label)
                        current_supercoil = current_supercoil + 1
                last_barrier = ind
                # add dividers
                self.axis.add_artist(self.get_barrier_line(ind, comp_size))
            for component in self.get_components(ind, comp_size):
                self.axis.add_artist(component)
        if current_supercoil < len(self.supercoils):
            sc_label, sc_box = self.get_supercoil_label(last_barrier, len(self.plasmid_components), centre, radius,
                                                        current_supercoil, comp_size)
            self.axis.add_artist(sc_box)
            self.axis.add_artist(sc_label)
        for env in self.draw_environments(comp_size):
            self.axis.add_artist(env)
        plt.title('Plasmid')
        plt.show()

    def draw_environments(self, comp_size):
        """
        Sets up locations for the environment and visible nodes and draws them returning the shape and text objects.

        Parameters
        ----------
        comp_size   :   float
            defines the size of the environment components as relative to the fixed size of on plasmid components (shows
             as squares)

        Returns
        -------
        List<>
            List of circles and text to be added to the figure providing the nodes and labels for the environment
            components.
        """
        envs_pos = []
        four_row_pos = (2.5*comp_size, comp_size, -comp_size, -2.5*comp_size)
        three_row_pos = (1.5*comp_size, 0, -1.5*comp_size)
        # calculate positions
        if len(self.environments) <= 4:
            # single column
            if len(self.environments) % 2:
                envs_pos.append((0.5, 0))
                if len(self.environments) > 1:
                    envs_pos.append((0.5, 1.5*comp_size))
                    envs_pos.append((0.5, -1.5*comp_size))
            else:
                envs_pos.append((0.5, comp_size))
                envs_pos.append((0.5, -comp_size))
                if len(self.environments) > 2:
                    envs_pos.append((0.5, 2.5*comp_size))
                    envs_pos.append((0.5, -2.5*comp_size))
        elif len(self.environments) % 4 == 0:
            # 4 rows
            row = 0
            col = 0.5
            for _ in self.environments:
                envs_pos.append((four_row_pos[row], col))
                row = (row + 1) % 4
                if row == 0:
                    col = col + comp_size/2
        elif len(self.environments) % 3 == 0:
            # 3 rows
            row = 0
            col = 0.5
            for _ in self.environments:
                envs_pos.append((three_row_pos[row], col))
                row = (row + 1) % 3
                if row == 0:
                    col = col + comp_size / 2
        elif len(self.environments) < 10:
            # 3 rows
            row = 0
            col = 0.5
            for _ in self.environments:
                envs_pos.append((three_row_pos[row], col))
                row = (row + 1) % 3
                if row == 0:
                    col = col + comp_size / 2
        elif len(self.environments) <= 16:
            # 4 rows
            row = 0
            col = 0.5
            for _ in self.environments:
                envs_pos.append((four_row_pos[row], col))
                row = (row + 1) % 4
                if row == 0:
                    col = col + comp_size / 2
        envs = []
        colour = "blue"
        for ind in range(len(self.environments)):
            if isinstance(self.environments[ind], Visible):
                colour = "orange"
            envs.append(plt.Circle(envs_pos[ind], comp_size*0.6, edgecolor=colour, facecolor="white"))
            envs.append(plt.Text(envs_pos[ind][0]-(comp_size/3), envs_pos[ind][1]-(comp_size/6),
                                 self.get_label(self.environments[ind])))
        return envs

    def shade_sc_regions(self):
        # TODO: add or update sc region shading
        pass

    def node_shading(self):
        # TODO: add or update the shading on component and environment nodes
        pass

    def get_plasmid_coordinates(self, center, radius):
        """
        Calculates the cartesian coordinates to position the plasmids components evenly around the plasmid drawn as a
        circle with center and radius given.

        Parameters
        ----------
        center  :   (x,y)
            Tuple giving cartesian coordinates of the center of the plasmid.
        radius  :   float
            The radius of the circle representing the plasmid.
        """
        # work out the position of coordinates based on size and position of circle.
        angle_incr = (2*math.pi)/self.component_count
        angle_ori = 0
        for i in range(self.component_count):
            angle_draw = (angle_ori-(math.pi/2)) % (2*math.pi)
            x = radius*np.sin(angle_draw) + center[0]
            y = radius*np.cos(angle_draw) + center[1]
            self.plasmid_positions.append((x, y))
            angle_ori = angle_ori + angle_incr

    def get_supercoil_label(self, inda, indb, center, radius, sc_ind, comp_size):
        """
        Creates the diamond and text label for the supercoiling region between two plasmid components.

        Parameters
        ----------
        inda        :   Integer
            The index of the anti-clockwise plasmid component
        indb        :   Integer
            The index of the clockwise plasmid component
        center      :   Tuple<float, float>
            The cartesian coordinates of the center of the plasmid.
        radius      :   float
            The radius of the plasmid
        sc_ind      :   Integer
            The index of the supercoiling region being labeled.
        comp_size   :   float
            The size of one side of the diamond.

        Returns
        -------
        plt.Text
            The text of the label
        plt.Rectangle
            The diamond for the label
        """
        angle_incr = (2*math.pi)/self.component_count
        theta_a = angle_incr * inda
        theta_mid = theta_a + (((math.pi*(indb-inda))/self.component_count) % (2*math.pi))
        mid_draw = (theta_mid-(math.pi/2)) % (2*math.pi)
        x = (radius/2) * np.sin(mid_draw) + center[0]
        y = (radius/2) * np.cos(mid_draw) + center[1]
        sc_label = plt.Text(x-(comp_size/3), y-(comp_size/4), self.get_label(self.supercoils[sc_ind]))
        sc_box = plt.Rectangle((x-(comp_size/2), y-(comp_size/2)), comp_size, comp_size,
                               angle=45, rotation_point='center', edgecolor='purple', facecolor='white')
        return sc_label, sc_box

    def get_components(self, ind, comp_size):
        """
        Generates boxes and labels for the component on the plasmid.

        Parameters
        ----------
        ind         :   int
             The index of the component to be drawn
        comp_size   :   float
            The width of the square to be drawn for the component.

        Returns
        -------
        List<plt.Rectangle, plt.Text>
            The box for the component and the label for the component
        """
        component_square = plt.Rectangle((self.plasmid_positions[ind][0] - (comp_size / 2),
                                          self.plasmid_positions[ind][1] - (comp_size / 2)),
                                         comp_size, comp_size, edgecolor="black", facecolor="white")
        component_label = plt.Text(self.plasmid_positions[ind][0] - (comp_size / 3), self.plasmid_positions[ind][1] -
                                   (comp_size / 4), self.get_label(self.plasmid_components[ind]))
        return [component_square, component_label]

    def get_label(self, component):
        """
        Generates a label based on the component including its type and internal values.

        Parameters
        ----------
        component   :   Object
            The component that needs to be labeled.

        Returns
        -------
        String
            The label for the component

        Raises
        ------
        LabelError
            Indicates a correct label could not be generated.
        """
        if isinstance(component, str) and component == "ori":
            return "ori"
        if isinstance(component, GenetetA):
            return "tetA"
        elif isinstance(component, SupercoilSensitive):
            label = "C"
            if component.fluorescent:
                label = label + "F"
            label = label + "_" + component.label
            return label
        elif isinstance(component, Promoter):
            label = "P"
            if component.fluorescent:
                label = label + "F"
            label = label + "_" + component.label
            return label
        elif isinstance(component, Environment):
            label = "E"
            if component.fluorescent:
                label = "F"
            label = label + "_" + component.label
            return label
        elif isinstance(component, Visible):
            return "V_" + component.colour
        elif isinstance(component, Supercoil):
            return "S_" + str(component.supercoiling_region)
        elif isinstance(component, Bridge):
            bridges = [x for x in self.plasmid_components if isinstance(x, Bridge) and x.label == component.label]
            if component == bridges[0]:
                return "BRA_" + component.label
            elif component == bridges[1]:
                return "BRC_" + component.label
            else:
                return "LabelError"
        else:
            return "LabelError"

    def draw_bridge_arcs(self, centre, radius, comp_size, arc_level=1.0):
        """
        Draw the arc between the barrier lines created by two bridge points.

        Parameters
        ----------
        centre      :   Tuple(float, float)
            The cartesian coordinates for the center of the plasmid.
        radius      :   float
            The radius of the plasmid.
        comp_size   :   float
            The size of the components is used to work out minor adjustments needed to place the arc between the two
            barriers.
        arc_level   :   the radius at which the arc is to be drawn

        Returns
        -------
        List<plt.Circle, plt.Circle, matplotlib.patches.Arc>
            The dot to draw on the first and second bridge barriers and the arc to draw between them.
        """
        # get indexes pairs of bridges
        bridge_dict_points = {}
        bridge_dict_ind = {}
        arc_adjust = 0.6*arc_level
        for ind in range(len(self.plasmid_components)):
            if isinstance(self.plasmid_components[ind], Bridge):
                if self.plasmid_components[ind].label in bridge_dict_points.keys():
                    bridge_dict_points[self.plasmid_components[ind].label] = \
                        (bridge_dict_points[self.plasmid_components[ind].label], self.plasmid_positions[ind])
                    bridge_dict_ind[self.plasmid_components[ind].label] = (bridge_dict_ind[
                                                                               self.plasmid_components[ind].label], ind)
                else:
                    bridge_dict_points[self.plasmid_components[ind].label] = self.plasmid_positions[ind]
                    bridge_dict_ind[self.plasmid_components[ind].label] = ind
        if bridge_dict_ind != {}:
            dots = []
            bridge_arc_pairs = []
            # draw dots on lines at arc radius for each pair
            for pair in bridge_dict_ind.keys():
                bridge_arc = []
                for point in bridge_dict_points[pair]:
                    # get midpoint of line and draw dot
                    point = self.adjust_point(point, comp_size)
                    mid_point = ((point[0]-centre[0])*arc_adjust + centre[0], (point[1]-centre[1])*arc_adjust
                                 + centre[1])
                    bridge_arc.append(mid_point)
                    dots.append(plt.Circle(mid_point, 0.03, color="black"))
                theta1 = bridge_dict_ind[pair][0]*(360/self.component_count)
                theta2 = bridge_dict_ind[pair][1] * (360 / self.component_count)
                print(theta1)
                print(theta2)
                # add arc
                bridge_arc = matplotlib.patches.Arc(centre, radius*arc_level, radius*arc_level, angle=-180,
                                                    theta1=360-theta2, theta2=360-theta1, edgecolor="black")
                bridge_arc_pairs.append(bridge_arc)
                return [dots[0], dots[1], bridge_arc]
        return []

    @staticmethod
    def adjust_point(point, comp_size):
        """
        Adjust the attachment point of the component based on the part of the plasmid it is in.

        Parameters
        ----------
        point      :   Tuple(float, float)
            Cartesian coordinates to be adjusted.
        comp_size   :  float
            The size of the component squares

        Returns
        -------
        Tuple(float, float)
            Adjusted cartesian coordinates
        """
        point = [point[0], point[1]]
        if point[0] < -1.1:
            point[0] = point[0] + (comp_size / 2)
        elif point[0] > -0.9:
            point[0] = point[0] - (comp_size / 2)
        if point[1] < -0.1:
            point[1] = point[1] + (comp_size / 2)
        elif point[1] > 0.1:
            point[1] = point[1] - (comp_size / 2)
        return point

    def get_barrier_line(self, ind, comp_size):
        """
        Draws a barrier line based on the index of the component and its size.

        Parameters
        ----------
        ind         :   Integer
            The index of the component the line needs to connect to.
        comp_size   :   float
            The size of the square component to be connected to.

        Returns
        -------
        lines.line2D
            The barrier line to be added to the figure.
        """
        end_point = [self.plasmid_positions[ind][0], self.plasmid_positions[ind][1]]
        end_point = self.adjust_point(end_point, comp_size)
        if isinstance(self.plasmid_components[ind], Bridge):
            barrier_line = lines.Line2D((-1, end_point[0]),
                                        (0, end_point[1]), ls="--", color="black")
        else:
            barrier_line = lines.Line2D((-1, end_point[0]),
                                        (0, end_point[1]), ls="-", color="black")
        return barrier_line
