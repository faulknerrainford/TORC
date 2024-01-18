import abc
from TORC import Supercoil


class Barrier:
    def __init__(self, local, cw_sc_region, acw_sc_region):
        """
        Barriers are components that can stop the propagation of supercoiling.

        Parameters
        ----------
        local           :   LocalArea
            Provides access to the variables in the plasmid that are visible to multiple components
        cw_sc_region    :   Supercoil
            The integer index of the supercoiling region clockwise(right) of the barrier
        acw_sc_region   :   Supercoil
            The integer index of the supercoiling region anticlockwise(left) of the barrier
        """
        if not isinstance(cw_sc_region, Supercoil):
            raise TypeError("clockwise region not a supercoil")
        if not isinstance(acw_sc_region, Supercoil):
            raise TypeError("anticlockwise region not a supercoil")
        self.cw_region = cw_sc_region
        self.acw_region = acw_sc_region
        self.local = local

    def update(self):
        """
        Checks if the barrier is open and propagates supercoiling if it is.

        """
        if self.barrier_check():
            self.sc_exchange()
            pass

    @abc.abstractmethod
    def barrier_check(self):
        """
        Reimplemented in subclasses, dictates if the barrier is open. If true then supercoiling exchange happens
        between the adjacent regions, else if false the barrier stops all supercoiling propagation.

        Returns
        -------
        Boolean
            True return indicates supercoiling propagation, false barrier is active

        """
        return False

    def sc_exchange(self):
        """
        Propagates supercoiling in correct direction based on the gene orientations between neighbouring supercoiling
        regions.

        """
        # cw = self.local.get_supercoil(self.cw_region)
        # acw = self.local.get_supercoil(self.acw_region)
        cw_cw_queue = self.local.get_supercoil_cw(self.cw_region.supercoiling_region)
        acw_acw_queue = self.local.get_supercoil_acw(self.acw_region.supercoiling_region)
        # read in cw region acw sc
        acw_value = self.cw_region.acw_sc
        # update acw region acw sc
        acw_acw_queue.put(acw_value)
        # read in acw region cw sc
        cw_value = self.acw_region.cw_sc
        # update cw region cw sc
        cw_cw_queue.put(cw_value)
