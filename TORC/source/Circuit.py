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

    def __init__(self, components, environments=None, label="circuit1", local=None):
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
        self.init_coil = None

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
            self.circuit_components = self.circuit_components + [env]
        # set initial supercoiling region
        current_sc, coil, sc_index = self.create_supercoil()
        self.init_coil = coil
        self.circuit_components = self.circuit_components + [current_sc]
        # generate each component clockwise including any additional supercoiling regions and environments needed
        for comp in self.component_list:
            if comp == "tetA":
                components, coil, sc_index = self.create_gene("tetA")
                self.circuit_components = self.circuit_components + components
            elif comp[0] in ["C", "CF", "P"]:
                self.circuit_components = self.circuit_components + self.create_promoter(comp[0], comp[1], sc_index)
            elif comp[0] in ["bridge"]:
                components, coil, sc_index = self.create_barrier(comp[0], comp[1], sc_index)
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

    def create_gene(self, label):
        """
        Creates a promoter gene component and the associated new supercoil region.

        Parameters
        -----------
        label   :   String
            Suggests which specific gene promoter pair is to be generated, current options: tetA

        Returns
        --------
        self.fail()
        List<GenetetA, Supercoil>
            The tetA gene and new supercoiling region
        ChannelEnd
            The in channel for the new supercoiling region
        Int
            The index for the new supercoiling region
        """
        if label == "tetA":
            sc, coil, sc_ind = self.create_supercoil()
            gene = GenetetA(coil, sc_ind-1, local=self.local)
            return [gene, sc], coil, sc_ind
        else:
            return None

    def create_promoter(self, promoter_type, output, sc_region, weak=0, strong=1):
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
            Index of supercoil region the promoter is in.n
        weak            :   float
            output rate of weak signals
        strong          :   float
            output rate of strong signals

        Returns
        --------
        List<>
            Component list either environment and promoter or just the promoter.
        """
        components = []
        if output not in self.local.get_keys():
            queue = Queue()
            env = self.create_environment(output, queue)
            self.env_queues[output] = queue
            components.append(env)
        if promoter_type == "P":
            promoter = Promoter(output, sc_region, self.local, weak=weak, strong=strong,
                                output_channel=self.env_queues[output])
            components.append(promoter)
        elif promoter_type == "C":
            promoter = SupercoilSensitive(output, sc_region, self.local, weak=weak, strong=strong,
                                          output_channel=self.env_queues[output])
            components.append(promoter)
        elif promoter_type == "CF":
            promoter = SupercoilSensitive(output, sc_region, self.local, weak=weak, strong=strong,
                                          output_channel=self.env_queues[output], fluorescent=True)
            components.append(promoter)
        return components

    def create_barrier(self, barrier_type, sensor_input, current_ind, init_sc_coil=None):
        """
        Generates a barrier point, and new supercoiling regions and environments if needed, of type from list: bridge,
        origin

        Parameters
        ----------
        barrier_type    :   String
            type of barrier to be created.
        sensor_input    :   String
            protein to be detected in environment to turn barrier on or off
        current_ind     :   Int
            index of the supercoiling region anti-clockwise of the barrier.
        init_sc         :   Supercoil
            the initial supercoiling region for plasmids which need to connect last to first using the origin of
            replication barrier.

        Returns
        -------
        List<>
            Components: supercoil region, environment(if needed), barrier
        ChannelEnd
            channel for modifying the new supercoiling region clockwise of the barrier,
        Int
            Index of new clockwise supercoiling region
        """
        components = []
        if barrier_type != "origin":
            sc, coil, sc_ind = self.create_supercoil()
            components.append(sc)
        else:
            sc_ind = 0
            coil = init_sc_coil
        if sensor_input and sensor_input not in self.local.get_keys():
            queue = Queue()
            env = self.create_environment(sensor_input, queue)
            self.env_queues[sensor_input] = queue
            components.append(env)
        if barrier_type == "bridge":
            bridge = Bridge(sensor_input, self.local, current_ind, sc_ind, coil)
            components.append(bridge)
        if barrier_type == "origin":
            origin = Origin("Origin", self.local, current_ind, sc_ind, coil)
            components.append(origin)
        return components, coil, sc_ind

    def create_supercoil(self):
        """
        Generate a new supercoil region.

        Returns
        -------
        Supercoil
            The new supercoiling region component
        ChannelEnd
            The channel to the new supercoiling region
        Int
            The index of the new supercoiling region
        """
        sc_coil, gene_coil = Channel()
        supercoil = Supercoil(sc_coil, self.local)
        return supercoil, gene_coil, supercoil.supercoiling_region

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
