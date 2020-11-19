using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using CsvHelper;
using Google.OrTools.LinearSolver;

namespace ps2_fantasy_football
{
    class Program
    {
        static void Main(string[] args)
        {
            var currentDirectory = Directory.GetCurrentDirectory();
            var players = ParseCsv($"{currentDirectory}/data/fantasy_football_data.csv");
            var solverVariables = new List<Variable>();
            Solver solver = Solver.CreateSolver("SCIP");
            var budgetConstraints = new BudgetConstraints
            {
                Budget              = 200,
                RosterLength        = 15,
                MaxActiveQb         = 1,
                MaxActiveWr         = 3,
                MaxActiveRb         = 2,
                MaxActiveTe         = 1,
                MaxActiveK          = 1,
                MaxActiveDef        = 1,
                MaxQb               = 2,
                MaxTe               = 2,
                MaxK                = 1,
                MaxDef              = 1,
                MaxPlayerOccurrence = 1,
                MaxBenchedPlayers   = 6
            };


            //roster wide constraints
            var maxBudget     = solver.MakeConstraint(0, budgetConstraints.Budget           , "maxBudget");
            var maxRosterSize = solver.MakeConstraint(0, budgetConstraints.RosterLength     , "maxRoster");
            var maxBenchSize  = solver.MakeConstraint(0, budgetConstraints.MaxBenchedPlayers, "maxBenchSize");

            //max active roster slot constraints
            var activeQuarterbackPositions  = solver.MakeConstraint(0, budgetConstraints.MaxActiveQb , "maxActiveQuarterback");
            var activeRunningBackPositions  = solver.MakeConstraint(0, budgetConstraints.MaxActiveRb , "maxActiveRunningBack");
            var activeWideReceiverPositions = solver.MakeConstraint(0, budgetConstraints.MaxActiveWr , "maxActiveWideReceiver");
            var activeTightEndPositions     = solver.MakeConstraint(0, budgetConstraints.MaxActiveTe , "maxActiveTightEnd");
            var activeKickerPositions       = solver.MakeConstraint(0, budgetConstraints.MaxActiveK  , "maxActiveKicker");
            var activeDefenderPositions     = solver.MakeConstraint(0, budgetConstraints.MaxActiveDef, "maxActiveDefender");

            //max total roster slot constraints
            var totalQuarterbackPositions = solver.MakeConstraint(0, budgetConstraints.MaxQb , "maxQuarterback");
            var totalTightEndPositions    = solver.MakeConstraint(0, budgetConstraints.MaxTe , "maxTightEnd");
            var totalKickerPositions      = solver.MakeConstraint(0, budgetConstraints.MaxK  , "maxKicker");
            var totalDefenderPositions    = solver.MakeConstraint(0, budgetConstraints.MaxDef, "maxDefender");

            //rb bench position constraints
            var runningBackBenchPosition1 = solver.MakeConstraint(0, budgetConstraints.MaxPlayerOccurrence, "runningBackB1");
            var runningBackBenchPosition2 = solver.MakeConstraint(0, budgetConstraints.MaxPlayerOccurrence, "runningBackB2");
            var runningBackBenchPosition3 = solver.MakeConstraint(0, budgetConstraints.MaxPlayerOccurrence, "runningBackB3");
            var runningBackBenchPosition4 = solver.MakeConstraint(0, budgetConstraints.MaxPlayerOccurrence, "runningBackB4");
            var runningBackBenchPosition5 = solver.MakeConstraint(0, budgetConstraints.MaxPlayerOccurrence, "runningBackB5");
            var runningBackBenchPosition6 = solver.MakeConstraint(0, budgetConstraints.MaxPlayerOccurrence, "runningBackB6");

            //wr bench position constraints
            var wideReceiverBenchPosition1 = solver.MakeConstraint(0, budgetConstraints.MaxPlayerOccurrence, "wideReceiverB1");
            var wideReceiverBenchPosition2 = solver.MakeConstraint(0, budgetConstraints.MaxPlayerOccurrence, "wideReceiverB2");
            var wideReceiverBenchPosition3 = solver.MakeConstraint(0, budgetConstraints.MaxPlayerOccurrence, "wideReceiverB3");
            var wideReceiverBenchPosition4 = solver.MakeConstraint(0, budgetConstraints.MaxPlayerOccurrence, "wideReceiverB4");
            var wideReceiverBenchPosition5 = solver.MakeConstraint(0, budgetConstraints.MaxPlayerOccurrence, "wideReceiverB5");
            var wideReceiverBenchPosition6 = solver.MakeConstraint(0, budgetConstraints.MaxPlayerOccurrence, "wideReceiverB6");

            //create objective function
            var objectiveFunction            = solver.Objective();
            objectiveFunction.SetMaximization();

            foreach (var player in players)
            {
                //create player constraint
                var playIndicator = solver.MakeConstraint(0, budgetConstraints.MaxPlayerOccurrence, $"{player.Name} Active Player");
                switch (player.Position)
                {
                    case PlayPosition.Qb:

                        // create indicators for position and player constraints
                        var qbA = solver.MakeIntVar(0, 1, $"{player.Name} Active Quarterback");
                        var qb1 = solver.MakeIntVar(0, 1, $"{player.Name} Bench 1 Quarterback");

                        solverVariables.Add(qbA);
                        solverVariables.Add(qb1);

                        playIndicator.SetCoefficient(qbA, 1);
                        playIndicator.SetCoefficient(qb1, 1);

                        //add player cost to priceConstraints
                        maxBudget.SetCoefficient(qbA, player.Price);
                        maxBudget.SetCoefficient(qb1, player.Price);

                        //add player to roster constraint
                        maxRosterSize.SetCoefficient(qbA, 1);
                        maxRosterSize.SetCoefficient(qb1, 1);

                        //add player to total position Constraint
                        totalQuarterbackPositions.SetCoefficient(qbA, 1);
                        totalQuarterbackPositions.SetCoefficient(qb1, 1);

                        //add player to active position Constraint
                        activeQuarterbackPositions.SetCoefficient(qbA, 1);

                        //add player to total bench constraint
                        maxBenchSize.SetCoefficient(qb1, 1);

                        //add player points to objective function
                        objectiveFunction.SetCoefficient(qbA, player.ProjectedPoints);
                        objectiveFunction.SetCoefficient(qb1, Math.Pow(0.5, 1) * player.ProjectedPoints);
                        break;

                    case PlayPosition.Rb:

                        // create indicators for position and player constraints
                        var rbA = solver.MakeIntVar(0, 1, $"{player.Name} Active Running Back");
                        var rb1 = solver.MakeIntVar(0, 1, $"{player.Name} Bench 1 Running Back");
                        var rb2 = solver.MakeIntVar(0, 1, $"{player.Name} Bench 2 Running Back");
                        var rb3 = solver.MakeIntVar(0, 1, $"{player.Name} Bench 3 Running Back");
                        var rb4 = solver.MakeIntVar(0, 1, $"{player.Name} Bench 4 Running Back");
                        var rb5 = solver.MakeIntVar(0, 1, $"{player.Name} Bench 5 Running Back");
                        var rb6 = solver.MakeIntVar(0, 1, $"{player.Name} Bench 6 Running Back");

                        solverVariables.Add(rbA);
                        solverVariables.Add(rb1);
                        solverVariables.Add(rb2);
                        solverVariables.Add(rb3);
                        solverVariables.Add(rb4);
                        solverVariables.Add(rb5);
                        solverVariables.Add(rb6);

                        playIndicator.SetCoefficient(rbA,1);
                        playIndicator.SetCoefficient(rb1,1);
                        playIndicator.SetCoefficient(rb2,1);
                        playIndicator.SetCoefficient(rb3,1);
                        playIndicator.SetCoefficient(rb4,1);
                        playIndicator.SetCoefficient(rb5,1);
                        playIndicator.SetCoefficient(rb6,1);

                        //add player cost to priceConstraints
                        maxBudget.SetCoefficient(rbA, player.Price);
                        maxBudget.SetCoefficient(rb1, player.Price);
                        maxBudget.SetCoefficient(rb2, player.Price);
                        maxBudget.SetCoefficient(rb3, player.Price);
                        maxBudget.SetCoefficient(rb4, player.Price);
                        maxBudget.SetCoefficient(rb5, player.Price);
                        maxBudget.SetCoefficient(rb6, player.Price);

                        //add player to roster constraint
                        maxRosterSize.SetCoefficient(rbA,1);
                        maxRosterSize.SetCoefficient(rb1,1);
                        maxRosterSize.SetCoefficient(rb2,1);
                        maxRosterSize.SetCoefficient(rb3,1);
                        maxRosterSize.SetCoefficient(rb4,1);
                        maxRosterSize.SetCoefficient(rb5,1);
                        maxRosterSize.SetCoefficient(rb6,1);

                        //add player to active position Constraint
                        activeRunningBackPositions.SetCoefficient(rbA, 1);

                        //add player to total bench constraint;
                        maxBenchSize.SetCoefficient(rb1,1);
                        maxBenchSize.SetCoefficient(rb2,1);
                        maxBenchSize.SetCoefficient(rb3,1);
                        maxBenchSize.SetCoefficient(rb4,1);
                        maxBenchSize.SetCoefficient(rb5,1);
                        maxBenchSize.SetCoefficient(rb6,1);

                        //add player to bench position constraints
                        runningBackBenchPosition1.SetCoefficient(rb1,1);
                        runningBackBenchPosition2.SetCoefficient(rb2,1);
                        runningBackBenchPosition3.SetCoefficient(rb3,1);
                        runningBackBenchPosition4.SetCoefficient(rb4,1);
                        runningBackBenchPosition5.SetCoefficient(rb5,1);
                        runningBackBenchPosition6.SetCoefficient(rb6,1);

                        //add player points to objective function
                        objectiveFunction.SetCoefficient(rbA,player.ProjectedPoints);
                        objectiveFunction.SetCoefficient(rb1,Math.Pow(0.5, 1) * player.ProjectedPoints);
                        objectiveFunction.SetCoefficient(rb2,Math.Pow(0.5, 2) * player.ProjectedPoints);
                        objectiveFunction.SetCoefficient(rb3,Math.Pow(0.5, 3) * player.ProjectedPoints);
                        objectiveFunction.SetCoefficient(rb4,Math.Pow(0.5, 4) * player.ProjectedPoints);
                        objectiveFunction.SetCoefficient(rb5,Math.Pow(0.5, 5) * player.ProjectedPoints);
                        objectiveFunction.SetCoefficient(rb6,Math.Pow(0.5, 6) * player.ProjectedPoints);
                        break;

                    case PlayPosition.Wr:

                        // create indicators for position and player constraints
                        var wrA = solver.MakeIntVar(0, 1, $"{player.Name} Active Wide Receiver");
                        var wr1 = solver.MakeIntVar(0, 1, $"{player.Name} Bench 1 Wide Receiver");
                        var wr2 = solver.MakeIntVar(0, 1, $"{player.Name} Bench 2 Wide Receiver");
                        var wr3 = solver.MakeIntVar(0, 1, $"{player.Name} Bench 3 Wide Receiver");
                        var wr4 = solver.MakeIntVar(0, 1, $"{player.Name} Bench 4 Wide Receiver");
                        var wr5 = solver.MakeIntVar(0, 1, $"{player.Name} Bench 5 Wide Receiver");
                        var wr6 = solver.MakeIntVar(0, 1, $"{player.Name} Bench 6 Wide Receiver");

                        solverVariables.Add(wrA);
                        solverVariables.Add(wr1);
                        solverVariables.Add(wr2);
                        solverVariables.Add(wr3);
                        solverVariables.Add(wr4);
                        solverVariables.Add(wr5);
                        solverVariables.Add(wr6);

                        playIndicator.SetCoefficient(wrA,1);
                        playIndicator.SetCoefficient(wr1,1);
                        playIndicator.SetCoefficient(wr2,1);
                        playIndicator.SetCoefficient(wr3,1);
                        playIndicator.SetCoefficient(wr4,1);
                        playIndicator.SetCoefficient(wr5,1);
                        playIndicator.SetCoefficient(wr6,1);

                        //add player cost to priceConstraints
                        maxBudget.SetCoefficient(wrA, player.Price);
                        maxBudget.SetCoefficient(wr1, player.Price);
                        maxBudget.SetCoefficient(wr2, player.Price);
                        maxBudget.SetCoefficient(wr3, player.Price);
                        maxBudget.SetCoefficient(wr4, player.Price);
                        maxBudget.SetCoefficient(wr5, player.Price);
                        maxBudget.SetCoefficient(wr6, player.Price);

                        //add player to roster constraint
                        maxRosterSize.SetCoefficient(wrA,1);
                        maxRosterSize.SetCoefficient(wr1,1);
                        maxRosterSize.SetCoefficient(wr2,1);
                        maxRosterSize.SetCoefficient(wr3,1);
                        maxRosterSize.SetCoefficient(wr4,1);
                        maxRosterSize.SetCoefficient(wr5,1);
                        maxRosterSize.SetCoefficient(wr6,1);

                        //add player to active position Constraint
                        activeWideReceiverPositions.SetCoefficient(wrA, 1);

                        //add player to bench constraint;
                        maxBenchSize.SetCoefficient(wr1,1);
                        maxBenchSize.SetCoefficient(wr2,1);
                        maxBenchSize.SetCoefficient(wr3,1);
                        maxBenchSize.SetCoefficient(wr4,1);
                        maxBenchSize.SetCoefficient(wr5,1);
                        maxBenchSize.SetCoefficient(wr6,1);

                        //add player to bench position constraints
                        wideReceiverBenchPosition1.SetCoefficient(wr1,1);
                        wideReceiverBenchPosition2.SetCoefficient(wr2,1);
                        wideReceiverBenchPosition3.SetCoefficient(wr3,1);
                        wideReceiverBenchPosition4.SetCoefficient(wr4,1);
                        wideReceiverBenchPosition5.SetCoefficient(wr5,1);
                        wideReceiverBenchPosition6.SetCoefficient(wr6,1);

                        //add player points to objective function
                        objectiveFunction.SetCoefficient(wrA, player.ProjectedPoints);
                        objectiveFunction.SetCoefficient(wr1,Math.Pow(0.5, 1) * player.ProjectedPoints);
                        objectiveFunction.SetCoefficient(wr2,Math.Pow(0.5, 2) * player.ProjectedPoints);
                        objectiveFunction.SetCoefficient(wr3,Math.Pow(0.5, 3) * player.ProjectedPoints);
                        objectiveFunction.SetCoefficient(wr4,Math.Pow(0.5, 4) * player.ProjectedPoints);
                        objectiveFunction.SetCoefficient(wr5,Math.Pow(0.5, 5) * player.ProjectedPoints);
                        objectiveFunction.SetCoefficient(wr6,Math.Pow(0.5, 6) * player.ProjectedPoints);
                        break;

                    case PlayPosition.K:

                        // create indicators for position and player constraints
                        var kA = solver.MakeIntVar(0, 1, $"{player.Name} Active Kicker");

                        solverVariables.Add(kA);

                        playIndicator.SetCoefficient(kA, 1);

                        //add player cost to priceConstraints
                        maxBudget.SetCoefficient(kA, player.Price);

                        //add player to roster constraint
                        maxRosterSize.SetCoefficient(kA, 1);

                        //add player to total position Constraint
                        totalKickerPositions.SetCoefficient(kA, 1);

                        //add player to active position Constraint
                        activeKickerPositions.SetCoefficient(kA, 1);

                        //add player points to objective function
                        objectiveFunction.SetCoefficient(kA, player.ProjectedPoints);
                        break;

                    case PlayPosition.Te:

                        //create indicators for position and player constraints
                        var teA = solver.MakeIntVar(0, 1, $"{player.Name} Active Tight End");
                        var te1 = solver.MakeIntVar(0, 1, $"{player.Name} Bench 1 Tight End");

                        solverVariables.Add(teA);
                        solverVariables.Add(te1);

                        playIndicator.SetCoefficient(teA, 1);
                        playIndicator.SetCoefficient(te1, 1);

                        //add player cost to priceConstraints
                        maxBudget.SetCoefficient(teA, player.Price);
                        maxBudget.SetCoefficient(te1, player.Price);

                        //add player to roster constraint
                        maxRosterSize.SetCoefficient(teA, 1);
                        maxRosterSize.SetCoefficient(te1, 1);

                        //add player to total position Constraint
                        totalTightEndPositions.SetCoefficient(teA, 1);
                        totalTightEndPositions.SetCoefficient(te1, 1);

                        //add player to active position Constraint
                        activeTightEndPositions.SetCoefficient(teA, 1);

                        //add player to bench constraint
                        maxBenchSize.SetCoefficient(te1, 1);

                        //add player points to objective function
                        objectiveFunction.SetCoefficient(teA, player.ProjectedPoints);
                        objectiveFunction.SetCoefficient(te1, Math.Pow(0.5, 1) * player.ProjectedPoints);
                        break;

                    case PlayPosition.Def:

                        // create indicators for position and player constraints
                        var defA = solver.MakeIntVar(0, 1, $"{player.Name} Active Defender");

                        solverVariables.Add(defA);

                        playIndicator.SetCoefficient(defA, 1);

                        //add player cost to priceConstraints
                        maxBudget.SetCoefficient(defA, player.Price);

                        //add player to roster constraint
                        maxRosterSize.SetCoefficient(defA, 1);

                        //add player to total position Constraint
                        totalDefenderPositions.SetCoefficient(defA, 1);

                        //add player to active position Constraint
                        activeDefenderPositions.SetCoefficient(defA, 1);

                        //add player points to objective function
                        objectiveFunction.SetCoefficient(defA, player.ProjectedPoints);
                        break;

                    default:
                        throw new ArgumentOutOfRangeException();
                }
            }


            solver.Solve();
            Console.WriteLine("Players & Positions Used");
            var totalCost = 0.0;
            var quarterbacks = 1;
            var runningBacks = 1;
            var wideReceivers = 1;
            var kickers = 1;
            var tightEnds = 1;
            var defenders = 1;

            foreach (var variable in solverVariables.Where(x=> x.SolutionValue() > 0))
            {
                if (variable.Name().Contains("Quarterback"))
                {
                    Console.WriteLine($"Player Position: {variable.Name()} - Overall Position: Quarterback {quarterbacks}");
                    quarterbacks++;
                }
                else if (variable.Name().Contains("Running Back"))
                {
                    Console.WriteLine($"Player Position: {variable.Name()} - Position: Running Back {runningBacks}");
                    runningBacks++;
                }
                else if (variable.Name().Contains("Wide Receiver"))
                {
                    Console.WriteLine($"Player Position: {variable.Name()} - Position: Wide Receiver {wideReceivers}");
                    wideReceivers++;
                }
                else if (variable.Name().Contains("Kicker"))
                {
                    Console.WriteLine($"Player Position: {variable.Name()} - Position: Kicker {kickers}");
                    kickers++;
                }
                else if (variable.Name().Contains("Tight End"))
                {
                    Console.WriteLine($"Player Position: {variable.Name()} - Position: Tight End {tightEnds}");
                    tightEnds++;
                }
                else if (variable.Name().Contains("Defender"))
                {
                    Console.WriteLine($"Player Position: {variable.Name()} - Position: Defender {defenders}");
                    defenders++;
                }

                totalCost += maxBudget.GetCoefficient(variable);
            }

            Console.WriteLine($"Projected Points: {solver.Objective().Value()}");
            Console.WriteLine($"Budget Used: {totalCost}");
            Console.ReadLine();
        }

