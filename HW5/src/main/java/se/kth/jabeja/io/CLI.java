package se.kth.jabeja.io;

import org.apache.log4j.Logger;
import org.kohsuke.args4j.CmdLineParser;
import org.kohsuke.args4j.Option;
import se.kth.jabeja.config.Config;
import se.kth.jabeja.config.AnnealingSelectionPolicy;
import se.kth.jabeja.config.GraphInitColorPolicy;
import se.kth.jabeja.config.NodeSelectionPolicy;

import java.io.File;
import java.io.FileNotFoundException;

/**
 * Created by salman on 10/25/16.
 */
public class CLI {
  final static Logger logger = Logger.getLogger(CLI.class);

  @Option(name = "-help", usage = "Print usages.")
  private boolean HELP = false;

  @Option(name = "-rounds", usage = "Number of rounds.")
  private int ROUNDS = 1000;

  @Option(name = "-numPartitions", usage = "Number of partitions.")
  private int NUM_PARTITIONS = 4;

  @Option(name = "-uniformRandSampleSize", usage = "Uniform random sample size.")
  private int UNIFORM_RAND_SAMPLE_SIZE = 6;

  @Option(name = "-temp", usage = "Simulated annealing temperature.")
  private float TEMPERATURE = 2;

  @Option(name = "-delta", usage = "Simulated annealing delta.")
  private float DELTA = (float) 0.005;

  @Option(name = "-seed", usage = "Seed.")
  private int SEED = 0;

  @Option(name = "-alpha", usage = "Alpha parameter")
  private float ALPHA = 2;

  @Option(name = "-randNeighborsSampleSize", usage = "Number of random neighbors sample size.")
  private int randNeighborsSampleSize = 3;

  @Option(name = "-annealingSelectionPolicy", usage = "Annealing selection policy. Supported, LINEAR, EXPONENTIAL")
  private String ANNEALING_POLICY = "LINEAR";
  private AnnealingSelectionPolicy annealingPolicy = AnnealingSelectionPolicy.LINEAR;

  @Option(name = "-graphInitColorSelectionPolicy", usage = "Initial color selection policy. Supported, RANDOM, ROUND_ROBIN, BATCH")
  private String GRAPH_INIT_COLOR_SELECTION_POLICY = "ROUND_ROBIN";
  private GraphInitColorPolicy graphInitColorSelectionPolicy = GraphInitColorPolicy.ROUND_ROBIN;

  @Option(name = "-nodeSelectionPolicy", usage = "Node selection policy. Supported, RANDOM, LOCAL, HYBRID")
  private String NODE_SELECTION_POLICY = "LOCAL";
  private NodeSelectionPolicy nodeSelectionPolicy = NodeSelectionPolicy.LOCAL;

  @Option(name = "-restart-temp", usage = "Restart temperature if edge cut has remained constant for ROUNDS_RESTART rounds.")
  private boolean restartTemp = false;

  @Option(name = "-rounds-restart", usage = "Number of rounds with constant edge cut seen before temperature is restarted.")
  private int roundsRestart = 100;

  @Option(name = "-delta-decay", usage = "Decay rate for delta parameter which is applied each time the temperature is restarted.")
  private float deltaDecay = 0;

  @Option(name = "-graph", usage = "Location of the input graph.")
  private static String GRAPH = "./graphs/ws-250.graph";

  @Option(name = "-outputDir", usage = "Location of the output file(s)")
  private static String OUTPUT_DIR = "./output";

  public Config parseArgs(String[] args) throws FileNotFoundException {
    CmdLineParser parser = new CmdLineParser(this);
    parser.setUsageWidth(80);
    try {
      // parse the arguments.
      parser.parseArgument(args);
      if (GRAPH_INIT_COLOR_SELECTION_POLICY.compareToIgnoreCase(GraphInitColorPolicy.RANDOM.toString()) == 0) {
        graphInitColorSelectionPolicy = GraphInitColorPolicy.RANDOM;
      } else if (GRAPH_INIT_COLOR_SELECTION_POLICY.compareToIgnoreCase(GraphInitColorPolicy.BATCH.toString()) == 0) {
        graphInitColorSelectionPolicy = GraphInitColorPolicy.BATCH;
      } else if (GRAPH_INIT_COLOR_SELECTION_POLICY.compareToIgnoreCase(GraphInitColorPolicy.ROUND_ROBIN.toString()) == 0) {
        graphInitColorSelectionPolicy = GraphInitColorPolicy.ROUND_ROBIN;
      } else {
        throw new IllegalArgumentException("Initial color selection policy is not supported");
      }

      if (NODE_SELECTION_POLICY.compareToIgnoreCase(NodeSelectionPolicy.RANDOM.toString()) == 0) {
        nodeSelectionPolicy = NodeSelectionPolicy.RANDOM;
      } else if (NODE_SELECTION_POLICY.compareToIgnoreCase(NodeSelectionPolicy.LOCAL.toString()) == 0) {
        nodeSelectionPolicy = NodeSelectionPolicy.LOCAL;
      } else if (NODE_SELECTION_POLICY.compareToIgnoreCase(NodeSelectionPolicy.HYBRID.toString()) == 0) {
        nodeSelectionPolicy = NodeSelectionPolicy.HYBRID;
      } else {
        throw new IllegalArgumentException("Node selection policy is not supported");
      }

      if (ANNEALING_POLICY.compareToIgnoreCase(AnnealingSelectionPolicy.LINEAR.toString()) == 0) {
        annealingPolicy = AnnealingSelectionPolicy.LINEAR;
      } else if (ANNEALING_POLICY.compareToIgnoreCase(AnnealingSelectionPolicy.EXPONENTIAL.toString()) == 0) {
        annealingPolicy = AnnealingSelectionPolicy.EXPONENTIAL;
      } else if (ANNEALING_POLICY.compareToIgnoreCase(AnnealingSelectionPolicy.IMPROVED_EXP.toString()) == 0) {
        annealingPolicy = AnnealingSelectionPolicy.IMPROVED_EXP;
      } else {
        throw new IllegalArgumentException("Annealing selection policy is not supported");
      }

    } catch (Exception e) {
      logger.error(e.getMessage());
      parser.printUsage(System.err);
      System.exit(-1);
    }

    File graphFile = new File(GRAPH);
    if (!graphFile.exists() || !graphFile.isFile()) {
      throw new FileNotFoundException("Graph file does not exist.");
    }

    if (HELP) {
      parser.printUsage(System.out);
      System.exit(0);
    }

    return new Config().setRandNeighborsSampleSize(randNeighborsSampleSize)
            .setDelta(DELTA)
            .setNumPartitions(NUM_PARTITIONS)
            .setUniformRandSampleSize(UNIFORM_RAND_SAMPLE_SIZE)
            .setRounds(ROUNDS)
            .setSeed(SEED)
            .setTemperature(TEMPERATURE)
            .setGraphFilePath(GRAPH)
            .setAnnealingSelectionPolicy(annealingPolicy)
            .setNodeSelectionPolicy(nodeSelectionPolicy)
            .setGraphInitialColorPolicy(graphInitColorSelectionPolicy)
            .setRestartTemp(restartTemp)
            .setRoundsRestart(roundsRestart)
            .setDeltaDecay(deltaDecay)
            .setOutputDir(OUTPUT_DIR)
            .setAlpha(ALPHA);
  }
}
