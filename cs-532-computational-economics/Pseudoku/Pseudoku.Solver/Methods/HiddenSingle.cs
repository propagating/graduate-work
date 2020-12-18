using System.Collections.Generic;
using System.Linq;

namespace Pseudoku.Solver.Methods
{
    public class HiddenSingle : IMethod
    {
        public bool ApplyMethod(PseudoCell cell, PseudoBoard board)
        {
            foreach (var value in cell.PossibleValues)
            {
                var rowCells = board.BoardCells.Where(x=> x.CellRow == cell.CellRow).Where(x => x.PossibleValues.Contains(value)).ToList();
                var colCells = board.BoardCells.Where(x=> x.CellColumn == cell.CellColumn).Where(x => x.PossibleValues.Contains(value)).ToList();
                var boxCells = board.BoardCells.Where(x=> x.CellBox == cell.CellBox).Where(x => x.PossibleValues.Contains(value)).ToList();

                if (rowCells.Count == 1 || colCells.Count == 1 || boxCells.Count == 1)
                {
                    cell.CurrentValue = value;
                    cell.PossibleValues = new List<int>();
                    cell.SolvedCell = true;
                    return true;
                }
            }
            return board.ValidState;
        }
    }
}
