namespace project3_genetic_algorithms
{
    public class ProgramConfiguration
    {
        public int TotalPlayers { get; set; }
        public EliminationMethod Elimination { get; set; }
        public int ParentsPerGeneration { get; set; }
        public int ChildrenPerParentPair { get; set; }
        public double MaxMutationRate { get; set; }
        public double MutationChance { get; set; }
        public int NumberOfGenerations { get; set; }
        public double SwapoverChance { get; set; }
        public double CrossoverChance { get; set; }
        public ProgramConfiguration()
        {
            TotalPlayers          = 10000;
            ParentsPerGeneration  = 10;   //generates 45 unique pairs of parents
            Elimination           = EliminationMethod.Elitism;
            ChildrenPerParentPair = 50;   //total of 2250 children per generation (45 pairs * 50 children per pair);
            MaxMutationRate       = 0.20; //max amount the each rate can change in a single period. Both will change by a different amount if a mutation does occur
            MutationChance        = 0.3;  //chance of mutating after crossover
            CrossoverChance       = 0.7;  //chance a random parent's gene is used as is, without change
            SwapoverChance        = 0.2;  //similar to crossover, but the position of the investment swaps places after crossing over
            NumberOfGenerations   = 100;
        }


    }
}
