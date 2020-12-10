namespace Pseudoku.Solver
{
    public interface IMethod
    {
        public bool ApplyMethod(PseudoCell cell, PseudoBoard board);
    }
}
