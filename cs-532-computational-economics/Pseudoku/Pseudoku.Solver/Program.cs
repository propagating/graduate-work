using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Runtime.InteropServices.ComTypes;
using Pseudoku.Solver.Methods;
using Pseudoku.Solver.Validators;

namespace Pseudoku.Solver
{
    class Program
    {
        static void Main(string[] args)
        {
            var quitResponse = "";
            do
            { Console.WriteLine("Welcome to PsuedoSolver");
            int numColumn = 9;
            int numRow = 9;
            WriteBreak();
            /*Console.WriteLine("How many columns does your Grid have?");
            Console.WriteLine("Current Grid Size is limited to any combination of values between 1x1 and 9x9");


            while (!int.TryParse("9", out numColumn) || numColumn == 0 || numColumn > 9)
            {
                Console.WriteLine("Please enter a numerical value between 1 and 9 for number of columns.");
                Console.WriteLine("Current Grid Size is limited to any combination of values between 1x1 and 9x9");
                Console.WriteLine();
            }
            WriteBreak();

            Console.WriteLine("How many Rows does your Grid have?");
            while (!int.TryParse("9", out numRow) || numRow == 0 || numRow > 9)
            {
                Console.WriteLine("Please enter a numerical value between 1 and 9 for number of rows.");
                Console.WriteLine("Current Grid Size is limited to any combination of values between 1x1 and 9x9");
                Console.WriteLine();
            }
            WriteBreak();

            Console.WriteLine("Please enter the string of numbers to represent your grid.");

            Console.WriteLine("Your Grid will be inserted from left to right, then top to bottom.\n" +
                              "A value of 0 will be treated as an empty cell.");
            Console.WriteLine();

            Console.WriteLine("For example, a 2x2 grid with empty values in R1C1 and R2C2 are entered as:\n" +
                              "0220");
            WriteBreak();*/

            /*while (string.IsNullOrWhiteSpace(gridString) || gridString.Length != (numColumn * numRow) || !gridString.All(char.IsDigit))
            {
                Console.WriteLine("Please enter a value containing only numbers of equal length to your grid size (Columns * Rows).");
                Console.WriteLine();
                gridString = Console.ReadLine();
            }
            WriteBreak();

            Console.WriteLine("Please select the types of constraints your puzzle has:");
            Console.WriteLine("Constraints can are entered as single letter keys in any order.");
            WriteBreak();
            Console.WriteLine("For Example, a puzzle with both King and Knight's Move Constraints can be entered as KN, NK, kn, nK, etc.");
            Console.WriteLine("Current Solver requires that Standard Sudoku Rules are followed at a minimum.");
            WriteBreak();

            Console.WriteLine("Currently Supported Constraints :");
            Console.WriteLine("K: King's Rule - Numbers cannot be within a chess king's move of the same number.");
            Console.WriteLine("N: Knight's Move - Numbers cannot be within a chess knight's move of the same number.");


            if (!string.IsNullOrWhiteSpace(constraints))
            {
                while (!constraints.ToUpper().Contains("K") && !constraints.ToUpper().Contains("N"))
                {
                    if (string.IsNullOrWhiteSpace(constraints))
                    {
                        break;
                    }
                    Console.WriteLine();
                    Console.WriteLine("Invalid constraint selection. Please enter K for King's Move, or N for Knight's Move");
                    Console.WriteLine("To use ONLY traditional Sudoku rules, enter a blank response.");

                    constraints = Console.ReadLine();
                }
            }
            WriteBreak();*/


            var gridString        = "";
            var sudokuGridString  = "005003060000580104300900050450039700100075000930000540500104093000358072003200600";
            var knightsGridString = "003608100040000070200000003600090008000102000700060004400000001060000020005409800";
            var kingsGridString   = "070003000009000507010070020800205000006000400000908005050030040201000800000500090";

            Console.WriteLine(
                "Please enter the number of the puzzle you'd like to solve.\nFor demonstration purposes, 3 puzzles with different constraints are provided.");
            Console.WriteLine("1. Standard Sudoku Rules Only");
            Console.WriteLine("2. Knights Move Constraint Sudoku (same number cannot be a chess Knight's Move Apart)");
            Console.WriteLine("3. Kings Move Constraint Sudoku (same number cannot be a chess King's Move Apart)");
            WriteBreak();

            int response;
            while (!int.TryParse(Console.ReadLine(), out response) || response < 1 || response > 3)
            {
                Console.WriteLine("ERROR: Please enter an integer from 1 to 3 that matches the puzzle you'd like a demonstration of.");
                Console.WriteLine("1. Standard Sudoku Rules Only");
                Console.WriteLine("2. Knights Move Constraint Sudoku (same number cannot be a chess Knight's Move Apart)");
                Console.WriteLine("3. Kings Move Constraint Sudoku (same number cannot be a chess King's Move Apart)");
                WriteBreak();

            }

            var constraints = "";
            switch (response)
            {
                case 1:
                    constraints = "";
                    gridString = sudokuGridString;
                    break;
                case 2:
                    constraints = "N";
                    gridString = knightsGridString;
                    break;
                case 3:
                    constraints = "K";
                    gridString = kingsGridString;
                    break;
            }

            var puzzleConstraints = new List<PuzzleConstraint>();
            puzzleConstraints.Add(PuzzleConstraint.NormalSudoku);
            if (constraints != null && constraints.ToUpper().Contains("K")) puzzleConstraints.Add(PuzzleConstraint.KingsMove);
            if (constraints != null && constraints.ToUpper().Contains("N")) puzzleConstraints.Add(PuzzleConstraint.KnightsMove);

            /*Console.WriteLine("Please verify the dimensions, constraints, and puzzle string are correct.");

            Console.WriteLine($"Puzzle Dimension : {numRow} Rows by {numColumn} Columns");*/
            WriteBreak();
            Console.WriteLine($"Constrains Chosen:");
            foreach (var c in puzzleConstraints)
            {
                Console.WriteLine(c.ToString());
            }

            WriteBreak();
            Console.WriteLine("Puzzle String");
            Console.WriteLine(gridString);

            var board = new PseudoBoard(numRow, numColumn, gridString);
            board.PrintBoard();
            WriteBreak();

            Console.WriteLine("Press any key to solve the puzzle.");
            Console.ReadLine();

            var solver = new Solver(puzzleConstraints);
            solver.Solve(board);

            Console.WriteLine("Enter any key to select a different puzzle, except for (Q).\nEnter (Q) to quit");
            quitResponse = Console.ReadLine();
        }
        while (string.IsNullOrWhiteSpace(quitResponse) || quitResponse.ToUpper() != "Q") ;

        }