        public static List<Player> ParseCsv(string fileLocation)
        {
            using (var reader = new StreamReader(fileLocation))
            {
                using (var csvReader = new CsvReader(reader, CultureInfo.InvariantCulture))
                {
                    var records = csvReader.GetRecords<Player>();
                    return records.ToList();
                }
            }
        }
    }

    public class BudgetConstraints
    {
        public int Budget { get; set; }
        public int RosterLength { get; set; }
        public int MaxQb { get; set; }
        public int MaxTe { get; set; }
        public int MaxK { get; set; }
        public int MaxDef { get; set; }
        public int MaxPlayerOccurrence { get; set; }
        public int MaxActiveQb { get; set; }
        public int MaxActiveWr { get; set; }
        public int MaxActiveRb { get; set; }
        public int MaxActiveTe { get; set; }
        public int MaxActiveDef { get; set; }
        public int MaxActiveK { get; set; }
        public int MaxBenchedPlayers { get; set; }
    }

    public class Player
    {
        public string Name { get; set; }
        public PlayPosition Position { get; set; }
        public string Team { get; set; }
        public double ProjectedPoints { get; set; }
        public double Price { get; set; }
    }

    public enum PlayPosition
    {
        Qb,
        Rb,
        Wr,
        K,
        Te,
        Def
    }
}
