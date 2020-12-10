using System.Linq;

namespace Pseudoku.Solver.Validators
{
    public class RowUnique : IValidator
    {
        public bool ValidatePotentialCellValues(PseudoCell cell, PseudoBoard board)
        {
            var existingValues = board.BoardCells.Where(x => x.CellRow == cell.CellRow && x.SolvedCell).Select(x=> x.CurrentValue).ToList();
            var cellValues = cell.PossibleValues.ToList();

            foreach (var value in existingValues)
            {
                cell.PossibleValues.Remove(value);
            }

            if (!cell.PossibleValues.Any())
            {
                board.ValidState = false; //board is invalid and can be disposed
                cell.PossibleValues = cellValues;
            }
            else if (cell.PossibleValues.Count == 1)
            {
                cell.CurrentValue = cell.PossibleValues.First(); //only 1 value remains.
                cell.SolvedCell = true;
            }
            return board.ValidState;
        }
    }
}
