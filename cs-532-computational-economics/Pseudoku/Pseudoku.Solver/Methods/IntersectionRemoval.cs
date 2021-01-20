using System.Linq;

namespace Pseudoku.Solver.Methods
{
    public class IntersectionRemoval : IMethod
    {
        public int MethodDifficulty { get; set; } = 1;

        public bool ApplyMethod(PseudoCell cell, PseudoBoard board)
        {
            var startCount = cell.PossibleValues.Count;
            foreach (var value in cell.PossibleValues)
            {
                var sharedBoxCount = 0;
                var sharedBoxCells = board.BoardCells.Where(x => x.CellBox == cell.CellBox && cell.PossibleValues.Contains(value)).ToList();
                sharedBoxCount = sharedBoxCells.Count;
                if (sharedBoxCells.Any() && sharedBoxCount <= 3)
                {
                    if (sharedBoxCells.Where(x => x.CellRow == cell.CellRow).Count() == sharedBoxCount)
                    {
                        foreach (var boardCell in board.BoardCells.Where(x => x.CellRow == cell.CellRow && x.CellBox != cell.CellBox))
                        {
                            boardCell.PossibleValues.Remove(value);
                        }
                    }

                    if (sharedBoxCells.Where(x => x.CellColumn == cell.CellColumn).Count() == sharedBoxCount)
                    {
                        foreach (var boardCell in board.BoardCells.Where(x => x.CellColumn == cell.CellColumn && x.CellBox != cell.CellBox))
                        {
                            boardCell.PossibleValues.Remove(value);
                        }
                    }
                }
            }
            return cell.PossibleValues.Count != startCount;
        }
    }
}
