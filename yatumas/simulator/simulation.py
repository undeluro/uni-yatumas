import blessed
from yatumas.simulator.controller import Controller
from yatumas.simulator.view import View
from yatumas.simulator.model import Model
from yatumas.machine.symbol import Symbol
from yatumas.machine.machine import Machine


class GraphicalSimulation:
    """
    Class responsible for the whole graphical simulation.
    It is built according to the Model-View-Controller design pattern:
    - https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller
    - https://www.techtarget.com/whatis/definition/model-view-controller-MVC

    We assume the classical architecture, where:
    - model contains all the information about the state
    - view just displays the state stored in the model
    - controller:
      * reads input from the user and updates the model.
      * decides when the view should be refreshed/rendered.

    Methods
    -------
    def run() -> None:
        runs the simulation

    Protected Attributes
    --------------------
    _model:
        the model component of the MVC
    _view:
        the view component of the MVC
    _controller
        the controller component of the MVC
    """

    _model: Model
    _view: View
    _controller: Controller

    def __init__(
        self,
        machine: Machine,
        machine_input: list[Symbol],
        step_interval_in_sec: float,
    ):
        """
        Initializes the simulation with the given parameters.

        Parameters
        ----------
        machine: Machine
            machine being simulated
        machine_input: list[Symbol]
            the initial input of the machine
        step_interval_in_sec: float
            how often the simulation should update its state
        """
        self._model = Model(machine, machine_input, step_interval_in_sec)
        term = blessed.Terminal()
        self._view = View(self._model, term)
        self._controller = Controller(self._model, self._view, term)

    def run(self):
        """
        Runs the simulation.
        """
        self._controller.run_simulation()
