import logging
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from heapq import heapify, heappop, heappush
from typing import ClassVar

import click
import numpy as np
import scipy.stats as stats
import simpy

logging.basicConfig(level="DEBUG", format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


@dataclass
class Customer:
    arrival_time: float

    _service_start_time: float | None = None
    _service_time: float | None = None

    _customer_id: ClassVar[int] = 0

    @property
    def departure_time(self) -> float:
        if self.service_start_time is None:
            raise ValueError("Service has not started yet.")  # noqa: TRY003
        return self.service_start_time + self.service_time

    @property
    def service_start_time(self) -> float:
        if self._service_start_time is None:
            raise ValueError("Service has not started yet.")  # noqa: TRY003
        return self._service_start_time

    @service_start_time.setter
    def service_start_time(self, value: float) -> None:
        self._service_start_time = value

    @property
    def service_time(self) -> float:
        if self._service_time is None:
            raise ValueError("Service has not started yet.")  # noqa: TRY003
        return self._service_time

    @service_time.setter
    def service_time(self, value: float) -> None:
        self._service_time = value

    def __post_init__(self):
        self.customer_id = Customer._customer_id
        Customer._customer_id += 1
        logger.debug(f"{self.arrival_time:.4f}: #{self.customer_id} arrives")

    def run(
        self,
        env: simpy.Environment,
        server: simpy.PriorityResource,
        server_ids: list[int],
        service_time_rvs: list[stats.rv_continuous],
    ):
        with server.request(priority=self.arrival_time) as req:  # type: ignore  # noqa: PGH003
            yield req
            self.server_id = heappop(server_ids)
            self.service_start_time = env.now
            self.service_time = service_time_rvs[self.server_id].rvs()
            logger.debug(
                f"{self.service_start_time:.4f}: #{self.customer_id} starts service on server {self.server_id}"
            )

            yield env.timeout(self.service_time)
            logger.debug(f"{env.now:.4f}: #{self.customer_id} ends service on server {self.server_id}")
            heappush(server_ids, self.server_id)


class ServerSystem:
    def __init__(
        self,
        arrival_end_time: float,
        interarrival_time_rv: stats.rv_continuous,
        service_time_rvs: list[stats.rv_continuous],
    ):
        self.env = simpy.Environment()
        self.arrival_end_time = arrival_end_time
        self.interarrival_time_rv = interarrival_time_rv

        self.num_servers = len(service_time_rvs)
        self.service_time_rvs = service_time_rvs
        self.server = simpy.PriorityResource(self.env, capacity=self.num_servers)
        self.server_ids = list(range(self.num_servers))

        heapify(self.server_ids)
        self.customers: list[Customer] = []

    def generate_interarrival_time(self):
        return self.interarrival_time_rv.rvs()

    def arrival(self):
        while self.env.now <= self.arrival_end_time:
            interarrival_time = self.generate_interarrival_time()
            yield self.env.timeout(interarrival_time)
            if self.env.now > self.arrival_end_time:
                break

            customer = Customer(arrival_time=self.env.now)
            self.customers.append(customer)
            self.env.process(customer.run(self.env, self.server, self.server_ids, self.service_time_rvs))

    def run(self, seed: int = 42) -> None:
        np.random.seed(seed)
        logger.info("Starting simulation...")
        self.env.process(self.arrival())
        self.env.run()

    def summary(self) -> tuple[int, float, float, dict[int, int]]:
        total_customers = len(self.customers)
        end_time = max(c.departure_time for c in self.customers) if total_customers > 0 else 0.0
        average_spent_time = (
            np.mean([c.departure_time - c.arrival_time for c in self.customers]) if total_customers > 0 else 0.0
        )
        customers_per_server = [0 for _ in range(self.num_servers)]
        for customer in self.customers:
            customers_per_server[customer.server_id] += 1
        logger.info(f"Total customers served: {total_customers}")
        logger.info(f"End of service time: {end_time:.2f}")
        logger.info(f"Average spent time: {average_spent_time:.2f}")
        logger.info(f"Customers per server: {customers_per_server}")

        return total_customers, end_time, average_spent_time, customers_per_server  # type: ignore  # noqa: PGH003


def run_single_simulation(
    seed: int,
    arrival_end_time: float,
    interarrival_time_rv: stats.rv_continuous,
    service_time_rvs: list[stats.rv_continuous],
):
    rng = np.random.default_rng(seed)
    interarrival_time_rv.random_state = rng
    for rv in service_time_rvs:
        rv.random_state = rng

    server_system = ServerSystem(
        arrival_end_time=arrival_end_time,
        interarrival_time_rv=interarrival_time_rv,
        service_time_rvs=service_time_rvs,
    )
    server_system.run(seed=seed)
    return server_system.summary()


class Simulation:
    def __init__(
        self,
        number_of_simulations: int,
        arrival_end_time: float,
        interarrival_time_rv: stats.rv_continuous,
        service_time_rvs: list[stats.rv_continuous],
    ):
        self.number_of_simulations = number_of_simulations
        self.arrival_end_time = arrival_end_time
        self.interarrival_time_rv = interarrival_time_rv
        self.service_time_rvs = service_time_rvs
        self.total_customers_per_simulation = []
        self.end_times_per_simulation = []
        self.average_spent_times_per_simulation = []
        self.customers_per_server_per_simulation = []

        self.run()

    def run(self):
        logger.info(f"Starting {self.number_of_simulations} simulations...")
        logger.disabled = True

        with ProcessPoolExecutor() as executor:
            results = list(
                executor.map(
                    run_single_simulation,
                    range(self.number_of_simulations),
                    [self.arrival_end_time] * self.number_of_simulations,
                    [self.interarrival_time_rv] * self.number_of_simulations,
                    [self.service_time_rvs] * self.number_of_simulations,
                )
            )

        for total_customers, end_time, average_spent_time, customers_per_server in results:
            self.total_customers_per_simulation.append(total_customers)
            self.end_times_per_simulation.append(end_time)
            self.average_spent_times_per_simulation.append(average_spent_time)
            self.customers_per_server_per_simulation.append(customers_per_server)

        logger.disabled = False
        logger.info(f"Completed {self.number_of_simulations} simulations.")

    def summary(self):
        avg_total_customers = np.mean(self.total_customers_per_simulation)
        logger.info(
            f"Average number of customers served: {avg_total_customers:.2f} "
            + f"(std: {np.std(self.total_customers_per_simulation):.2f})"
        )
        logger.info(
            f"Average end of service time: {np.mean(self.end_times_per_simulation):.2f} "
            + f"(std: {np.std(self.end_times_per_simulation):.2f})"
        )
        logger.info(
            f"Average spent time: {np.mean(self.average_spent_times_per_simulation):.2f} "
            + f"(std: {np.std(self.average_spent_times_per_simulation):.2})"
        )

        avg_customers_per_server = np.mean(self.customers_per_server_per_simulation, axis=0)
        std_customers_per_server = np.std(self.customers_per_server_per_simulation, axis=0)
        for i, (avg, std) in enumerate(zip(avg_customers_per_server, std_customers_per_server)):
            logger.info(
                f"Average number of customers served on server {i}: {avg:.2f} (std: {std:.2f}), ratio: {avg / avg_total_customers:.4f}"
            )
        logger.info("Simulation completed.")


@click.command()
@click.option(
    "--exercise",
    type=click.Choice(["1", "2"], case_sensitive=False),
    required=True,
    help="Choose the exercise to run: '1' or '2'.",
)
@click.option(
    "--number-of-simulations",
    type=int,
    default=100,
    help="Set the number of simulations to run (default: 100).",
)
def main(exercise: str, number_of_simulations: int):
    if exercise == "1":
        interarrival_time_rv = stats.expon(scale=1 / 10)
        service_time_rvs = [stats.gamma(a=3, scale=1 / 40)]
    elif exercise == "2":
        interarrival_time_rv = stats.expon(scale=1 / 6)
        service_time_rvs = [stats.expon(scale=1 / 4), stats.expon(scale=1 / 3)]

    simulation = Simulation(
        number_of_simulations=number_of_simulations,
        arrival_end_time=9.0,
        interarrival_time_rv=interarrival_time_rv,  # type: ignore  # noqa: PGH003
        service_time_rvs=service_time_rvs,  # type: ignore  # noqa: PGH003
    )
    simulation.summary()


if __name__ == "__main__":
    main()