        public static void WriteBreak()
        {
            Console.WriteLine();
            Console.WriteLine("------------------------------------------------------------------------");
            Console.WriteLine();
        }
    }

    public class Solver
    {
        public List<IValidator> BoardValidators { get; set; } = new List<IValidator>();
        public List<IMethod> SolverMethods { get; set; } = new List<IMethod>();

        public Solver(List<PuzzleConstraint> constraints)
        {
            SolverMethods.Add(new HiddenSingle());
            SolverMethods.Add(new IntersectionRemoval());


            foreach (var constraint in constraints)
            {
                switch (constraint)
                {
                    case PuzzleConstraint.NormalSudoku:
                        BoardValidators.Add( new ColumnUnique());
                        BoardValidators.Add(new RowUnique());
                        BoardValidators.Add(new BoxUnique());
                        break;
                    case PuzzleConstraint.KnightsMove:
                        BoardValidators.Add(new KnightUnique());
                        break;
                    case PuzzleConstraint.KingsMove:
                        BoardValidators.Add(new KingUnique());
                        break;
                    default:
                        throw new ArgumentOutOfRangeException();
                }
            }
        }
        public void Solve(PseudoBoard board)
        {
            var currentFailures = 0;
            var totalFailures   = 0;
            var stepCount       = 0;
            var timer           = new Stopwatch();

            timer.Start();
            while (!board.PuzzleSolved)
            {
                var solvableCells = board.BoardCells.Where(x => !x.SolvedCell).ToList();
                foreach (var cell in solvableCells)
                {
                    foreach (var validator in BoardValidators)
                    {
                        var success = validator.ValidatePotentialCellValues(cell, board);
                        if (!success)
                        {
                            currentFailures++;
                            totalFailures++;
                        }
                        else currentFailures = 0;
                        stepCount++;
                    }

                    foreach (var method in SolverMethods)
                    {
                        method.ApplyMethod(cell, board);
                        stepCount++;
                    }
                }

                board.PuzzleSolved = board.BoardCells.All(x => x.SolvedCell);
            }
            timer.Stop();
            board.PrintBoard();
            Console.WriteLine();
            Console.WriteLine($"Puzzle Solved in {timer.Elapsed}\nTotal Steps Taken (Validators & Solve Methods) {stepCount}\nTotal Actions Taken (Validators & Solve Methods w/ Legal Move Available) {stepCount-totalFailures}");
        }
    }


