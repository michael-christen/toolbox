import networkx


def main() -> None:
    # Create a NetworkX graph
    # G = networkx.fast_gnp_random_graph(100, 0.1, directed=True)
    G = networkx.gnr_graph(100, 0.1)


if __name__ == "__main__":
    main()
