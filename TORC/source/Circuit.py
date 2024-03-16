from TORC import Environment, Channel, Supercoil, GenetetA, SupercoilSensitive, Promoter, Bridge, Visible, LocalArea, \
    BridgeError, Origin
from queue import Queue
from threading import Thread


class Circuit:
    """
    Class for a plasmid circuit with its own local area of supercoiling and environments.

    Parameters
    ----------
    components      :   List<Tuple<String, String>>
        List of components to build onto the circuit, in type,name tuples.
    environments    :   List<Tuple<String, float>>
        List of initial environment conditions for non-empty starting environments in name, content tuples.
    label           :   String
        Name of the circuit
    local           :   LocalArea
        Local area can be provided to the system with a full start state if needed.
    """

    def __init__(self, components, environments=None, label="circuit1", local=None, relax=1):
        if environments is None:
            environments = []
        self.component_list = components
        self.environments = environments
        self.label = label
        self.circuit_components = []
        self.env_queues = {}
        if not local:
            self.local = LocalArea()
        else:
            self.local = local
        self.visible = None
        self.init_cw = None
        self.init_acw = None
        self.relax = relax

    # noinspection PyTypeChecker
    def setup(self):
        """
        Sets up the circuit by building the environments, components and supercoiling regions of the circuit.
        """
        # set up listed environments
        for env in self.environments:
            queue = Queue()
            self.env_queues[env[0]] = queue
            if env[0] in ["red", "blue", "green", "yellow", "magenta", "cyan"]:
                env = self.create_environment(env[0], queue, env[1], fluorescence=True)
            else:
                env = self.create_environment(env[0], queue, env[1], fluorescence=False)
            # TODO: set degradation rates from table
            self.circuit_components = self.circuit_components + [env]
        # set initial supercoiling region
        # TODO: add initial supercoiling if global supercoiling is set
        current_sc, cw, acw, sc_index = self.create_supercoil()
        self.init_cw = cw
        self.init_acw = acw
        self.circuit_components = self.circuit_components + [current_sc]
        # generate each component clockwise including any additional supercoiling regions and environments needed
        for comp in self.component_list:
            # TODO: user label lookup in table to assign different types eg. if comp[0].type = promoter rather than
            #  in list. Separate gene, promoter, location out to help with set up.
            if comp == "tetA" or comp[0] == "tetA":
                if len(comp) > 1 and comp[1] == "clockwise":
                    orientation = True
                else:
                    orientation = False
                current_sc = [x for x in self.circuit_components if isinstance(x, Supercoil)
                              and x.supercoiling_region == sc_index][0]
                if isinstance(comp[-1], dict):
                    components, temp_cw, temp_acw, temp_sc_index = self.create_gene("tetA", current_sc, orientation,
                                                                                    comp[-1])
                else:
                    components, temp_cw, temp_acw, temp_sc_index = self.create_gene("tetA", current_sc, orientation)
                if temp_cw is not None:
                    cw = temp_cw
                    acw = temp_acw
                if sc_index is not None:
                    sc_index = temp_sc_index
                self.circuit_components = self.circuit_components + components
            elif comp[0] in ["C", "CF", "P"]:
                if len(comp) > 2 and comp[2] == "anticlockwise":
                    orientation = True
                else:
                    orientation = False
                if isinstance(comp[-1], dict):
                    self.circuit_components = self.circuit_components \
                                              + self.create_promoter(comp[0], comp[1], sc_index,
                                                                     clockwise=orientation, parameters=comp[-1])
                else:
                    self.circuit_components = self.circuit_components \
                                              + self.create_promoter(comp[0], comp[1], sc_index, clockwise=orientation)
            elif comp[0] in ["bridge"]:
                current_sc = [x for x in self.circuit_components if isinstance(x, Supercoil)
                              and x.supercoiling_region == sc_index][0]
                components, cw, acw, sc_index = self.create_barrier(comp[0], comp[1], current_sc)
                self.circuit_components = self.circuit_components + components
        self.circuit_components = self.circuit_components + [self.create_visible()]
        # pair up bridges
        self.pair_bridges()
        # set up visible output
        self.visible = self.circuit_components[-1]

    def run(self, steps):
        """
        Runs through the component update functions for a given number of steps.

        Parameters
        ----------
        steps   :   Int
            Number of updates to run on each component.
        """
        for step in range(steps):
            threads = [Thread(target=x.update) for x in self.circuit_components]
            [x.start() for x in threads]
            [x.join() for x in threads]

    def create_gene(self, label, current_sc, clockwise=True, parameters=None):
        """
        Creates a promoter gene component and the associated new supercoil region.

        Parameters
        -----------
        label   :   String
            Suggests which specific gene promoter pair is to be generated, current options: tetA
        current_sc  :   Supercoil
            The current supercoiling region
        clockwise   :   Boolean
            The orientation of the gene being added
        parameters  :   Dictionary
            Set of additional setting for tetA such as supercoiling strength, "sc_rate"

        Returns
        --------
        List<GenetetA, Supercoil>
            The tetA gene and new supercoiling region
        Queue
            clockwise coiling for supercoiling region queue
        Queue
            anticlockwise coiling for supercoiling region queue
        Int
            The index for the new supercoiling region
        """
        if label == "tetA":
            sc, cw, acw, sc_ind = self.create_supercoil()
            if parameters and "sc_rate" in parameters.keys():
                gene = GenetetA(cw, sc, current_sc, local=self.local, clockwise=clockwise,
                                sc_strength=parameters["sc_rate"])
            else:
                gene = GenetetA(cw, sc, current_sc, local=self.local, clockwise=clockwise)
            return [gene, sc], cw, acw, sc_ind
        else:
            return None

    def create_promoter(self, promoter_type, output, sc_region, weak=0, strong=1, clockwise=True, parameters=None):
        """
        Creates promoters either with a basic, supercoiling sensitive or supercoiling sensitive with fluorescence and
        any associated environments needed.

        Parameters
        ----------
        promoter_type   :   String
            Type of promoter to be created choices from: P (basic promoter), C (supercoil sensitive promoter),
            CF (supercoil sensitive fluorescence promoter)
        output          :   String
            Name of gene/protein to be expressed
        sc_region       :   Int
            Index of supercoil region the promoter is in.
        weak            :   float
            output rate of weak signals
        strong          :   float
            output rate of strong signals
        clockwise       :   Boolean
            Indicates the orientation of the promoter gene pair on the plasmid
        parameters      :   dict
            Dictionary of additional parameters

        Returns
        --------
        List<>
            Component list either environment and promoter or just the promoter.
        """
        # TODO: Use look up table here
        if parameters:
            if "weak" in parameters.keys():
                weak = parameters["weak"]
            if "strong" in parameters.keys():
                strong = parameters["strong"]
            if "sc_rate" in parameters.keys():
                sc_rate = parameters["sc_rate"]
            else:
                sc_rate = 0
            if "response" in parameters.keys():
                response = parameters["response"]
            else:
                response = 0
            if "gradient" in parameters.keys():
                gradient = parameters["gradient"]
            else:
                gradient = 1
            if "rate_dist" in parameters.keys():
                rate_dist = parameters["rate_dist"]
            else:
                rate_dist = "threshold"
        else:
            sc_rate = 0
            response = 0
            gradient = 1
            rate_dist = "threshold"
        components = []
        if output not in self.local.get_keys():
            queue = Queue()
            env = self.create_environment(output, queue)
            self.env_queues[output] = queue
            components.append(env)
        if promoter_type == "P":
            promoter = Promoter(output, sc_region, self.local, weak=weak, strong=strong,
                                output_channel=self.env_queues[output], clockwise=clockwise, sc_rate=sc_rate,
                                threshold=response, gradient=gradient, rate_dist=rate_dist)
            components.append(promoter)
        elif promoter_type == "C":
            promoter = SupercoilSensitive(output, sc_region, self.local, weak=weak, strong=strong,
                                          output_channel=self.env_queues[output], clockwise=clockwise, sc_rate=sc_rate,
                                          threshold=response, gradient=gradient, rate_dist=rate_dist)
            components.append(promoter)
        elif promoter_type == "CF":
            promoter = SupercoilSensitive(output, sc_region, self.local, weak=weak, strong=strong,
                                          output_channel=self.env_queues[output], fluorescent=True, clockwise=clockwise,
                                          sc_rate=sc_rate, threshold=response, gradient=gradient, rate_dist=rate_dist)
            components.append(promoter)
        return components

    def create_barrier(self, barrier_type, sensor_input, current_sc):
        """
        Generates a barrier point, and new supercoiling regions and environments if needed, of type from list: bridge,
        origin

        Parameters
        ----------
        barrier_type    :   String
            type of barrier to be created.
        sensor_input    :   String
            protein to be detected in environment to turn barrier on or off
        current_sc      :   Supercoil
            current supercoiling region anti-clockwise of the barrier.

        Returns
        -------
        List<>
            Components: supercoil region, environment(if needed), barrier
        Queue
            Queue for cw supercoiling of the new supercoiling region
        Queue
            Queue for acw supercoiling of the new supercoiling region
        Int
            Index of new clockwise supercoiling region
        """
        components = []
        if barrier_type != "origin":
            sc, cw, acw, sc_ind = self.create_supercoil()
        else:
            # id the original supercoiling region to close loop
            sc = [x for x in self.circuit_components if isinstance(x, Supercoil) and x.supercoiling_region == 0][0]
            sc_ind = 0
            cw = self.local.get_supercoil_cw(sc_ind)
            acw = self.local.get_supercoil_acw(sc_ind)
        components.append(sc)
        if sensor_input and sensor_input not in self.local.get_keys():
            queue = Queue()
            env = self.create_environment(sensor_input, queue)
            self.env_queues[sensor_input] = queue
            components.append(env)
        if barrier_type == "bridge":
            bridge = Bridge(sensor_input, self.local, acw_sc_region=current_sc, cw_sc_region=sc)
            components.append(bridge)
        if barrier_type == "origin":
            origin = Origin("Origin", self.local, sc, current_sc)
            components.append(origin)
            components.remove(sc)
        return components, cw, acw, sc_ind

    def create_supercoil(self):
        """
        Generate a new supercoil region.

        Returns
        -------
        Supercoil
            The new supercoiling region component
        Queue
            clockwise coiling queue
        Queue
            anticlockwise coiling queue
        Int
            The index of the new supercoiling region
        """
        cw_queue = Queue()
        acw_queue = Queue()
        supercoil = Supercoil(cw_queue, acw_queue, self.local, relax=self.relax)
        return supercoil, cw_queue, acw_queue, supercoil.supercoiling_region

    def create_environment(self, label, queue_in, content=0.0, decay_rate=0, fluorescence=False):
        """
        Generates a new environment component for the circuit.

        Parameters
        ----------

        label           :   String
            Name of protein or colour being tracked
        queue_in        :   Queue
            Queue from which the environment will read new input
        content         :   float
            Amount of protein already in the environment
        decay_rate      :   float
            The amount of protein that is lost to decay in the environment at each timestep
        fluorescence    :   Boolean
            indicates if the output protein is fluorescent

        Returns
        -------
        Environment
            The new environment component
        """
        env = Environment(label, self.local, content=content, decay_rate=decay_rate, input_queue=queue_in,
                          fluorescent=fluorescence)
        return env

    def create_visible(self):
        """
        Creates a component and that interprets the fluorescent outputs and produces a combined colour.

        Returns
        -------
        Visible
            A component for combining all light output from the proteins in the system.
        """
        return Visible(self.local)

    def pair_bridges(self):
        """
        Connects pairs of bridge points with matching labels

        Raises
        ------
        BridgeError
            An error indicating the wrong number of bridge points of a single type have been found.
        """
        bridges = [x for x in self.circuit_components if isinstance(x, Bridge)]
        for bridge in bridges:
            poss_joins = [x for x in bridges if x.label == bridge.label and x != bridge]
            if len(poss_joins) == 1:
                bridge.set_bridge_check(poss_joins[0])
                poss_joins[0].set_bridge_check(bridge)
                bridges.remove(poss_joins[0])
                bridges.remove(bridge)
                if len(bridges) == 0:
                    break
            elif len(poss_joins) > 1:
                raise BridgeError("Too many bridge points of same type")
            else:
                raise BridgeError("No bridge point pair found")