    public class PseudoCell
    {
        public int CellRow { get; set; }
        public int CellColumn { get; set; }
        public int CellBox { get; set; }
        public List<int> PossibleValues { get; set; } = new List<int>();
        public int CurrentValue { get; set; }
        public bool SolvedCell { get; set; } = false;

        public void FindBox()
        {
            //assume 9x9 grid for now until custom boxes are allowed
            if(CellColumn <= 3 && CellRow <=3) CellBox = 1;
            else if(CellColumn <= 6 && CellRow <=3) CellBox = 2;
            else if(CellColumn <= 9 && CellRow <=3) CellBox = 3;
            else if(CellColumn <= 3 && CellRow <=6) CellBox = 4;
            else if(CellColumn <= 6 && CellRow <=6) CellBox = 5;
            else if(CellColumn <= 9 && CellRow <=6) CellBox = 6;
            else if(CellColumn <= 3 && CellRow <=9) CellBox = 7;
            else if(CellColumn <= 6 && CellRow <=9) CellBox = 8;
            else if(CellColumn <= 9 && CellRow <=9) CellBox = 9;

        }
    }

    public class PseudoBoard
    {
        public List<PseudoCell> BoardCells { get; set; } = new List<PseudoCell>();
        public int MaxRows { get; set; }
        public int MaxColumns { get; set; }
        public List<int> AllowedValues { get; set; }
        public bool ValidState { get; set; } = true;
        public bool PuzzleSolved { get; set; }

        public PseudoBoard(int rows, int cols, string inputValues)
        {
            MaxRows           = rows;
            MaxColumns        = cols;
            AllowedValues     = Enumerable.Range(1, Math.Max(MaxRows, MaxColumns)).Select(x => x).ToList();
            var currentRow    = 1;
            var currentColumn = 1;
            var currentIndex  = 0;

            var values = inputValues.ToList();

            while (currentRow <= MaxRows)
            {
                while (currentColumn <= MaxColumns)
                {
                    var cellValue = Convert.ToInt32(values[currentIndex] - 48); //char of 0 enters as 48
                    var pseudoCell = new PseudoCell
                    {
                        CellRow        = currentRow,
                        CellColumn     = currentColumn,
                        CurrentValue   = cellValue,
                        PossibleValues = cellValue == 0 ? Enumerable.Range(1, Math.Max(MaxRows, MaxColumns)).Select(x=> x).ToList(): new List<int>(), //create a new list object to avoid passing around the list by reference, each class needs a unique list of values
                        SolvedCell     = cellValue == 0 ? false : true
                    };

                    pseudoCell.FindBox();
                    BoardCells.Add(pseudoCell);
                    currentIndex++;
                    currentColumn++;
                }

                currentColumn = 1;
                currentRow++;
            }
        }

        public void PrintBoard()
        {
            var currentRow = 1;
            Console.WriteLine("___________________________________");
            while (currentRow <= MaxRows)
            {
                foreach (var box in BoardCells.Where(x=> x.CellRow == currentRow).GroupBy(x=> x.CellBox))
                {
                    foreach (var cell in box)
                    {
                        if(cell.CellColumn == 1){Console.Write("||");}
                        if(cell.CurrentValue == 0){Console.Write("   ");}
                        else{Console.Write($" {cell.CurrentValue} ");}
                    }
                    Console.Write("||");
                }

                Console.WriteLine();
                if (currentRow == 9)
                {
                    Console.Write("-----------------------------------");
                    Console.WriteLine();
                }
                else if (currentRow % 3 == 0)
                {
                    Console.Write("||_________||_________||_________||");
                    Console.WriteLine();
                }
                currentRow++;
            }
        }
    }

    public enum PuzzleConstraint
    {
        NormalSudoku,
        KnightsMove,
        KingsMove
    }

}
