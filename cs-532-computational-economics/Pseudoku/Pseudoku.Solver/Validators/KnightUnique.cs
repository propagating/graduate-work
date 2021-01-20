using System.Collections.Generic;
using System.Linq;

namespace Pseudoku.Solver.Validators
{
    public class KnightUnique : IValidator
    {
        public int ValidatorDifficulty { get; set; } = 1;
        public static readonly List<(int,int)> KnightMoves = new List<(int, int)>{(1 , 2), (1 , -2), (-1, 2), (-1, -2), (2 , 1), (2 , -1), (-2, 1), (-2, -1)};

        public bool ValidatePotentialCellValues(PseudoCell cell, PseudoBoard board)
        {
            var startCount = cell.PossibleValues.Count; //can be used in case we need to implement guessing as a way to rollback changes
            foreach (var move in KnightMoves.ToList())
            {
                var moveVertical   = cell.CellRow + move.Item1;
                var moveHorizontal = cell.CellColumn + move.Item2;

                var existingValues = board.BoardCells.Where(x => x.CellRow == moveVertical
                                                                 && x.CellColumn == moveHorizontal
                                                                 && x.CellBox != cell.CellBox
                                                                 && x.SolvedCell
                                                                 && cell.PossibleValues.Contains(x.CurrentValue)).Select(x=> x.CurrentValue).ToList();
                foreach (var value in existingValues)
                {
                    cell.PossibleValues.Remove(value);
                }
                if (cell.PossibleValues.Count == 1)
                {
                    cell.CurrentValue   = cell.PossibleValues.First(); //only 1 value remains.
                    cell.PossibleValues = new List<int>();
                    cell.SolvedCell     = true;
                    return true;
                }

            }

            return cell.PossibleValues.Count != startCount;
        }

    }
}
