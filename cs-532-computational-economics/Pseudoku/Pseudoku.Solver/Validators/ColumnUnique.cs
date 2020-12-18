using System.Collections.Generic;
using System.Linq;

namespace Pseudoku.Solver.Validators
{
    public class ColumnUnique : IValidator
    {
        public bool ValidatePotentialCellValues(PseudoCell cell, PseudoBoard board)
        {
            var existingValues = board.BoardCells.Where(x => x.CellColumn == cell.CellColumn && x.SolvedCell && cell.PossibleValues.Contains(x.CurrentValue)).Select(x=> x.CurrentValue).ToList();

            foreach (var value in existingValues)
            {
                cell.PossibleValues.Remove(value);
            }

            if (cell.PossibleValues.Count == 1)
            {
                cell.CurrentValue = cell.PossibleValues.First(); //only 1 value remains.
                cell.PossibleValues = new List<int>();
                cell.SolvedCell = true;
            }


            return board.ValidState; //for use if we end up with some sort of recursive guessing
        }
    }
}
