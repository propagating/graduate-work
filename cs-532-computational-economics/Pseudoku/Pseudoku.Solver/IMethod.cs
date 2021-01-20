namespace Pseudoku.Solver
{
    public interface IMethod
    {
        public int MethodDifficulty { get; set; }
        public bool ApplyMethod(PseudoCell cell, PseudoBoard board);
    }
}
