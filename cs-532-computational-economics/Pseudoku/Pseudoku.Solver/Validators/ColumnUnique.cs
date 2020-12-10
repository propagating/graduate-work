using System.Linq;

namespace Pseudoku.Solver.Validators
{
    public class ColumnUnique : IValidator
    {
        public bool ValidatePotentialCellValues(PseudoCell cell, PseudoBoard board)
        {
            var existingValues = board.BoardCells.Where(x => x.CellColumn == cell.CellColumn && x.SolvedCell).Select(x=> x.CurrentValue).ToList();
            var cellValues = cell.PossibleValues.ToList();

            foreach (var value in existingValues)
            {
                cell.PossibleValues.Remove(value);
            }

            if (!cell.PossibleValues.Any())
            {
                board.ValidState = false; //board is invalid and can be disposed
                return false;
            }
            else if (cellValues.Count == cell.PossibleValues.Count)
            {
                board.ValidState = false;
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
