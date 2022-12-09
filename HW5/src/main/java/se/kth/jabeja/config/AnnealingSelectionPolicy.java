package se.kth.jabeja.config;

/**
 * Select the simulated annealing policy (linear, exponential).
 */
public enum AnnealingSelectionPolicy {
    LINEAR("LINEAR"),
    EXPONENTIAL("EXPONENTIAL");

    String name;

    AnnealingSelectionPolicy(String name) {
        this.name = name;
    }

    @Override
    public String toString() {
        return name;
    }
}
