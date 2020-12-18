using System.Collections.Generic;
using System.Linq;

namespace Pseudoku.Solver.Validators
{
    public class KingUnique : IValidator
    {
        public static readonly List<(int, int)> KingMoves = new List<(int, int)> {(1, 1), (1, -1), (-1, 1), (-1, -1)};
        public bool ValidatePotentialCellValues(PseudoCell cell, PseudoBoard board)
        {
            var cellValues = cell.PossibleValues.ToList(); //can be used in case we need to implement guessing as a way to rollback changes
            foreach (var move in KingMoves.ToList())
            {
                var existingValues = board.BoardCells
                                          .Where(x => x.CellRow == (cell.CellRow + move.Item1) && x.CellColumn == (cell.CellColumn + move.Item2) &&
                                                      x.SolvedCell && cell.PossibleValues.Contains(x.CurrentValue)).Select(x => x.CurrentValue).ToList();

                if(existingValues.Any())
                {
                    foreach (var value in existingValues)
                    {
                        cell.PossibleValues.Remove(value);
                    }

                    if (cell.PossibleValues.Count == 1)
                    {
                        cell.CurrentValue = cell.PossibleValues.First(); //only 1 value remains.
                        cell.PossibleValues = new List<int>();
                        cell.SolvedCell = true;
                        return true;
                    }
                }
            }

            return board.ValidState;
        }
    }
}
