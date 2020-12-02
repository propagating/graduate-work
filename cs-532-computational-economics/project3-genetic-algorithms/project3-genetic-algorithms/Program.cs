using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace project3_genetic_algorithms
{
    class Program
    {
        static void Main(string[] args)
        {
            var solver = new GeneticSolver();
            var players = solver.GeneratePlayers(solver.Configuration.TotalPlayers);
            var eliminationMethods = (EliminationMethod[])Enum.GetValues(typeof(EliminationMethod));
            solver.SimulatePeriods(players);
            foreach(var method in eliminationMethods)
            {
                solver.Configuration.Elimination = method;
                var currentGeneration = 0;
                var bestPerGeneration = new List<Player>();
                while (currentGeneration < solver.Configuration.NumberOfGenerations)
                {
                    var parents = solver.FindParents(players);
                    var bestPlayer = players.OrderByDescending(x => x.CurrentLifeEnjoyment).FirstOrDefault();
                    bestPerGeneration.Add(bestPlayer);
                    var parentPairs = HelperMethods.UniquePairs(parents).ToList(); //generates unique pairings of parents
                    players = new List<Player>(); //clear out previous list of players so that we can use the same list for the newly generated children
                    foreach (var pair in parentPairs)
                    {
                        var parentChildren = solver.GenerateChildrenFromParents(pair.ToList());
                        players.AddRange(parentChildren);
                    }
                    currentGeneration++;
                    solver.SimulatePeriods(players);
                }

                var best = bestPerGeneration.OrderByDescending(x => x.CurrentLifeEnjoyment).FirstOrDefault();
                Console.WriteLine($"Best Player Found for {method.ToString()} Elimination");
                Console.WriteLine($"Total Life Enjoyment: {best.CurrentLifeEnjoyment}");
                Console.WriteLine("Investment Ratios per Period");
                foreach (var period in best.PlayPeriods)
                {
                    Console.WriteLine($"Period : {period.PeriodNumber}\nHealth Investment : {period.HealthInvestmentRatio}\nLife Investment : {period.LifeInvestmentRatio}");
                }
                Console.WriteLine();
            }

            Console.WriteLine("Thanks for playing");
            Console.ReadLine();
        }
    }

    public class GeneticSolver
    {
        public ProgramConfiguration Configuration { get; set; }

        public void SimulatePeriods(List<Player> players)
        {
            foreach (var player in players)
            {
                foreach (var period in player.PlayPeriods.OrderBy(x => x.PeriodNumber))
                {
                    if (player.CurrentHealth == 0) continue;
                    player.FindMaxRowsHarvested(); //updates available rows for harvest
                    player.CurrentHarvestValue += player.FindHarvestValue(); //calculates number of dots * dot value by area taken up by harvest area, adds to total player harvest amount

                    var amountHealthInvested = player.CalculateHealthInvestmentAmount(period);
                    var amountLifeInvested   = player.CalculateLifeInvestmentAmount(period);
                    player.CurrentHarvestValue -= amountHealthInvested;
                    player.CurrentHarvestValue -= amountLifeInvested;

                    player.UpdateCurrentHealth(period.PeriodNumber, amountHealthInvested);
                    player.CurrentLifeEnjoyment += player.CalculateLifeEnjoyment(amountLifeInvested);
                }
            }
        }

        #region ParentSelection

        public List<Player> FindParents(List<Player> players)
        {
            List<Player> parents;
            switch (Configuration.Elimination)
            {
                case EliminationMethod.Elitism:
                    parents = players.OrderByDescending(x => x.CurrentLifeEnjoyment).Take(Configuration.ParentsPerGeneration).ToList(); //take top parents
                    break;
                case EliminationMethod.Tournament:
                    parents = RunTournament(20, players);
                    break;
                case EliminationMethod.Roulette:
                    parents = RunRouletteSelection(players);
                    break;
                case EliminationMethod.Rank:
                    parents = RunRankSelection(players);
                    break;
                case EliminationMethod.SplitVote:
                    parents = RunSplitVote(players);
                    break;
                default:
                    parents = players.OrderByDescending(x => x.CurrentLifeEnjoyment).Take(Configuration.ParentsPerGeneration).ToList(); //default to elitism
                    break;
            }

            return parents;
        }

        private List<Player> RunRankSelection(List<Player> players)
        {
            var playerCount = players.Count;
            var orderedPlayers = players.OrderBy(x => x.CurrentLifeEnjoyment).ToList();
            var totalFitness = (playerCount + 1.0) * playerCount / 2.0;
            var totalProbability = 0.0;
            for (var i = 0; i < playerCount; i++)
            {
                var prob = i / totalFitness;
                orderedPlayers[i].SelectionProbability = prob;
                totalProbability += prob;
            }

            var selectedPlayers = new List<Player>();
            var selectedCount = 0;

            while (selectedCount < Configuration.ParentsPerGeneration)
            {
                var targetProbability = HelperMethods.RandomNumberBetween(0.0, totalProbability);
                var currentProbability = 0.0;
                var index = -1;
                while (currentProbability < targetProbability)
                {
                    index++;
                    if (index >= playerCount)
                    {
                        index--;
                        break;
                    }
                    currentProbability += orderedPlayers[index].SelectionProbability;
                }
                selectedPlayers.Add(orderedPlayers[index]);
                selectedCount++;
            }

            return selectedPlayers;
        }

        private List<Player> RunRouletteSelection(List<Player> players)
        {
            var playerCount = players.Count;
            var orderedPlayers = players.OrderBy(x => x.CurrentLifeEnjoyment).ToList();
            var totalFitness = orderedPlayers.Sum(x => x.CurrentLifeEnjoyment);

            var totalProbability = 0.0;
            for (var i = 0; i < playerCount; i++)
            {
                var prob = orderedPlayers[i].CurrentLifeEnjoyment / totalFitness;
                orderedPlayers[i].SelectionProbability = prob;
                totalProbability += prob;
            }

            var selectedPlayers = new List<Player>();
            var selectedCount = 0;
            while (selectedCount < Configuration.ParentsPerGeneration)
            {
                var targetProbability = HelperMethods.RandomNumberBetween(0.0, totalProbability);
                var currentProbability = 0.0;
                var index = -1;
                while (currentProbability < targetProbability)
                {
                    index++;
                    if (index >= playerCount)
                    {
                        index--;
                        break;
                    }
                    currentProbability += orderedPlayers[index].SelectionProbability;

                }
                selectedPlayers.Add(orderedPlayers[index]);
                selectedCount++;
            }

            return selectedPlayers;
        }

        private List<Player> RunSplitVote(List<Player> players)
        {

            var worstPlayers    = players.OrderBy(x => x.CurrentLifeEnjoyment).Take(Configuration.ParentsPerGeneration).ToList();
            var bestPlayers     = players.OrderByDescending(x => x.CurrentLifeEnjoyment).Take(Configuration.ParentsPerGeneration).ToList();
            var combinedPlayers = bestPlayers.Union(worstPlayers).ToList();

            return combinedPlayers.OrderBy(x => Guid.NewGuid()).Take(Configuration.ParentsPerGeneration)
                                  .ToList(); // randomly select parents between best and worst
        }

        private List<Player> RunTournament(int tournamentSize, List<Player> players)
        {
            var winningPlayers = new List<Player>();
            var playerCount = 0;
            while (playerCount < Configuration.ParentsPerGeneration)
            {
                var tournamentPlayers =  players.OrderBy(x => Guid.NewGuid()).Take(tournamentSize).ToList(); //get 20 random players
                var winningPlayer = tournamentPlayers.OrderByDescending(x => x.CurrentLifeEnjoyment).FirstOrDefault();//select best player
                players.Remove(winningPlayer);//remove winning player from list of players
                winningPlayers.Add(winningPlayer);
                playerCount++;
            }

            return winningPlayers;
        }

        #endregion

        #region Mutation Functions

        private Period MutateChildPlayPeriod(ValueTuple<decimal, decimal> investmentRatio,Period parentAPeriod, Period parentBPeriod)
        {
            var doParentCrossOver = HelperMethods.RandomNumberBetween(0.0, 1.0);
            if (doParentCrossOver < Configuration.CrossoverChance)
            {
                investmentRatio = ProcessParentCrossOver(parentAPeriod, parentBPeriod);
            }

            var doSwapOver = HelperMethods.RandomNumberBetween(0.0, 1.0);
            if (doSwapOver < Configuration.SwapoverChance)
            {
                investmentRatio = ProcessSwapOver(investmentRatio);
            }

            var doMutate = HelperMethods.RandomNumberBetween(0.0, 1.0);
            if (doMutate < Configuration.MutationChance)
            {
                investmentRatio = ProcessMutate(investmentRatio);
            }


            var period = new Period
            {
                PeriodNumber          = parentAPeriod.PeriodNumber,
                HealthInvestmentRatio = investmentRatio.Item1,
                LifeInvestmentRatio   = investmentRatio.Item2,
                HarvestValue          = 0,
                LifeEnjoyment         = 0,
            };
            return period;
        }

        private ValueTuple<decimal, decimal> ProcessMutate(ValueTuple<decimal, decimal> investmentRatio)
        {
            var mutateHealthAmount = Convert.ToDecimal(HelperMethods.RandomNumberBetween(-Configuration.MaxMutationRate, Configuration.MaxMutationRate)) * investmentRatio.Item1;
            var mutateLifeAmount   = Convert.ToDecimal(HelperMethods.RandomNumberBetween(-Configuration.MaxMutationRate, Configuration.MaxMutationRate)) * investmentRatio.Item2;

            var mutatedHealth = investmentRatio.Item1 + mutateHealthAmount;
            var mutatedLife = investmentRatio.Item2 + mutateLifeAmount;

            var stepSize     = 0.01m;
            var healthWeight = mutatedHealth / (mutatedHealth + mutatedLife);
            var lifeWeight   = 1.0m - healthWeight;
            while (mutatedHealth + mutatedLife > 1.0m)
            {
                mutatedHealth -= stepSize * healthWeight;
                mutatedLife   -= stepSize * lifeWeight;
            }

            return new ValueTuple<decimal, decimal>(mutatedHealth, mutatedLife);
        }

        private ValueTuple<decimal, decimal> ProcessSwapOver(ValueTuple<decimal, decimal> investmentRatio)
        {
            return new ValueTuple<decimal, decimal>(investmentRatio.Item2, investmentRatio.Item1);
        }

        private ValueTuple<decimal, decimal> ProcessParentCrossOver(Period parentAPeriod, Period parentBPeriod)
        {
            var healthParentChoice = HelperMethods.RandomNumberBetween(0.0, 1.0);
            var lifeParentChoice   = HelperMethods.RandomNumberBetween(0.0, 1.0);

            var healthRatio  = healthParentChoice >= 0.5 ? parentAPeriod.HealthInvestmentRatio: parentBPeriod.HealthInvestmentRatio;
            var lifeRatio    = lifeParentChoice >= 0.5 ? parentAPeriod.LifeInvestmentRatio    : parentBPeriod.LifeInvestmentRatio;

            var stepSize     = 0.01m;
            var healthWeight = healthRatio / (healthRatio + lifeRatio);
            var lifeWeight   = 1.0m - healthWeight;

            while (healthRatio + lifeRatio > 1.0m)
            {
                healthRatio -= stepSize * healthWeight;
                lifeRatio   -= stepSize * lifeWeight;
            }

            return new ValueTuple<decimal, decimal>(healthRatio,lifeRatio);
        }

        #endregion

        #region GeneratePlayers

        public List<Player> GeneratePlayers(int totalPlayers)
        {
            var currentPlayers = 0;
            var players = new List<Player>();
            while (currentPlayers < totalPlayers)
            {
                currentPlayers++;
                var player = new Player();

                var currentPeriod = 0;
                while (currentPeriod < PlayerConfiguration.Periods)
                {
                    currentPeriod++;
                    var investmentRatios = player.GenerateLifeHealthInvestmentRatio(); //ensures that combined ratios aren't above 1

                    var period = new Period
                    {
                        PeriodNumber          = currentPeriod,
                        HealthInvestmentRatio = investmentRatios.Item1,
                        LifeInvestmentRatio   = investmentRatios.Item2,
                        HarvestValue          = 0,
                        LifeEnjoyment         = 0,

                    };
                    player.PlayPeriods.Add(period);
                }
                players.Add(player);
            }

            return players;
        }

        public List<Player> GenerateChildrenFromParents(List<Player> parentPair)
        {
            var children = new List<Player>();
            var parentA = parentPair.FirstOrDefault();
            var parentB = parentPair.LastOrDefault();

            var childrenCount = 0;
            while (childrenCount < Configuration.ChildrenPerParentPair) //cause I don't like for loops when I can avoid them
            {
                var child = new Player();

                var parentAPeriods = parentA.PlayPeriods;
                foreach (var parentAPeriod in parentAPeriods)
                {
                    var parentBPeriod = parentB.PlayPeriods.FirstOrDefault(x => x.PeriodNumber == parentAPeriod.PeriodNumber);
                    var investmentRatio = child.GenerateLifeHealthInvestmentRatio(); //default generation in case no flips pass
                    var childPeriod = MutateChildPlayPeriod(investmentRatio, parentAPeriod, parentBPeriod);
                    child.PlayPeriods.Add(childPeriod);
                }
                children.Add(child);

                childrenCount++; //faster than counting num elements in a list every time
            }

            return children;
        }

        #endregion


        public GeneticSolver(EliminationMethod eliminationMethod)
        {
            Configuration = new ProgramConfiguration
            {
                Elimination = eliminationMethod
            };
        }

        public GeneticSolver()
        {
            Configuration = new ProgramConfiguration();
        }
    }
}
