namespace Pseudoku.Solver
{
    public interface IValidator
    {
        public int ValidatorDifficulty { get; set; }
        public bool ValidatePotentialCellValues(PseudoCell cell, PseudoBoard board);
    }
}
