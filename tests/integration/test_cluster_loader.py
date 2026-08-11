from cluster.ClusterLoader import load_cluster_inventory
from cluster.WorkerNode import WorkerNode
from simulation.Time import SimulationTime


def test_load_cluster_inventory_from_minimal_csvs(fixture_paths):
    inventory = load_cluster_inventory(
        fixture_paths.inventory_csv,
        fixture_paths.frequency_csv,
        cluster_name="TEST",
        strict=True,
    )

    assert len(inventory) == 1

    worker_node_class, quantity = next(iter(inventory.items()))
    assert quantity == 1

    simulation_time = SimulationTime(
        {
            "output": {
                "verbosity": "low",
            }
        },
        "2024-01-16 16:00",
    )
    worker_node = worker_node_class(simulation_time, "-001")

    assert isinstance(worker_node, WorkerNode)
    assert worker_node.hostname == "TESTNODE_0-001"
    assert worker_node.number_of_cores == 2
    assert worker_node.max_RAM == 8.0
    assert worker_node.powerusage_idle == 50.0 / 3600
    assert worker_node.frequencies_available == [3.0]
    assert worker_node.HEPScore_vs_frequency == [1939.60]


def test_load_cluster_inventory_respects_cluster_filter(fixture_paths):
    inventory = load_cluster_inventory(
        fixture_paths.inventory_csv,
        fixture_paths.frequency_csv,
        cluster_name="OTHER",
        strict=True,
    )

    assert inventory == {}
