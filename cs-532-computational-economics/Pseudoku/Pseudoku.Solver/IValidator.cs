namespace Pseudoku.Solver
{
    public interface IValidator
    {
        public bool ValidatePotentialCellValues(PseudoCell cell, PseudoBoard board);
    }
}
